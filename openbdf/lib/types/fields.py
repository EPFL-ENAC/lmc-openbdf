from typing import Any

from pydantic.fields import FieldInfo as PydanticFieldInfo
from sqlmodel.main import FieldInfo as SQLModelFieldInfo


def field_metadata(field_info: SQLModelFieldInfo | PydanticFieldInfo) -> dict[str, Any]:
    """
    Return json schema extra / schema extra metadata from a field.
    """
    return getattr(field_info, "json_schema_extra", None) or {}


def get_field_code(field_name: str, field_info: SQLModelFieldInfo | PydanticFieldInfo) -> str:
    """
    Prefer the metadata field_code when available, else fallback to field name.
    """
    meta = field_metadata(field_info)
    return meta.get("field_code", field_name)


def get_attribute_name(field_name: str, field_info: SQLModelFieldInfo | PydanticFieldInfo) -> str:
    """
    Prefer the metadata attribute_name when available, else fallback to field name.
    """
    meta = field_metadata(field_info)
    return meta.get("attribute_name", field_name)
