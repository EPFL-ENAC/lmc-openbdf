from enum import Enum
from typing import Optional


class OpenBDFEnum(str, Enum):
    display_name: str
    description: str | None
    parent_category: Optional["OpenBDFEnum"]

    def __new__(
        cls,
        value: str,
        display_name: str,
        description: str | None = None,
        parent_category: Optional["OpenBDFEnum"] = None,
    ):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.display_name = display_name
        obj.description = description
        obj.parent_category = parent_category
        return obj

    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.display_name) for item in cls]

    @classmethod
    def metadata(cls) -> list[dict[str, str | None]]:
        return [
            {
                "value": item.value,
                "display_name": item.display_name,
                "description": item.description,
                "parent_category": item.parent_category,
            }
            for item in cls
        ]
