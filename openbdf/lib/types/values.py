from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, cast

import pandas as pd

from openbdf.lib.converters.translators import DocumentTranslator
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.model.enums.openbdf_enum import OpenBDFEnum

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


def parse_enum(enum_cls: type[Enum], raw_value: Any, translator: DocumentTranslator | None = None) -> Enum:
    """
    Parse an enum from either its .value or .name.
    """
    if issubclass(enum_cls, OpenBDFEnum):
        openbdf_cls = cast(type[OpenBDFEnum], enum_cls)
        found = openbdf_cls.find_value(raw_value, translator)
        if found is not None:
            return found

    for member in enum_cls:
        if raw_value == member.value or raw_value == member.name:
            return member

    raise ValueError(f"Invalid enum value {raw_value!r} for enum {enum_cls.__name__}")


def parse_value(annotation: Any, raw_value: Any, translator: DocumentTranslator | None = None) -> Any:
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

    (annotation, _) = unwrap_optional(annotation)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return parse_enum(annotation, raw_value, translator)

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
        try:
            return date.fromisoformat(str(raw_value))
        except ValueError:
            pass
        return date(year=int(raw_value), month=1, day=1)

    if annotation is datetime:
        if isinstance(raw_value, datetime):
            return raw_value
        return datetime.fromisoformat(str(raw_value))

    return raw_value


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
