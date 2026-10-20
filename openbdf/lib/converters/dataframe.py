from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional, TypeVar

import pandas as pd
from sqlmodel import SQLModel

from openbdf.lib.converters.lca_results import lca_results_wide_to_tall
from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator, PreprocessRule
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.types.values import parse_value, serialize_value
from openbdf.model.building_bill_materials_slim import (
    BuildingBillMaterialsSlimRecordBase,
    BuildingBillMaterialsSlimRecordBaseDraft,
)
from openbdf.model.general_info import ProjectRecordBase, ProjectRecordBaseDraft
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase, ProjectMaterialDatabaseBaseDraft
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    BuildingBillMaterialsSlimRecordDraft,
    LCAResultsTallFullRecord,
    LCAResultsTallFullRecordDraft,
    LCAResultsWideFullRecord,
    LCAResultsWideFullRecordDraft,
    ProjectMaterialDatabaseRecord,
    ProjectMaterialDatabaseRecordDraft,
    ProjectRecord,
    ProjectRecordDraft,
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


def horizontal_from_dataframe(
    df: pd.DataFrame,
    model_cls: type[ModelT],
    translator_category: str,
    *,
    excluded_fields: set[str] | None = None,
    document_translator: DocumentTranslator | None = None,
    drop_invalid: bool = False,
    required_model_cls: type[SQLModel] | None = None,
) -> list[ModelT]:
    """
    Build a list of model instances from a horizontal dataframe.

    Dataframe columns are interpreted as field_code values.
    Unknown columns are ignored.

    If drop_invalid is True and required_model_cls is given, the required
    fields of required_model_cls are derived with is_required(). Rows that
    miss a required field are not kept and a message is printed to the
    terminal for each dropped row.
    """
    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()

    fields = model_cls.model_fields
    code_to_name = build_field_code_to_name_map(
        model_cls,
        excluded_fields=excluded_fields,
    )

    required_names: set[str] = set()
    if drop_invalid and required_model_cls is not None:
        for req_field, field_info in required_model_cls.model_fields.items():
            if field_info.is_required():
                required_names.add(req_field)

    # The column set is fixed for all rows, so translation, field resolution
    # and default parsing run once instead of once per row.
    column_plans: list[list[tuple[str, Any, PreprocessRule | None]]] = []
    for column in df.columns:
        column_plan: list[tuple[str, Any, PreprocessRule | None]] = []
        for translated_code in document_translator.translate(translator_category, str(column)):
            field_name = code_to_name.get(translated_code)
            if field_name is None:
                continue
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

    for row_number, row_values in enumerate(df.itertuples(index=False, name=None), start=1):
        kwargs: dict[str, Any] = {}

        for column_plan, raw_cell in zip(column_plans, row_values):
            for field_name, annotation, preprocess_rule in column_plan:
                raw_value = raw_cell
                if preprocess_rule:
                    result = preprocess_rule.execute(raw_value)
                    if result.valid:
                        raw_value = result.value
                    else:
                        raw_value = None

                kwargs[field_name] = parse_value(
                    annotation,
                    raw_value,
                    document_translator,
                )

        for field_name, default_parsed in default_plans:
            if kwargs.get(field_name) is not None:
                continue
            kwargs[field_name] = default_parsed

        if not any(value is not None for value in kwargs.values()):
            continue

        if drop_invalid and required_names:
            missing = [name for name in required_names if kwargs.get(name) is None]
            if missing:
                material_id = kwargs.get("material_id")
                if material_id is not None:
                    identifier = f"material_id={material_id!r}"
                else:
                    identifier = f"row {row_number}"
                print(
                    f"Dropped bill of materials line ({identifier}): "
                    f"missing required field(s): {', '.join(sorted(missing))}."
                )
                continue

        items.append(model_cls(**kwargs))

    return items


