from datetime import date, datetime
from typing import Any

from openpyxl.worksheet.datavalidation import DataValidation
from sqlmodel.main import FieldInfo

from openbdf.lib.converters.enums_registry import Boolean, EnumRegistry
from openbdf.model.enums.openbdf_enum import OpenBDFEnum


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
            formula1=enum_registry.get_validation_formula(Boolean),
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
