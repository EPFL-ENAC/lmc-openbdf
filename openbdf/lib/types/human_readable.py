from datetime import date, datetime
from typing import Any

import annotated_types
from pydantic.fields import FieldInfo as PydanticFieldInfo
from sqlmodel.main import FieldInfo as SQLModelFieldInfo

_TYPE_TO_HUMAN_READABLE: dict[Any, str] = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "Boolean",
    date: "date",
    datetime: "datetime",
}


def human_readable_type(type: Any) -> str:
    return _TYPE_TO_HUMAN_READABLE.get(type, getattr(type, "__name__", str(type)))


def human_readable_constraints(field: SQLModelFieldInfo | PydanticFieldInfo) -> str:
    constraints = []

    metadata = getattr(field, "metadata", []) or []

    min_len = None
    max_len = None
    ge = None
    gt = None
    le = None
    lt = None

    for item in metadata:
        if isinstance(item, annotated_types.Len):
            min_len = item.min_length
            max_len = item.max_length
        elif isinstance(item, annotated_types.MaxLen):
            max_len = item.max_length
        elif isinstance(item, annotated_types.MinLen):
            min_len = item.min_length
        elif isinstance(item, annotated_types.Ge):
            ge = item.ge
        elif isinstance(item, annotated_types.Gt):
            gt = item.gt
        elif isinstance(item, annotated_types.Le):
            le = item.le
        elif isinstance(item, annotated_types.Lt):
            lt = item.lt

    if max_len is not None:
        constraints.append(f"max {max_len} characters")
    if min_len is not None:
        constraints.append(f"min {min_len} characters")

    if le is not None:
        constraints.append(f"≤ {le}")
    elif lt is not None:
        constraints.append(f"< {lt}")

    if ge is not None:
        constraints.append(f"≥ {ge}")
    elif gt is not None:
        constraints.append(f"> {gt}")

    return ", ".join(constraints) if constraints else ""