def model_from_vertical_dataframe(
    project_df: pd.DataFrame,
    model_cls: type[ModelT],
    excluded_fields: set[str] | None = None,
    translator_category: str = COMMON_CATEGORY_PROPERTIES["project"]["name"],
    *,
    document_translator: DocumentTranslator | None = None,
) -> ModelT:
    """
    Build a project model from a dataframe produced by project_to_dataframe().

    Expected columns:
    - field_code
    - value

    Extra columns are ignored.
    """
    required_columns = {"field_code", "value"}
    missing = required_columns - set(project_df.columns)
    if missing:
        raise ValueError(f"Project dataframe is missing required columns: {sorted(missing)}")

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()

    fields = model_cls.model_fields
    code_to_name = build_field_code_to_name_map(
        model_cls,
        excluded_fields=excluded_fields,
    )

    kwargs: dict[str, Any] = {}

    for _, row in project_df.iterrows():
        field_code = row["field_code"]

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

            field_info = fields[field_name]
            annotation = field_info.annotation
            kwargs[field_name] = parse_value(
                annotation,
                row["value"],
                document_translator,
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

    return model_cls(**kwargs)


def project_from_dataframe(
    project_df: pd.DataFrame, document_translator: DocumentTranslator | None = None
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
    )


def project_draft_from_dataframe(
    project_df: pd.DataFrame, document_translator: DocumentTranslator | None = None
) -> ProjectRecordBaseDraft:
    """
    Build a ProjectRecordDraft from a dataframe produced by project_to_dataframe().

    Expected columns:
    - field_code
    - value

    Extra columns are ignored.
    """
    return model_from_vertical_dataframe(
        project_df,
        ProjectRecordBaseDraft,
        excluded_fields=PROJECT_EXCLUDED_FIELDS,
        translator_category=COMMON_CATEGORY_PROPERTIES["project"]["name"],
        document_translator=document_translator or DocumentTranslator(),
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


MaterialPair = tuple[str, str | None]


def _material_ref_id_number(material_ref_id: str | None) -> int:
    """Return the numeric suffix of an M%d material_ref_id, or 0."""
    if material_ref_id and material_ref_id.startswith("M") and material_ref_id[1:].isdigit():
        return int(material_ref_id[1:])
    return 0


def _material_pair(
    custom_material_name: str | None,
    lca_dataset_material_name: str | None,
) -> MaterialPair | None:
    """
    Return the normalized pair that identifies a material, or None when it has no name.
    Names and EPD dataset names compare without surrounding spaces and without case,
    and a missing EPD dataset is the same as a blank one.
    """
    name = (custom_material_name or "").strip().casefold()
    if not name:
        return None
    return name, (lca_dataset_material_name or "").strip().casefold() or None


def _material_pair_label(record: Any) -> str:
    """Describe a material pair as written in the workbook, for a finding."""
    name = (record.custom_material_name or "").strip()
    dataset = (record.lca_dataset_material_name or "").strip()
    return f"{name!r} with EPD dataset {dataset!r}" if dataset else f"{name!r} without an EPD dataset"


def _group_by_material_pair(records: list[Any]) -> dict[MaterialPair, list[Any]]:
    """Group records by material pair and drop the records that carry no material name."""
    grouped: dict[MaterialPair, list[Any]] = {}
    for record in records:
        pair = _material_pair(record.custom_material_name, record.lca_dataset_material_name)
        if pair is not None:
            grouped.setdefault(pair, []).append(record)
    return grouped


def _first_text(records: list[Any], field_name: str) -> str | None:
    """Return the first non-blank value of a text field, without its surrounding spaces."""
    for record in records:
        value = (getattr(record, field_name) or "").strip()
        if value:
            return value
    return None


def _bom_row_mass(row: BuildingBillMaterialsSlimRecordBaseDraft) -> Decimal:
    """Return the mass a bill of materials row contributes, repeated once per floor unless stated."""
    repetitions = 1 if row.floor_repetition is None else row.floor_repetition
    return (row.material_weight_kg or Decimal(0)) * repetitions


def _validate_project_material_database_against_bom(
    bill_of_materials: list[BuildingBillMaterialsSlimRecordBase],
    project_material_database: list[ProjectMaterialDatabaseBase],
) -> None:
    """
    Check the project material database lines against the bill of materials and
    raise a ValueError naming every mismatch. A material is the pair of its name
    and its EPD dataset name.
    """
    bom_rows_by_pair = _group_by_material_pair(bill_of_materials)
    pmd_lines_by_pair = _group_by_material_pair(project_material_database)

    findings: list[str] = []

    orphan_labels = [
        _material_pair_label(pmd_lines_by_pair[pair][0]) for pair in pmd_lines_by_pair if pair not in bom_rows_by_pair
    ]
    if orphan_labels:
        findings.append(f"project material database lines without a bill of materials material: {orphan_labels!r}")

    missing_labels = [
        _material_pair_label(bom_rows_by_pair[pair][0]) for pair in bom_rows_by_pair if pair not in pmd_lines_by_pair
    ]
    if missing_labels:
        findings.append(f"bill of materials materials without a project material database line: {missing_labels!r}")

    duplicate_labels = [
        _material_pair_label(lines[0])
        for pair, lines in pmd_lines_by_pair.items()
        if len(lines) > 1 and pair in bom_rows_by_pair
    ]
    if duplicate_labels:
        findings.append(
            f"bill of materials materials with more than one project material database line: {duplicate_labels!r}"
        )

    for pair, lines in pmd_lines_by_pair.items():
        if pair not in bom_rows_by_pair or len(lines) != 1:
            continue
        expected_ref_id = lines[0].material_ref_id
        wrong_ref_ids = list(
            dict.fromkeys(
                bom.material_ref_id
                for bom in bom_rows_by_pair[pair]
                if bom.material_ref_id and bom.material_ref_id != expected_ref_id
            )
        )
        if wrong_ref_ids:
            findings.append(
                f"bill of materials rows of material {_material_pair_label(lines[0])} carry material_ref_id values "
                f"that differ from the project material database material_ref_id {expected_ref_id!r}: {wrong_ref_ids!r}"
            )

    ref_id_counts: dict[str, int] = {}
    for pmd in project_material_database:
        ref_id_counts[pmd.material_ref_id] = ref_id_counts.get(pmd.material_ref_id, 0) + 1
    duplicate_ref_ids = [ref_id for ref_id, count in ref_id_counts.items() if count > 1]
    if duplicate_ref_ids:
        findings.append(
            f"project material database material_ref_id values used by more than one line: {duplicate_ref_ids!r}"
        )

    if findings:
        raise ValueError("The project material database does not match the bill of materials: " + "; ".join(findings))


def _merge_project_material_database_draft(
    bill_of_materials: list[BuildingBillMaterialsSlimRecordBaseDraft],
    project_material_database: list[ProjectMaterialDatabaseBaseDraft],
) -> list[ProjectMaterialDatabaseBaseDraft]:
    """
    Merge the parsed project material database lines with the bill of materials.
    A material is the pair of its name and its EPD dataset name. Every bill of
    materials pair without a line gets a generated one, the automatic fields of
    every line are recomputed from its rows, and the rows are back-filled with the
    line's material_ref_id. A line without bill of materials rows is kept and its
    automatic fields count zero.
    """
    bom_rows_by_pair = _group_by_material_pair(bill_of_materials)

    first_line_by_pair: dict[MaterialPair, ProjectMaterialDatabaseBaseDraft] = {}
    for pmd in project_material_database:
        pair = _material_pair(pmd.custom_material_name, pmd.lca_dataset_material_name)
        if pair is not None:
            first_line_by_pair.setdefault(pair, pmd)

    ref_id_records: list[ProjectMaterialDatabaseBaseDraft | BuildingBillMaterialsSlimRecordBaseDraft] = [
        *project_material_database,
        *bill_of_materials,
    ]
    highest_ref_id = max(
        (_material_ref_id_number(record.material_ref_id) for record in ref_id_records),
        default=0,
    )

    generated_by_pair: dict[MaterialPair, ProjectMaterialDatabaseBaseDraft] = {}
    for pair, bom_rows in bom_rows_by_pair.items():
        if pair in first_line_by_pair:
            continue
        highest_ref_id += 1
        generated_by_pair[pair] = ProjectMaterialDatabaseBaseDraft(
            custom_material_name=_first_text(bom_rows, "custom_material_name"),
            lca_dataset_material_name=_first_text(bom_rows, "lca_dataset_material_name"),
            lca_database_name=_first_text(bom_rows, "lca_database_name"),
            material_ref_id=f"M{highest_ref_id:04d}",
        )

    total_mass = sum(_bom_row_mass(row) for bom_rows in bom_rows_by_pair.values() for row in bom_rows)
    for pair, bom_rows in bom_rows_by_pair.items():
        line = first_line_by_pair.get(pair) or generated_by_pair[pair]
        line_mass = sum(_bom_row_mass(row) for row in bom_rows)
        line.bom_row_count = len(bom_rows)
        line.material_mass_kg = line_mass
        line.material_mass_share = line_mass / total_mass * 100 if total_mass else Decimal(0)
        for row in bom_rows:
            row.material_ref_id = line.material_ref_id

    for pmd in project_material_database:
        pair = _material_pair(pmd.custom_material_name, pmd.lca_dataset_material_name)
        if pair is None or pair not in bom_rows_by_pair:
            pmd.bom_row_count = 0
            pmd.material_mass_kg = Decimal(0)
            pmd.material_mass_share = Decimal(0)

    return [*project_material_database, *generated_by_pair.values()]


def bom_from_dataframe(
    bom_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    drop_invalid: bool = False,
) -> list[BuildingBillMaterialsSlimRecordBase]:
    """
    Build a list of BuildingBillMaterialsSlimRecordBase from a dataframe
    produced by bom_to_dataframe().

    If drop_invalid is True, lines that miss a required field are dropped
    and a message is printed for each dropped line.
    """
    bom_df = add_material_id_column_if_missing(bom_df)
    return horizontal_from_dataframe(
        bom_df,
        BuildingBillMaterialsSlimRecordBase,
        COMMON_CATEGORY_PROPERTIES["bom"]["name"],
        excluded_fields=BOM_EXCLUDED_FIELDS,
        document_translator=document_translator,
        drop_invalid=drop_invalid,
        required_model_cls=BuildingBillMaterialsSlimRecordBase,
    )


def bom_draft_from_dataframe(
    bom_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
    *,
    drop_invalid: bool = False,
) -> list[BuildingBillMaterialsSlimRecordBaseDraft]:
    """
    Build a list of BuildingBillMaterialsSlimRecordBaseDraft from a dataframe
    produced by bom_to_dataframe().

    If drop_invalid is True, lines that miss a required field are dropped
    and a message is printed for each dropped line.
    """
    bom_df = add_material_id_column_if_missing(bom_df)
    return horizontal_from_dataframe(
        bom_df,
        BuildingBillMaterialsSlimRecordBaseDraft,
        COMMON_CATEGORY_PROPERTIES["bom"]["name"],
        excluded_fields=BOM_EXCLUDED_FIELDS,
        document_translator=document_translator,
        drop_invalid=drop_invalid,
        required_model_cls=BuildingBillMaterialsSlimRecordBase,
    )


def project_material_database_from_dataframe(
    project_material_database_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
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
    )


def project_material_database_draft_from_dataframe(
    project_material_database_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> list[ProjectMaterialDatabaseBaseDraft]:
    """
    Build a list of ProjectMaterialDatabaseBaseDraft from a dataframe
    produced by the Project Material Database sheet.
    """
    return horizontal_from_dataframe(
        project_material_database_df,
        ProjectMaterialDatabaseBaseDraft,
        COMMON_CATEGORY_PROPERTIES["material_database"]["name"],
        document_translator=document_translator,
    )


def _require_project_material_database(project_material_database_df: pd.DataFrame | None) -> pd.DataFrame:
    """Return the project material database of a strict record, which must be present."""
    if project_material_database_df is None:
        raise ValueError(
            "The Project Material Database sheet is missing from the source workbook; "
            "add it, or open the workbook in draft mode."
        )
    return project_material_database_df


def results_wide_from_dataframe(
    results_wide_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> list[LCAResultsWideFullRecord]:
    """
    Build a list of LCAResultsWideFullRecord from a dataframe produced
    by results_wide_to_dataframe().
    """
    results_wide_df = add_material_id_column_if_missing(results_wide_df)
    return horizontal_from_dataframe(
        results_wide_df,
        LCAResultsWideFullRecord,
        COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
    )


def results_wide_draft_from_dataframe(
    results_wide_draft_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> list[LCAResultsWideFullRecordDraft]:
    """
    Build a list of LCAResultsWideFullRecordDraft from a dataframe produced
    by results_wide_to_dataframe().
    """
    results_wide_draft_df = add_material_id_column_if_missing(results_wide_draft_df)
    return horizontal_from_dataframe(
        results_wide_draft_df,
        LCAResultsWideFullRecordDraft,
        COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
    )


def results_tall_from_dataframe(
    results_tall_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> list[LCAResultsTallFullRecord]:
    """
    Build a list of LCAResultsTallFullRecord from a dataframe produced
    by results_tall_to_dataframe().
    """
    return horizontal_from_dataframe(
        results_tall_df,
        LCAResultsTallFullRecord,
        COMMON_CATEGORY_PROPERTIES["results_tall"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
    )


def results_tall_draft_from_dataframe(
    results_tall_draft_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> list[LCAResultsTallFullRecordDraft]:
    """
    Build a list of LCAResultsTallFullRecordDraft from a dataframe produced
    by results_tall_to_dataframe().
    """
    return horizontal_from_dataframe(
        results_tall_draft_df,
        LCAResultsTallFullRecordDraft,
        COMMON_CATEGORY_PROPERTIES["results_tall"]["name"],
        excluded_fields=RESULTS_EXCLUDED_FIELDS,
        document_translator=document_translator,
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
    drop_invalid: bool = False,
) -> ProjectRecord:
    """
    Reconstruct a ProjectRecord and attach its bill of materials from logical tables.

    If drop_invalid is True, bill of materials lines that miss a required
    field are dropped and a message is printed for each dropped line.
    """

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()

    project_base = project_from_dataframe(tables.project, document_translator)
    bill_of_materials_base = bom_from_dataframe(
        tables.bill_of_materials,
        document_translator,
        drop_invalid=drop_invalid,
    )

    bill_of_materials = [BuildingBillMaterialsSlimRecord(**bom.model_dump()) for bom in bill_of_materials_base]

    project_material_database_base = project_material_database_from_dataframe(
        _require_project_material_database(tables.project_material_database),
        document_translator,
    )
    project_material_database = [
        ProjectMaterialDatabaseRecord(**record.model_dump()) for record in project_material_database_base
    ]

    _validate_project_material_database_against_bom(bill_of_materials_base, project_material_database_base)

    material_id_to_bom = {bom.material_id: bom for bom in bill_of_materials}

    results_wide: list[LCAResultsWideFullRecord] = []
    results_tall: list[LCAResultsTallFullRecord] = []

    if tables.results_wide is not None:
        results_wide = results_wide_from_dataframe(tables.results_wide, document_translator)
        for result_wide in results_wide:
            matching_bom = material_id_to_bom.get(result_wide.material_id, None)
            if matching_bom is not None:
                matching_bom.lca_results_full_record = result_wide

    if tables.results_tall is not None:
        results_tall = results_tall_from_dataframe(tables.results_tall, document_translator)
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


def project_draft_package_from_tables(
    tables: OpenBDFTables,
    document_translator: DocumentTranslator | None = None,
    *,
    drop_invalid: bool = False,
) -> ProjectRecordDraft:
    """
    Reconstruct a ProjectRecordDraft and attach its bill of materials from logical tables.

    If drop_invalid is True, bill of materials lines that miss a required
    field are dropped and a message is printed for each dropped line.
    """

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()

    project_base = project_draft_from_dataframe(tables.project, document_translator)
    bill_of_materials_base = bom_draft_from_dataframe(
        tables.bill_of_materials,
        document_translator,
        drop_invalid=drop_invalid,
    )

    project_material_database_base = (
        project_material_database_draft_from_dataframe(tables.project_material_database, document_translator)
        if tables.project_material_database is not None
        else []
    )
    project_material_database = [
        ProjectMaterialDatabaseRecordDraft(**record.model_dump())
        for record in _merge_project_material_database_draft(
            bill_of_materials_base,
            project_material_database_base,
        )
    ]

    bill_of_materials = [BuildingBillMaterialsSlimRecordDraft(**bom.model_dump()) for bom in bill_of_materials_base]

    material_id_to_bom = {bom.material_id: bom for bom in bill_of_materials}

    results_wide: list[LCAResultsWideFullRecordDraft] = []
    results_tall: list[LCAResultsTallFullRecordDraft] = []

    if tables.results_wide is not None:
        results_wide = results_wide_draft_from_dataframe(tables.results_wide, document_translator)
        for result_wide in results_wide:
            matching_bom = material_id_to_bom.get(result_wide.material_id, None)
            if matching_bom is not None:
                matching_bom.lca_results_full_record = result_wide

    if tables.results_tall is not None:
        results_tall = results_tall_draft_from_dataframe(tables.results_tall, document_translator)
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
                    LCAResultsTallFullRecordDraft,
                )
                matching_bom.lca_results_tall_full_records.extend(tall_results)
                results_tall.extend(tall_results)

    project_draft = ProjectRecordDraft(
        **project_base.model_dump(),
        bill_of_materials=bill_of_materials,
        project_material_database=project_material_database,
        results_wide=results_wide,
        results_tall=results_tall,
    )

    return project_draft
