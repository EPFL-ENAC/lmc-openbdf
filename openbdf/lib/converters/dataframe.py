from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Any, Optional, TypeVar

import pandas as pd
from pydantic import ValidationError
from sqlmodel import SQLModel

from openbdf.lib.converters.lca_results import lca_results_wide_to_tall
from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator, PreprocessRule
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.types.values import parse_value, serialize_value
from openbdf.lib.validation.collect import MaterialPair, group_by_material_pair, material_pair
from openbdf.lib.validation.errors import (
    DroppedLine,
    DuplicateFieldCode,
    OpenBDFValidationError,
    TypeMismatch,
    UnknownEnumValue,
    findings_from_validation_error,
)
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.general_info import ProjectRecordBase
from openbdf.model.ingest import make_ingest_model
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    LCAResultsTallFullRecord,
    LCAResultsWideFullRecord,
    ProjectMaterialDatabaseRecord,
    ProjectRecord,
)

PROJECT_EXCLUDED_FIELDS = {"id", "bill_of_materials"}
BOM_EXCLUDED_FIELDS = {"id", "project_id", "project"}
RESULTS_EXCLUDED_FIELDS = {"id", "building_bill_materials_slim_record_id", "building_bill_materials_slim_record"}


def build_field_code_to_name_map(
    model_cls: type[SQLModel],
    excluded_fields: Optional[set[str]] = None,
) -> dict[str, str]:
    """
    Build a mapping from field_code -> field_name for a model.
    """
    excluded_fields = excluded_fields or set()
    mapping: dict[str, str] = {}

    for field_name, field_info in model_cls.model_fields.items():
        if field_name in excluded_fields:
            continue
        field_code = get_field_code(field_name, field_info)
        mapping[field_code] = field_name

    return mapping


def project_to_dataframe(project: ProjectRecord | ProjectRecordBase) -> pd.DataFrame:
    """
    Convert a ProjectRecord into a dataframe with one row per attribute.

    Output columns:
    - field_code
    - field_name
    - attribute_name
    - value
    """
    rows: list[dict[str, Any]] = []
    fields = ProjectRecordBase.model_fields

    for field_name, field_info in fields.items():
        if field_name in PROJECT_EXCLUDED_FIELDS:
            continue

        rows.append({
            "field_code": get_field_code(field_name, field_info),
            "value": serialize_value(getattr(project, field_name, None)),
        })

    return pd.DataFrame(rows)


def bom_to_dataframe(
    items: list[BuildingBillMaterialsSlimRecord],
) -> pd.DataFrame:
    """
    Convert a list of BuildingBillMaterialsSlimRecord into a tabular dataframe.

    Columns use field_code values when available.
    """
    fields = BuildingBillMaterialsSlimRecord.model_fields

    included_fields: list[tuple[str, Any, str]] = []
    for field_name, field_info in fields.items():
        if field_name in BOM_EXCLUDED_FIELDS:
            continue
        field_code = get_field_code(field_name, field_info)
        included_fields.append((field_name, field_info, field_code))

    rows: list[dict[str, Any]] = []
    for item in items:
        row: dict[str, Any] = {}
        for field_name, _, field_code in included_fields:
            row[field_code] = serialize_value(getattr(item, field_name, None))
        rows.append(row)

    return pd.DataFrame(rows, columns=[field_code for _, _, field_code in included_fields])


ModelT = TypeVar("ModelT", bound=SQLModel)


def horizontal_to_dataframe(
    items: list[ModelT],
    model_cls: type[ModelT],
) -> pd.DataFrame:
    """
    Convert a list of BuildingBillMaterialsSlimRecord into a tabular dataframe.

    Columns use field_code values when available.
    """
    fields = model_cls.model_fields

    included_fields: list[tuple[str, Any, str]] = []
    for field_name, field_info in fields.items():
        field_code = get_field_code(field_name, field_info)
        included_fields.append((field_name, field_info, field_code))

    rows: list[dict[str, Any]] = []
    for item in items:
        row: dict[str, Any] = {}
        for field_name, _, field_code in included_fields:
            row[field_code] = serialize_value(getattr(item, field_name, None))
        rows.append(row)

    return pd.DataFrame(rows, columns=[field_code for _, _, field_code in included_fields])


def parse_finding(
    annotation: Any,
    raw_value: Any,
    field_code: str,
    source: str,
    row: int | None,
) -> OpenBDFValidationError:
    """Describe a cell that parse_value could not read as a field finding."""
    annotation, _ = unwrap_optional(annotation)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return UnknownEnumValue(f"Value {raw_value!r} is not a valid {annotation.__name__}", source=source, row=row)
    return TypeMismatch(
        f"Field {field_code} expects {getattr(annotation, '__name__', annotation)}", source=source, row=row
    )


