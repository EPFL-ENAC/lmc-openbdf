from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from openbdf.lib.converters.dataframe import project_package_from_tables
from openbdf.lib.openbdf_tables import OpenBDFTables, workbook_translator
from openbdf.lib.sources.excel_source import ExcelSheetSource
from openbdf.lib.validation import DroppedLine, OpenBDFValidationError, validate_project
from openbdf.model.enums.element_classifications import OpenBDFBuildingElementClassification

# The row sheets of the specification keep labels in column A, the old codes on Excel
# row 3, the updated codes on row 4, and the data from row 14.
FIRST_DATA_ROW = 14


def row_sheet(workbook: Workbook, title: str, codes: list[tuple[str, str | None]], rows: list[list[Any]]) -> None:
    sheet = workbook.create_sheet(title)
    sheet.cell(3, 1, "Field Code")
    sheet.cell(4, 1, "UPDATED Field Code")
    for column, (old, new) in enumerate(codes, start=2):
        sheet.cell(3, column, old)
        sheet.cell(4, column, new)
    for offset, row in enumerate(rows):
        for column, value in enumerate(row, start=2):
            sheet.cell(FIRST_DATA_ROW + offset, column, value)


def specification_workbook(path: Path) -> None:
    workbook = Workbook()
    general = workbook.active
    general.title = "General Information"
    # Codes in columns G and H, values in column Q, from Excel row 2.
    general.cell(1, 7, "Field Code")
    general.cell(1, 8, "UPDATED Field Code")
    general.cell(1, 17, "Value")
    for row, (old, new, value) in enumerate(
        [("project_name", None, "Spec project"), ("permit_date", "project_permit_date", 43466)], start=2
    ):
        general.cell(row, 7, old)
        general.cell(row, 8, new)
        general.cell(row, 17, value)

    row_sheet(
        workbook,
        "Bill of Materials",
        [
            ("material_id", None),
            ("material_name_custom", "custom_material_name"),
            ("bec_custom", None),
            ("bec_openbdf", None),
            ("material_weight_kg", None),
        ],
        [
            # The national code has no mapping, so the workbook's own element code, a number cell, is kept.
            ["MAT-1", "Concrete", "2E.01 Aussenwandkonstruktionen", 2.1, 100],
            ["MAT-2", None, None, None, 500],  # dropped, carried a mass and results
            ["MAT-3", None, None, None, 0],  # dropped, carried nothing
        ],
    )
    row_sheet(
        workbook,
        "LCA Result (Wide)",
        [
            ("material_id", None),
            ("gwp_total_a1_a3", None),
            ("gwp_total_d", None),
            ("gwp_total_d1", None),
            ("gwp_total_d2", None),
            ("gwp_total_total", None),
        ],
        [
            ["MAT-1", 10, 1, 0.5, 0.5, 12],  # module D added twice to the total
            ["MAT-2", 5, None, None, None, 5],
            ["MAT-3", 0],  # a zero result adds nothing, so it is not data
        ],
    )
    workbook.save(path)


def test_a_specification_layout_workbook_is_read_with_its_updated_codes(tmp_path: Path):
    path = tmp_path / "specification.xlsx"
    specification_workbook(path)

    with ExcelSheetSource(path) as source:
        translator = workbook_translator(source)
        tables = OpenBDFTables.from_source(source, translator)
    assert tables is not None
    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(tables, translator, findings=findings, draft=True, drop_invalid=True)
    dropped = frozenset(finding.row for finding in findings if isinstance(finding, DroppedLine) and finding.row)
    findings.extend(validate_project(project, tables, document_translator=translator, dropped_rows=dropped))

    assert project.project_name == "Spec project"
    assert project.project_permit_date == date(2019, 1, 1)
    [concrete] = project.bill_of_materials
    assert (concrete.material_id, concrete.custom_material_name) == ("MAT-1", "Concrete")
    assert concrete.bec_openbdf.value == "2.1"
    dropped_findings = sorted((finding.code, finding.row) for finding in findings if finding.code == "W005")
    assert dropped_findings == [("W005", 15), ("W005", 16)]


def test_a_whole_number_cell_finds_its_element_code():
    # pandas reads a whole-number cell as an int, and any other number cell as a float.
    assert OpenBDFBuildingElementClassification.find_value(2.1).value == "2.1"
    assert OpenBDFBuildingElementClassification.find_value(2).value == "2"
