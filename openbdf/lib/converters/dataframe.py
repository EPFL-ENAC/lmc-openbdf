from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional, Union, cast, get_args, get_origin

import pandas as pd
from model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from model.enums.openbdf_enum import OpenBDFEnum
from model.general_info import ProjectRecordBase
from model.tables import BuildingBillMaterialsSlimRecord, ProjectRecord
from sqlmodel import SQLModel

PROJECT_EXCLUDED_FIELDS = {"id", "bill_of_materials"}
BOM_EXCLUDED_FIELDS = {"id", "project_id", "project"}

VALUE_ALIASES = {
    "yes": True,
    "no": False,
    "true": True,
    "false": False,
    "..": None,
    "N/A": None,
    "n/a": None,
    "null": None,
    "NULL": None,
    "none": None,
    "None": None,
    "-": None,
}


def unwrap_optional(annotation: Any) -> Any:
    """
    Convert Optional[T] / Union[T, None] to T.
    """
    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def field_metadata(field_info: Any) -> dict[str, Any]:
    """
    Return json schema extra / schema extra metadata from a field.
    """
    return getattr(field_info, "json_schema_extra", None) or {}


def get_field_code(field_name: str, field_info: Any) -> str:
    """
    Prefer the metadata field_code when available, else fallback to field name.
    """
    meta = field_metadata(field_info)
    return meta.get("field_code", field_name)


def get_attribute_name(field_name: str, field_info: Any) -> str:
    """
    Prefer the metadata attribute_name when available, else fallback to field name.
    """
    meta = field_metadata(field_info)
    return meta.get("attribute_name", field_name)


def serialize_value(value: Any) -> Any:
    """
    Convert Python values into dataframe-safe scalar values.
    """
    if value is None:
        return None

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    return value


def parse_enum(enum_cls: type[Enum], raw_value: Any) -> Enum:
    """
    Parse an enum from either its .value or .name.
    """
    if issubclass(enum_cls, OpenBDFEnum):
        openbdf_cls = cast(type[OpenBDFEnum], enum_cls)
        found = openbdf_cls.find_value(raw_value)
        if found is not None:
            return found

    for member in enum_cls:
        if raw_value == member.value or raw_value == member.name:
            return member

    raise ValueError(f"Invalid enum value {raw_value!r} for enum {enum_cls.__name__}")


def parse_value(annotation: Any, raw_value: Any) -> Any:
    """
    Convert dataframe scalar values back into typed Python values.
    """

    if isinstance(raw_value, str):
        raw_value = raw_value.strip()
        if raw_value in VALUE_ALIASES:
            return VALUE_ALIASES[raw_value]

    if raw_value is None:
        return None

    if pd.isna(raw_value):
        return None

    if isinstance(raw_value, str) and raw_value.strip() == "":
        return None

    annotation = unwrap_optional(annotation)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return parse_enum(annotation, raw_value)

    if annotation is Decimal:
        return Decimal(str(raw_value))

    if annotation is int:
        return int(raw_value)

    if annotation is float:
        return float(raw_value)

    if annotation is str:
        return str(raw_value)

    if annotation is bool:
        if isinstance(raw_value, bool):
            return raw_value
        return str(raw_value).strip().lower() in {"1", "true", "yes"}

    if annotation is date:
        if isinstance(raw_value, datetime):
            return raw_value.date()
        if isinstance(raw_value, date):
            return raw_value
        return date.fromisoformat(str(raw_value))

    if annotation is datetime:
        if isinstance(raw_value, datetime):
            return raw_value
        return datetime.fromisoformat(str(raw_value))

    return raw_value


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


def project_to_dataframe(project: ProjectRecord) -> pd.DataFrame:
    """
    Convert a ProjectRecord into a dataframe with one row per attribute.

    Output columns:
    - field_code
    - field_name
    - attribute_name
    - value
    """
    rows: list[dict[str, Any]] = []
    fields = ProjectRecord.model_fields

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


def project_from_dataframe(project_df: pd.DataFrame) -> ProjectRecordBase:
    """
    Build a ProjectRecordBase from a dataframe produced by project_to_dataframe().

    Expected columns:
    - field_code
    - value

    Extra columns are ignored.
    """
    required_columns = {"field_code", "value"}
    missing = required_columns - set(project_df.columns)
    if missing:
        raise ValueError(f"Project dataframe is missing required columns: {sorted(missing)}")

    fields = ProjectRecordBase.model_fields
    code_to_name = build_field_code_to_name_map(
        ProjectRecordBase,
        excluded_fields=PROJECT_EXCLUDED_FIELDS,
    )

    kwargs: dict[str, Any] = {}

    for _, row in project_df.iterrows():
        field_code = row["field_code"]

        if pd.isna(field_code):
            continue

        field_code = str(field_code)
        field_name = code_to_name.get(field_code)
        if field_name is None:
            continue

        field_info = fields[field_name]
        annotation = field_info.annotation
        kwargs[field_name] = parse_value(annotation, row["value"])

    return ProjectRecordBase(**kwargs)


def bom_from_dataframe(bom_df: pd.DataFrame) -> list[BuildingBillMaterialsSlimRecordBase]:
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
            field_name = code_to_name.get(str(column))
            if field_name is None:
                continue

            field_info = fields[field_name]
            annotation = field_info.annotation
            kwargs[field_name] = parse_value(annotation, row[column])

        if any(value is not None for value in kwargs.values()):
            # we skip completely empty rows to avoid creating empty records
            items.append(BuildingBillMaterialsSlimRecordBase(**kwargs))

    return items


def project_package_to_dataframes(
    project: ProjectRecordBase,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert a full ProjectRecordBase package into:
    - project dataframe
    - bill of materials dataframe
    """
    project_df = project_to_dataframe(project)
    bom_df = bom_to_dataframe(project.bill_of_materials or [])
    return project_df, bom_df


def project_package_from_dataframes(
    project_df: pd.DataFrame,
    bom_df: pd.DataFrame,
) -> ProjectRecord:
    """
    Reconstruct a ProjectRecordBase and attach its bill_of_materials from dataframes.
    """

    project_base = project_from_dataframe(project_df)
    bill_of_materials_base = bom_from_dataframe(bom_df)

    project = ProjectRecord(
        **project_base.model_dump(),
        bill_of_materials=[BuildingBillMaterialsSlimRecord(**bom.model_dump()) for bom in bill_of_materials_base],
    )

    return project
