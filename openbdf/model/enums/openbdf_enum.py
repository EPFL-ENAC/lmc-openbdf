from __future__ import annotations

from enum import Enum

from openbdf.lib.converters.translators import DocumentTranslator


class OpenBDFEnum(str, Enum):
    display_name: str
    description: str | None
    parent_category: OpenBDFEnum | None

    def __new__(
        cls,
        value: str,
        display_name: str,
        description: str | None = None,
        parent_category: OpenBDFEnum | None = None,
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
                "parent_category": item.parent_category.value if item.parent_category else None,
            }
            for item in cls
        ]

    @classmethod
    def is_valid(cls, label: str) -> bool:
        """
        Check if a string matches any value or display_name in the enum.
        """
        return any(
            label == item.value
            or label == item.name
            or str(label).lower() == item.display_name.lower()
            or str(label).lower() == f"{item.value} {item.display_name}".lower()
            or str(label).lower() == f"{item.value}: {item.description}".lower()
            for item in cls
        )

    @classmethod
    def find_value(cls, label: str, translator: DocumentTranslator | None = None) -> OpenBDFEnum | None:
        """
        Return the enum instance matching the value or display_name.
        """
        if translator:
            label = translator.translate(cls.__name__, label)[
                0
            ]  # Use the first translated name as enums are a one-to-one mapping

        for item in cls:
            if (
                label == item.value
                or label == item.name
                or str(label).lower() == item.display_name.lower()
                or str(label).lower() == f"{item.value} {item.display_name}".lower()
                or str(label).lower() == f"{item.value}: {item.description}".lower()
            ):
                return item

        return None


class enum_attribute:
    """
    Class-level value on an enum, without turning it into an enum member.

    A regular assignment inside an enum class body would create a new member.
    This class can be used to wrap values that describe an entire datatype.
    """

    def __init__(self, value: object):
        self.value = value

    def __get__(self, instance: object, owner: type) -> object:
        return self.value
