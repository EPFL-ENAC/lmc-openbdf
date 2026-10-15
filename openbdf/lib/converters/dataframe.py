from __future__ import annotations

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
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    BuildingBillMaterialsSlimRecordDraft,
    LCAResultsTallFullRecord,
    LCAResultsTallFullRecordDraft,
    LCAResultsWideFullRecord,
    LCAResultsWideFullRecordDraft,
    ProjectMaterialDatabaseRecord,
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
        tables.project_material_database,
        document_translator,
    )
    project_material_database = [
        ProjectMaterialDatabaseRecord(**record.model_dump()) for record in project_material_database_base
    ]

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
        results_wide=results_wide,
        results_tall=results_tall,
    )

    return project_draft
