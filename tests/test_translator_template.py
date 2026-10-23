from openpyxl import load_workbook

from openbdf.cli.save import save_openbdf_to_xlsx, save_translator
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

    bill_of_materials = workbook[COMMON_CATEGORY_PROPERTIES["bom"]["name"]]
    service_life_row = next(
        row for row in bill_of_materials.iter_rows() if row[1].value == "material_reference_service_life"
    )
    assert [cell.value for cell in service_life_row[:5]] == [
        None,
        "material_reference_service_life",
        "Reference Service Life (RSL)",
        "Decimal",
        "Required",
    ]


def test_openbdf_template_includes_criticality_metadata(tmp_path):
    output_path = tmp_path / "openbdf_template.xlsx"
    save_openbdf_to_xlsx(output_path, None)

    workbook = load_workbook(output_path)
    info = workbook["General Information"]
    assert [info.cell(row=1, column=column).value for column in range(9, 12)] == [
        "Requirements",
        "Criticality",
        "Value",
    ]
    assert info.cell(row=2, column=10).value == "SHOULD"

    for sheet_name in FIELD_SHEET_NAMES[1:]:
        sheet = workbook[sheet_name]
        assert sheet["A2"].value == "Field Code"
        assert sheet["A3"].value == "Description"
        assert sheet["A4"].value == "Data Type"
        assert sheet["A5"].value == "Constraint"
        assert sheet["A6"].value == "Units"
        assert sheet["A7"].value == "Requirements"
        assert sheet["A8"].value == "Criticality"
        # Reference alignment position (v2.0.0): row 9 stays present but empty.
        assert sheet["A9"].value is None
        assert sheet.cell(row=2, column=2).value == "material_id"
        # material_id is MUST in format v2.0.0 on every field sheet.
        assert sheet.cell(row=8, column=2).value == "MUST"

    type_definitions = workbook["TypeDefinitions"]
    assert type_definitions["A1"].style == "AttributeName"
    assert type_definitions["B1"].style == "AttributeName"

    theme = workbook.loaded_theme
    assert b'<a:latin typeface="Calibri"/>' in theme
    assert b"Cambria" not in theme

    assert all(font.name == "Calibri" for font in workbook._fonts)


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
