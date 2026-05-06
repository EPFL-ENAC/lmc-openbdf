from __future__ import annotations

from enum import Enum

from openbdf.lib.converters.attribute_translator import DocumentTranslator


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
    def find_value(cls, label: str, translator: DocumentTranslator | None) -> OpenBDFEnum | None:
        """
        Return the enum instance matching the value or display_name.
        """
        if translator:
            label = translator.translate(cls.__name__, label)

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