def horizontal_from_dataframe(
    df: pd.DataFrame,
    model_cls: type[ModelT],
    translator_category: str,
    *,
    excluded_fields: set[str] | None = None,
    document_translator: DocumentTranslator | None = None,
    findings: list[OpenBDFValidationError] | None = None,
    drop_invalid: bool = False,
) -> list[ModelT]:
    """
    Build a list of model instances from a horizontal dataframe.

    Dataframe columns are interpreted as field_code values.
    Unknown columns are ignored.

    Every row is read into an all-optional ingest model and then validated with
    model_cls. A row that fails validation is kept as read and its findings are
    added to the findings list, so one bad cell does not stop the pipeline.

    If drop_invalid is True, the rows that miss a required field are not kept and
    each of them is reported as an E33 warning.
    """
    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()
    if findings is None:
        findings = []

    fields = model_cls.model_fields
    code_to_name = build_field_code_to_name_map(
        model_cls,
        excluded_fields=excluded_fields,
    )
    name_to_code = {name: code for code, name in code_to_name.items()}
    ingest_cls = make_ingest_model(model_cls)

    # The column set is fixed for all rows, so translation, field resolution
    # and default parsing run once instead of once per row.
    column_plans: list[list[tuple[str, Any, PreprocessRule | None]]] = []
    seen_field_names: set[str] = set()
    for column in df.columns:
        column_plan: list[tuple[str, Any, PreprocessRule | None]] = []
        for translated_code in document_translator.translate(translator_category, str(column)):
            field_name = code_to_name.get(translated_code)
            if field_name is None:
                continue
            if field_name in seen_field_names:
                findings.append(
                    DuplicateFieldCode(
                        f"Field code {translated_code} is declared twice",
                        source=translator_category,
                    )
                )
            seen_field_names.add(field_name)
            column_plan.append((
                field_name,
                fields[field_name].annotation,
                document_translator.get_preprocess_rule(translator_category, field_name),
            ))
        column_plans.append(column_plan)

    # parse_value returns only immutable scalars, so the parsed defaults can
    # be shared across all rows.
    default_plans: list[tuple[str, Any]] = []
    for field_code, default_field_name in code_to_name.items():
        default_value = document_translator.get_default(translator_category, field_code)
        if default_value is not None:
            default_plans.append((
                default_field_name,
                parse_value(fields[default_field_name].annotation, default_value, document_translator),
            ))

    items: list[ModelT] = []

    for row_index, row_values in zip(df.index, df.itertuples(index=False, name=None)):
        row = int(row_index) + 1
        kwargs: dict[str, Any] = {}
        row_findings: list[OpenBDFValidationError] = []
        failed_fields: set[str] = set()

        for column_plan, raw_cell in zip(column_plans, row_values):
            for field_name, annotation, preprocess_rule in column_plan:
                raw_value = raw_cell
                if preprocess_rule:
                    result = preprocess_rule.execute(raw_value)
                    if result.valid:
                        raw_value = result.value
                    else:
                        raw_value = None

                try:
                    kwargs[field_name] = parse_value(
                        annotation,
                        raw_value,
                        document_translator,
                    )
                except (ValueError, ArithmeticError):
                    kwargs[field_name] = None
                    failed_fields.add(field_name)
                    row_findings.append(
                        parse_finding(
                            annotation,
                            raw_value,
                            name_to_code.get(field_name, field_name),
                            translator_category,
                            row,
                        )
                    )

        for field_name, default_parsed in default_plans:
            if kwargs.get(field_name) is not None:
                continue
            kwargs[field_name] = default_parsed

        if not any(value is not None for value in kwargs.values()):
            continue

        record = ingest_cls(**kwargs)
        try:
            # A None value means the sheet carries no value, so pydantic reports it
            # as a missing required field instead of a type mismatch.
            record = model_cls.model_validate(record.model_dump(exclude_none=True))
        except ValidationError as exc:
            row_findings.extend(
                findings_from_validation_error(
                    exc,
                    model_cls,
                    source=translator_category,
                    row=row,
                    skip_fields=frozenset(failed_fields),
                )
            )
            if drop_invalid and any(finding.code == "E01" for finding in row_findings):
                findings.append(
                    DroppedLine(
                        _dropped_line_message(row, kwargs.get("material_id"), row_findings),
                        source=translator_category,
                        row=row,
                    )
                )
                continue

        findings.extend(row_findings)
        items.append(record)

    return items


