from openpyxl import load_workbook

from openbdf.cli.save import save_translator
from openbdf.lib.converters.translators import (
    COMMON_CATEGORY_PROPERTIES,
    SHEETS_PROPERTIES_HEADERS,
)

FIELD_SHEET_NAMES = [properties["name"] for properties in COMMON_CATEGORY_PROPERTIES.values()]
FIELD_SHEET_HEADERS = [
    "Field code in your format",
    "OpenBDF field code",
    "OpenBDF attribute name",
    "Datatype",
    "Requirements",
    "Default value",
    "Preprocess rule",
]
ENUM_SHEET_HEADERS = [
    "Value in your format",
    "OpenBDF enum value",
    "OpenBDF value display name",
    "OpenBDF value description (if any)",
    "OpenBDF value parent category (if applicable)",
]


def test_translator_template_adds_default_and_preprocess_columns(tmp_path):
    output_path = tmp_path / "translator_template.xlsx"
    save_translator(output_path)

    workbook = load_workbook(output_path)
    for sheet_name in FIELD_SHEET_NAMES:
        sheet = workbook[sheet_name]

        assert [sheet.cell(row=1, column=column).value for column in range(1, 8)] == FIELD_SHEET_HEADERS
        assert sheet["F1"].style == "AttributeName"
        assert sheet["G1"].style == "AttributeName"
        assert sheet.column_dimensions["F"].width == 30
        assert sheet.column_dimensions["G"].width == 30

        for row in range(2, sheet.max_row + 1):
            assert sheet.cell(row=row, column=6).value is None
            assert sheet.cell(row=row, column=7).value is None
            assert sheet.cell(row=row, column=6).style == "EditableValue"
            assert sheet.cell(row=row, column=7).style == "EditableValue"
            assert sheet.cell(row=row, column=6).protection.locked is False
            assert sheet.cell(row=row, column=7).protection.locked is False


def test_translator_template_keeps_non_field_sheet_layouts(tmp_path):
    output_path = tmp_path / "translator_template.xlsx"
    save_translator(output_path)

    workbook = load_workbook(output_path, read_only=True)
    library = workbook["Translations Library"]
    expected_library_headers = list(SHEETS_PROPERTIES_HEADERS.values())

    assert library.max_column == len(expected_library_headers)
    assert [library.cell(row=1, column=column).value for column in range(1, 11)] == expected_library_headers

    enum_sheet = workbook["ProjectUnits"]
    assert enum_sheet.max_column == 5
    assert [enum_sheet.cell(row=1, column=column).value for column in range(1, 6)] == ENUM_SHEET_HEADERS
