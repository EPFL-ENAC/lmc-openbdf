from datetime import date, datetime
from types import NoneType, UnionType
from typing import Any, Union, get_args, get_origin

from openpyxl.worksheet.datavalidation import DataValidation

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


def get_display_type(type: Any) -> str:
    return getattr(type, "__name__", str(type))


def xlsx_validation_from_type(
    data_type: Any, is_optional: bool, metadata: Any, enum_registry: EnumRegistry
) -> DataValidation | None:
    if isinstance(data_type, type) and issubclass(data_type, OpenBDFEnum):
        return DataValidation(
            type="list",
            formula1=enum_registry.get_validation_formula(data_type),
            allow_blank=is_optional,
        )
    elif data_type == int:
        return DataValidation(type="whole", allow_blank=is_optional)
    elif data_type == float:
        return DataValidation(type="decimal", allow_blank=is_optional)
    elif data_type == bool:
        return DataValidation(
            type="list",
            formula1='"True,False"',
            allow_blank=is_optional,
        )
    elif data_type == str:
        if hasattr(metadata, "max_length") and metadata.max_length:
            return DataValidation(
                type="textLength", operator="lessThanOrEqual", formula1=metadata.max_length, allow_blank=is_optional
            )
    elif data_type in (date, datetime):
        # Look for min/max dates in metadata if they exist
        start = getattr(metadata, "min_date", "1900-01-01")
        end = getattr(metadata, "max_date", None)

        if end:
            return DataValidation(
                type="date",
                operator="between",
                formula1=start,
                formula2=end,
                allow_blank=is_optional,
            )
        return DataValidation(
            type="date",
            operator="greaterThanOrEqual",
            formula1=start,
            allow_blank=is_optional,
        )

    return None