def model_from_vertical_dataframe(
    project_df: pd.DataFrame,
    model_cls: type[ModelT],
    excluded_fields: set[str] | None = None,
    translator_category: str = COMMON_CATEGORY_PROPERTIES["project"]["name"],
    *,
    document_translator: DocumentTranslator | None = None,
    findings: list[OpenBDFValidationError] | None = None,
) -> ModelT:
    """
    Build a project model from a dataframe produced by project_to_dataframe().

    Expected columns:
    - field_code
    - value

    Extra columns are ignored.

    Every value is read into an all-optional ingest model and then validated with
    model_cls. A value that fails validation is kept as read and its findings are
    added to the findings list, so one bad cell does not stop the pipeline.
    """
    required_columns = {"field_code", "value"}
    missing = required_columns - set(project_df.columns)
    if missing:
        raise ValueError(f"Project dataframe is missing required columns: {sorted(missing)}")

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()
    if findings is None:
        findings = []

    fields = model_cls.model_fields
    code_to_name = build_field_code_to_name_map(
        model_cls,
        excluded_fields=excluded_fields,
    )
    name_to_code = {name: code for code, name in code_to_name.items()}
    ingest_cls = make_ingest_model(model_cls)

    kwargs: dict[str, Any] = {}
    seen_field_names: set[str] = set()
    failed_fields: set[str] = set()
    field_rows: dict[str, int] = {}

    for row_index, row in project_df.iterrows():
        field_code = row["field_code"]
        row_number = int(row_index) + 1

        if pd.isna(field_code):
            continue

        field_codes = document_translator.translate(
            translator_category,
            str(field_code),
        )
        for field_code in field_codes:
            field_name = code_to_name.get(field_code)
            if field_name is None:
                continue

            if field_name in seen_field_names:
                findings.append(
                    DuplicateFieldCode(
                        f"Field code {field_code} is declared twice",
                        source=translator_category,
                        row=row_number,
                    )
                )
            seen_field_names.add(field_name)
            field_rows[field_name] = row_number

            annotation = fields[field_name].annotation
            try:
                kwargs[field_name] = parse_value(
                    annotation,
                    row["value"],
                    document_translator,
                )
            except (ValueError, ArithmeticError):
                kwargs[field_name] = None
                failed_fields.add(field_name)
                findings.append(
                    parse_finding(
                        annotation,
                        row["value"],
                        name_to_code.get(field_name, field_name),
                        translator_category,
                        row_number,
                    )
                )

    for field_code, field_name in code_to_name.items():
        if kwargs.get(field_name) is not None:
            continue
        default_value = document_translator.get_default(translator_category, field_code)
        if default_value is not None:
            field_info = fields[field_name]
            kwargs[field_name] = parse_value(
                field_info.annotation,
                default_value,
                document_translator,
            )

    record = ingest_cls(**kwargs)
    try:
        return model_cls.model_validate(record.model_dump(exclude_none=True))
    except ValidationError as exc:
        findings.extend(
            findings_from_validation_error(
                exc,
                model_cls,
                source=translator_category,
                row_by_field=field_rows,
                skip_fields=frozenset(failed_fields),
            )
        )
        return record


def project_from_dataframe(
    project_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
) -> ProjectRecordBase:
    """
    Build a ProjectRecord from a dataframe produced by project_to_dataframe().

    Expected columns:
    - field_code
    - value

    Extra columns are ignored.
    """
    return model_from_vertical_dataframe(
        project_df,
        ProjectRecordBase,
        excluded_fields=PROJECT_EXCLUDED_FIELDS,
        translator_category=COMMON_CATEGORY_PROPERTIES["project"]["name"],
        document_translator=document_translator or DocumentTranslator(),
        findings=findings,
    )


