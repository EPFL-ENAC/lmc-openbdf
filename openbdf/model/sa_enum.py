from sqlalchemy import Enum as SAEnum

from openbdf.model.enums.openbdf_enum import OpenBDFEnum


def sa_enum(enum_cls: type[OpenBDFEnum]) -> SAEnum:
    """Column type that persists an OpenBDFEnum by value, not by member name."""
    return SAEnum(
        enum_cls,
        native_enum=False,
        values_callable=lambda cls: [member.value for member in cls],
    )
