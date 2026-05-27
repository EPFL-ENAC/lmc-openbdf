from __future__ import annotations

from typing import Any, Optional, TypeVar

import pandas as pd
from sqlmodel import SQLModel

from openbdf.lib.converters.attribute_translator import COMMON_CATEGORY_NAMES, DocumentTranslator
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.types.values import parse_value, serialize_value
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.general_info import ProjectRecordBase, ProjectRecordBaseDraft
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    BuildingBillMaterialsSlimRecordDraft,
    ProjectRecord,
    ProjectRecordDraft,
)

PROJECT_EXCLUDED_FIELDS = {"id", "bill_of_materials"}
BOM_EXCLUDED_FIELDS = {"id", "project_id", "project"}


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


def wide_to_dataframe(
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


def model_from_vertical_dataframe(
    project_df: pd.DataFrame,
    model_cls: type[ModelT],
    excluded_fields: set[str] | None = None,
    translator_category: str = COMMON_CATEGORY_NAMES["project"],
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
        document_translator = DocumentTranslator()

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

        field_code = document_translator.translate(
            translator_category,
            str(field_code),
        )
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

    return model_cls(**kwargs)


def project_from_dataframe(
    project_df: pd.DataFrame, document_translator: DocumentTranslator = DocumentTranslator()
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
        translator_category=COMMON_CATEGORY_NAMES["project"],
        document_translator=document_translator,
    )


def project_draft_from_dataframe(
    project_df: pd.DataFrame, document_translator: DocumentTranslator = DocumentTranslator()
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
        translator_category=COMMON_CATEGORY_NAMES["project"],
        document_translator=document_translator,
    )


def bom_from_dataframe(
    bom_df: pd.DataFrame, document_translator: DocumentTranslator = DocumentTranslator()
) -> list[BuildingBillMaterialsSlimRecordBase]:
    """
    Build a list of BuildingBillMaterialsSlimRecord from a dataframe produced
    by bom_to_dataframe().

    Dataframe columns are interpreted as field_code values.
    Unknown columns are ignored.
    """
    fields = BuildingBillMaterialsSlimRecordBase.model_fields
    code_to_name = build_field_code_to_name_map(
        BuildingBillMaterialsSlimRecordBase,
        excluded_fields=BOM_EXCLUDED_FIELDS,
    )

    items: list[BuildingBillMaterialsSlimRecordBase] = []

    for _, row in bom_df.iterrows():
        kwargs: dict[str, Any] = {}

        for column in bom_df.columns.tolist():
            field_name = code_to_name.get(document_translator.translate(COMMON_CATEGORY_NAMES["bom"], str(column)))
            if field_name is None:
                continue

            field_info = fields[field_name]
            annotation = field_info.annotation
            kwargs[field_name] = parse_value(annotation, row[column], document_translator)

        if any(value is not None for value in kwargs.values()):
            # we skip completely empty rows to avoid creating empty records
            items.append(BuildingBillMaterialsSlimRecordBase(**kwargs))

    return items


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


def project_package_from_dataframes(
    project_df: pd.DataFrame,
    bom_df: pd.DataFrame,
    document_translator: DocumentTranslator | None = None,
) -> ProjectRecord:
    """
    Reconstruct a ProjectRecord and attach its bill_of_materials from dataframes.
    """

    if document_translator is None:
        document_translator = DocumentTranslator()

    project_base = project_from_dataframe(project_df, document_translator)
    bill_of_materials_base = bom_from_dataframe(bom_df, document_translator)

    project = ProjectRecord(
        **project_base.model_dump(),
        bill_of_materials=[BuildingBillMaterialsSlimRecord(**bom.model_dump()) for bom in bill_of_materials_base],
    )

    return project


def project_draft_package_from_dataframes(
    project_df: pd.DataFrame | None,
    bom_df: pd.DataFrame | None,
    document_translator: DocumentTranslator | None = None,
) -> ProjectRecordDraft:
    """
    Reconstruct a ProjectRecordDraft and attach its bill_of_materials from dataframes.
    """

    if document_translator is None:
        document_translator = DocumentTranslator()

    project_base = (
        project_draft_from_dataframe(project_df, document_translator)
        if project_df is not None
        else ProjectRecordBaseDraft()
    )
    bill_of_materials_base = bom_from_dataframe(bom_df, document_translator) if bom_df is not None else []

    project_draft = ProjectRecordDraft(
        **project_base.model_dump(),
        bill_of_materials=[BuildingBillMaterialsSlimRecordDraft(**bom.model_dump()) for bom in bill_of_materials_base],
    )

    return project_draft
