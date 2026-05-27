from datetime import date, datetime
from types import NoneType, UnionType
from typing import Any, Union, get_args, get_origin

from openpyxl.worksheet.datavalidation import DataValidation
from sqlmodel.main import FieldInfo

from openbdf.lib.converters.enums_registry import EnumRegistry
from openbdf.model.enums.openbdf_enum import OpenBDFEnum


def unwrap_optional(annotation: Any) -> tuple[Any, bool]:
    """
    Takes a type annotation and returns the annotation stripped from the Optional if needed and True/False if it was an optional
    This function checks if the annotation is of the form Optional[T] (i.e., Union[T, None]) and returns T and a boolean indicating optionality.
    """
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Union, UnionType) and NoneType in args:
        non_none_args = [arg for arg in args if arg is not NoneType]
        if len(non_none_args) == 1:
            return non_none_args[0], True
    return annotation, False


_TYPE_TO_HUMAN_READABLE: dict[Any, str] = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "boolean",
    date: "date",
    datetime: "datetime",
}


def get_display_type(type: Any) -> str:
    return _TYPE_TO_HUMAN_READABLE.get(type, getattr(type, "__name__", str(type)))


from datetime import date, datetime
from typing import Any

import annotated_types


def human_readable_constraints(field: Any, data_type: Any) -> str:
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
        constraints.append(f"max {max_len} chars")
    if min_len is not None:
        constraints.append(f"min {min_len} chars")

    if le is not None:
        constraints.append(f"≤ {le}")
    elif lt is not None:
        constraints.append(f"< {lt}")

    if ge is not None:
        constraints.append(f"≥ {ge}")
    elif gt is not None:
        constraints.append(f"> {gt}")

    return ", ".join(constraints) if constraints else ""


def xlsx_validation_from_type(
    data_type: Any,
    is_optional: bool,
    metadata: FieldInfo,
    enum_registry: EnumRegistry,
) -> DataValidation | None:
    """
    Creates an openpyxl DataValidation object based on the type and
    Pydantic Field constraints.
    """
    dv_type = None
    operator = None
    f1, f2 = None, None

    # 1. Enums (Dropdowns)
    if isinstance(data_type, type) and issubclass(data_type, OpenBDFEnum):
        return DataValidation(
            type="list",
            formula1=enum_registry.get_validation_formula(data_type),
            allow_blank=is_optional,
        )

    # 2. Booleans
    elif data_type == bool:
        return DataValidation(
            type="list",
            formula1='"True,False"',
            allow_blank=is_optional,
        )

    # 3. Numeric Types (Int/Float)
    elif data_type in (int, float):
        dv_type = "whole" if data_type == int else "decimal"
        le = getattr(metadata, "le", None)
        lt = getattr(metadata, "lt", None)
        ge = getattr(metadata, "ge", None)
        gt = getattr(metadata, "gt", None)

        # Determine range operators
        if ge is not None and le is not None:
            operator, f1, f2 = "between", ge, le
        elif gt is not None and le is not None:
            # Excel doesn't support strict 'greater than' + 'less than or equal'
            # in one native UI rule perfectly, but 'between' is the closest fit.
            operator, f1, f2 = "between", gt, le
        elif ge is not None:
            operator, f1 = "greaterThanOrEqual", ge
        elif gt is not None:
            operator, f1 = "greaterThan", gt
        elif le is not None:
            operator, f1 = "lessThanOrEqual", le
        elif lt is not None:
            operator, f1 = "lessThan", lt

    # 4. Strings
    elif data_type == str:
        max_len = getattr(metadata, "max_length", None)
        min_len = getattr(metadata, "min_length", None)
        if max_len is not None or min_len is not None:
            dv_type = "textLength"
            if min_len and max_len:
                operator, f1, f2 = (
                    "between",
                    min_len,
                    max_len,
                )
            elif max_len:
                operator, f1 = "lessThanOrEqual", max_len
            elif min_len:
                operator, f1 = "greaterThanOrEqual", min_len

    # 5. Dates
    elif data_type in (date, datetime):
        dv_type = "date"
        # Checking for custom extra attributes often stored in Field.json_schema_extra
        start = getattr(metadata, "min_date", "1900-01-01")
        end = getattr(metadata, "max_date", None)

        if end:
            operator, f1, f2 = "between", start, end
        else:
            operator, f1 = "greaterThanOrEqual", start

    if dv_type:
        return DataValidation(
            type=dv_type,
            operator=operator,
            formula1=f1,
            formula2=f2,
            allow_blank=is_optional,
        )

    return None
