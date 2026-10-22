from dataclasses import dataclass

import pandas as pd
from openpyxl.utils import get_column_letter

from openbdf.model.enums.openbdf_enum import OpenBDFEnum


class Boolean(OpenBDFEnum):
    """
    Stand-in enum for bool fields so they share the Boolean column of the
    TypeDefinitions sheet instead of an inline validation list. Model fields
    stay annotated bool, so the database schema stores real booleans.
    """

    TRUE = ("TRUE", "TRUE")
    FALSE = ("FALSE", "FALSE")


@dataclass
class EnumRegistryEntry:
    enum_cls: type[OpenBDFEnum]
    column_letter: str
    column_index: int

    def validation_range(self, start_row: int = 3) -> str:
        return f"${self.column_letter}${start_row}:${self.column_letter}${len(self.enum_cls.choices()) + start_row - 1}"


class EnumRegistry:
    """
    A registry to keep track of all OpenBDFEnum subclasses and their members.
    This allows us to easily retrieve enum metadata (like display names) when generating Excel files.
    """

    _registry: dict[type[OpenBDFEnum], EnumRegistryEntry]
    _sheet_name: str = "TypeDefinitions"

    def __init__(self):
        self._registry = {}

    def register(self, *enum_classes: type[OpenBDFEnum]) -> None:
        """Pre-register types so the TypeDefinitions sheet has a fixed set of columns in a fixed order."""
        for enum_cls in enum_classes:
            self.get_entry(enum_cls)

    def get_entry(self, enum_cls: type[OpenBDFEnum]) -> EnumRegistryEntry:
        item = self._registry.get(enum_cls)
        if item is None:
            item = EnumRegistryEntry(
                enum_cls=enum_cls,
                column_letter=get_column_letter(len(self._registry) + 2),
                column_index=(len(self._registry) + 2),
            )  # Start from column B (2); column A holds the "Datatype Name" corner label
            self._registry[enum_cls] = item

        return item

    def get_validation_formula(self, enum_cls: type[OpenBDFEnum]) -> str:
        entry = self.get_entry(enum_cls)
        return f"{self._sheet_name}!{entry.validation_range(start_row=3)}"

    def to_xlsx(self, writer: pd.ExcelWriter):
        if not self._registry:
            return  # No enums to write

        sheet = writer.book.create_sheet(self._sheet_name)
        sheet.protection.sheet = True  # Lock the sheet to prevent accidental edits

        corner = sheet.cell(row=1, column=1, value="Datatype Name")
        corner.style = "AttributeName"
        sheet.column_dimensions["A"].width = 20

        # Row 2 holds the reference of each datatype, written by the enum classes themselves.
        reference_label = sheet.cell(row=2, column=1, value="Reference")
        reference_label.style = "AttributeName"

        for entry in self._registry.values():
            enum_cls = entry.enum_cls

            # Write the type name as a header
            header_cell = sheet.cell(row=1, column=entry.column_index, value=enum_cls.__name__)
            header_cell.style = "AttributeName"
            sheet.column_dimensions[entry.column_letter].width = max(
                (len(enum_cls.__name__) + 2) * 1.5, 20
            )  # Set column width based on header length

            # Write the members below, from row 3
            reference = getattr(enum_cls, "reference", None)
            reference_cell = sheet.cell(
                row=2, column=entry.column_index, value=reference.display_name if reference else ""
            )
            reference_cell.style = "Metadata"

            for idx, (_, display_name) in enumerate(enum_cls.choices(), start=3):
                member_cell = sheet.cell(row=idx, column=entry.column_index, value=display_name)
                member_cell.style = "Metadata"
