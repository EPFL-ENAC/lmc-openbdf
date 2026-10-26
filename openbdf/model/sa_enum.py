from typing import Any

from sqlalchemy import Enum as SAEnum

from openbdf.model.enums.openbdf_enum import OpenBDFEnum


def sa_enum(enum_cls: type[OpenBDFEnum]) -> Any:
    """
    Return the column type that persists an OpenBDFEnum by value, not by member name.

    The value is an instance and not a class, so the return type is Any: SQLModel types
    the sa_type keyword as type[Any]. Narrow this when SQLModel widens that keyword.
    """
    return SAEnum(
        enum_cls,
        native_enum=False,
        values_callable=lambda cls: [member.value for member in cls],
    )