def add_material_id_column_if_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure that the dataframe has a 'material_id' column.
    If not, add one with default values.
    """
    if "material_id" not in df.columns:
        df = df.copy()
        df.insert(
            0,
            "material_id",
            [f"MAT-{i + 1}" for i in range(len(df))],
        )
    return df


def _material_ref_id_number(material_ref_id: str | None) -> int:
    """Return the numeric suffix of an M%d material_ref_id, or 0."""
    if material_ref_id and material_ref_id.startswith("M") and material_ref_id[1:].isdigit():
        return int(material_ref_id[1:])
    return 0


def _first_text(records: list[Any], field_name: str) -> str | None:
    """Return the first non-blank value of a text field, without its surrounding spaces."""
    for record in records:
        value = (getattr(record, field_name) or "").strip()
        if value:
            return value
    return None


def _dropped_line_message(row: int, material_id: Any, reasons: list[OpenBDFValidationError]) -> str:
    """Describe a dropped line and the reasons that made it invalid."""
    identifier = f" (material_id {material_id!r})" if material_id else ""
    return f"Row {row}: line dropped{identifier}: {'; '.join(reason.message for reason in reasons)}"


def _bom_row_mass(row: BuildingBillMaterialsSlimRecordBase) -> Decimal:
    """Return the mass a bill of materials row contributes, repeated once per floor unless stated."""
    repetitions = 1 if row.floor_repetition is None else row.floor_repetition
    return (row.material_weight_kg or Decimal(0)) * repetitions


def _merge_project_material_database_draft(
    bill_of_materials: list[BuildingBillMaterialsSlimRecordBase],
    project_material_database: list[ProjectMaterialDatabaseBase],
) -> list[ProjectMaterialDatabaseBase]:
    """
    Merge the parsed project material database lines with the bill of materials.
    A material is the pair of its name and its EPD dataset name. Every bill of
    materials pair without a line gets a generated one, the automatic fields of
    every line are recomputed from its rows, and the rows are back-filled with the
    line's material_ref_id. A line without bill of materials rows is kept and its
    automatic fields count zero.
    """
    bom_rows_by_pair = group_by_material_pair(bill_of_materials)
    line_cls = make_ingest_model(ProjectMaterialDatabaseBase)

    first_line_by_pair: dict[MaterialPair, ProjectMaterialDatabaseBase] = {}
    for pmd in project_material_database:
        pair = material_pair(pmd.custom_material_name, pmd.lca_dataset_material_name)
        if pair is not None:
            first_line_by_pair.setdefault(pair, pmd)

    ref_id_records: list[ProjectMaterialDatabaseBase | BuildingBillMaterialsSlimRecordBase] = [
        *project_material_database,
        *bill_of_materials,
    ]
    highest_ref_id = max(
        (_material_ref_id_number(record.material_ref_id) for record in ref_id_records),
        default=0,
    )

    generated_by_pair: dict[MaterialPair, ProjectMaterialDatabaseBase] = {}
    for pair, bom_rows in bom_rows_by_pair.items():
        if pair in first_line_by_pair:
            continue
        highest_ref_id += 1
        generated_by_pair[pair] = line_cls(
            custom_material_name=_first_text(bom_rows, "custom_material_name"),
            lca_dataset_material_name=_first_text(bom_rows, "lca_dataset_material_name"),
            lca_database_name=_first_text(bom_rows, "lca_database_name"),
            material_ref_id=f"M{highest_ref_id:04d}",
        )

    total_mass = sum(
        (_bom_row_mass(row) for bom_rows in bom_rows_by_pair.values() for row in bom_rows),
        Decimal(0),
    )
    for pair, bom_rows in bom_rows_by_pair.items():
        line = first_line_by_pair.get(pair) or generated_by_pair[pair]
        line_mass = sum((_bom_row_mass(row) for row in bom_rows), Decimal(0))
        line.bom_row_count = len(bom_rows)
        line.material_mass_kg = line_mass
        line.material_mass_share = line_mass / total_mass * 100 if total_mass else Decimal(0)
        for row in bom_rows:
            row.material_ref_id = line.material_ref_id

    for pmd in project_material_database:
        pair = material_pair(pmd.custom_material_name, pmd.lca_dataset_material_name)
        if pair is None or pair not in bom_rows_by_pair:
            pmd.bom_row_count = 0
            pmd.material_mass_kg = Decimal(0)
            pmd.material_mass_share = Decimal(0)

    return [*project_material_database, *generated_by_pair.values()]


def bom_from_dataframe(
    bom_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
    drop_invalid: bool = False,
) -> list[BuildingBillMaterialsSlimRecordBase]:
    """
    Build a list of BuildingBillMaterialsSlimRecordBase from a dataframe
    produced by bom_to_dataframe().

    If drop_invalid is True, lines that miss a required field are dropped
    and reported as E33 warnings.
    """
    bom_df = add_material_id_column_if_missing(bom_df)
    return horizontal_from_dataframe(
        bom_df,
        BuildingBillMaterialsSlimRecordBase,
        COMMON_CATEGORY_PROPERTIES["bom"]["name"],
        excluded_fields=BOM_EXCLUDED_FIELDS,
        document_translator=document_translator,
        findings=findings,
        drop_invalid=drop_invalid,
    )


def project_material_database_from_dataframe(
    project_material_database_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
) -> list[ProjectMaterialDatabaseBase]:
    """
    Build a list of ProjectMaterialDatabaseBase from a dataframe
    produced by the Project Material Database sheet.
    """
    return horizontal_from_dataframe(
        project_material_database_df,
        ProjectMaterialDatabaseBase,
        COMMON_CATEGORY_PROPERTIES["material_database"]["name"],
        document_translator=document_translator,
        findings=findings,
    )


def results_wide_from_dataframe(
    results_wide_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
) -> list[LCAResultsWideFullBase]:
    """
    Build a list of LCAResultsWideFullBase from a dataframe produced
    by results_wide_to_dataframe().
    """
    results_wide_df = add_material_id_column_if_missing(results_wide_df)
    return horizontal_from_dataframe(
        results_wide_df,
        LCAResultsWideFullBase,
        COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
        findings=findings,
    )


def results_tall_from_dataframe(
    results_tall_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
) -> list[LCAResultsTallBase]:
    """
    Build a list of LCAResultsTallBase from a dataframe produced
    by results_tall_to_dataframe().
    """
    return horizontal_from_dataframe(
        results_tall_df,
        LCAResultsTallBase,
        COMMON_CATEGORY_PROPERTIES["results_tall"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
        findings=findings,
    )


def project_package_to_dataframes(
    project: ProjectRecord,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert a full ProjectRecord package into:
    - project dataframe
    - bill of materials dataframe
    """
    project_df = project_to_dataframe(project)
    bom_df = bom_to_dataframe(project.bill_of_materials or [])
    return project_df, bom_df


def project_package_from_tables(
    tables: OpenBDFTables,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
    draft: bool = False,
    drop_invalid: bool = False,
) -> ProjectRecord:
    """
    Reconstruct a ProjectRecord and attach its bill of materials from logical tables.

    In draft mode a missing project material database line is generated from the bill
    of materials and the automatic fields are recomputed. Every record is validated
    and its findings are added to the findings list, so the caller can report all of
    them and decide whether to export the file.

    If drop_invalid is True, bill of materials lines that miss a required
    field are dropped and a message is printed for each dropped line.
    """

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()
    if findings is None:
        findings = []

    project_base = project_from_dataframe(tables.project, document_translator, findings=findings)
    bill_of_materials_base = bom_from_dataframe(
        tables.bill_of_materials,
        document_translator,
        findings=findings,
        drop_invalid=drop_invalid,
    )

    project_material_database_base = (
        project_material_database_from_dataframe(
            tables.project_material_database,
            document_translator,
            findings=findings,
        )
        if tables.project_material_database is not None
        else []
    )
    if draft:
        project_material_database_base = _merge_project_material_database_draft(
            bill_of_materials_base,
            project_material_database_base,
        )

    project_material_database = [
        ProjectMaterialDatabaseRecord(**record.model_dump()) for record in project_material_database_base
    ]
    bill_of_materials = [BuildingBillMaterialsSlimRecord(**bom.model_dump()) for bom in bill_of_materials_base]

    material_id_to_bom = {bom.material_id: bom for bom in bill_of_materials}

    results_wide: list[LCAResultsWideFullRecord] = []
    results_tall: list[LCAResultsTallFullRecord] = []

    if tables.results_wide is not None:
        results_wide = [
            LCAResultsWideFullRecord(**record.model_dump())
            for record in results_wide_from_dataframe(tables.results_wide, document_translator, findings=findings)
        ]
        for result_wide in results_wide:
            matching_bom = material_id_to_bom.get(result_wide.material_id, None)
            if matching_bom is not None:
                matching_bom.lca_results_full_record = result_wide

    if tables.results_tall is not None:
        results_tall = [
            LCAResultsTallFullRecord(**record.model_dump())
            for record in results_tall_from_dataframe(tables.results_tall, document_translator, findings=findings)
        ]
        for result_tall in results_tall:
            matching_bom = material_id_to_bom.get(result_tall.material_id, None)
            if matching_bom is not None:
                matching_bom.lca_results_tall_full_records.append(result_tall)
    elif results_wide:
        results_tall = []
        for result_wide in results_wide:
            matching_bom = material_id_to_bom.get(result_wide.material_id, None)
            if matching_bom is not None:
                tall_results = lca_results_wide_to_tall(
                    result_wide,
                    matching_bom,
                    LCAResultsTallFullRecord,
                )
                matching_bom.lca_results_tall_full_records.extend(tall_results)
                results_tall.extend(tall_results)

    project = ProjectRecord(
        **project_base.model_dump(),
        bill_of_materials=bill_of_materials,
        project_material_database=project_material_database,
        results_wide=results_wide,
        results_tall=results_tall,
    )

    return project
