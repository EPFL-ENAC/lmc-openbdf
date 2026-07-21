from pathlib import Path

import pandas as pd
import pytest

from openbdf.lib.converters.translators import DocumentTranslator, SheetTranslation, TranslationsLibrary
from openbdf.lib.importer import (
    DuplicateSheetNamesError,
    ExcelSheetSource,
    load_openbdf_tables,
)


class MemorySheetSource:
    def __init__(self, sheets: dict[str, pd.DataFrame]):
        self._sheets = sheets
        self.read_sheets: list[str] = []

    @property
    def sheet_names(self):
        return self._sheets.keys()

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        self.read_sheets.append(sheet_name)
        return self._sheets[sheet_name].copy()


def write_workbook(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, header=False, index=False)


def table_translator() -> DocumentTranslator:
    return DocumentTranslator(
        library=TranslationsLibrary([
            SheetTranslation(
                original_name="Project Input",
                translated_name="General Information",
                orientation="vertical",
                header_col=0,
                values_col=1,
            ),
            SheetTranslation(
                original_name="Materials Input",
                translated_name="Bill of Materials",
                orientation="horizontal",
                header_row=0,
                start_row=1,
                start_col=0,
            ),
            SheetTranslation(
                original_name="Wide Input",
                translated_name="LCA Result (Wide)",
                orientation="horizontal",
                header_row=0,
                start_row=1,
                start_col=0,
            ),
            SheetTranslation(
                original_name="Tall Input",
                translated_name="LCA Result (Tall)",
                orientation="horizontal",
                header_row=0,
                start_row=1,
                start_col=0,
            ),
        ])
    )


def test_load_openbdf_tables_uses_only_the_sheet_source_interface():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
        "Materials Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
        "Wide Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
        "Tall Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
    })

    tables = load_openbdf_tables(source, table_translator())

    assert tables is not None
    assert tables.project.to_dict(orient="records") == [{"field_code": "project_name", "value": "Example project"}]
    assert tables.bill_of_materials.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.results_wide is not None
    assert tables.results_wide.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.results_tall is not None
    assert tables.results_tall.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert source.read_sheets == ["Project Input", "Materials Input", "Wide Input", "Tall Input"]


def test_load_openbdf_tables_allows_missing_optional_sheets():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
        "Materials Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
    })

    tables = load_openbdf_tables(source, table_translator())

    assert tables is not None
    assert tables.results_wide is None
    assert tables.results_tall is None


def test_load_openbdf_tables_returns_none_when_a_required_sheet_is_missing():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
    })

    assert load_openbdf_tables(source, table_translator()) is None
    assert source.read_sheets == ["Project Input"]


@pytest.mark.parametrize("reverse_order", [False, True])
def test_excel_sheet_source_reads_multiple_files_lazily_and_closes_them(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    reverse_order: bool,
):
    first = tmp_path / "first.xlsx"
    second = tmp_path / "second.xlsx"
    write_workbook(first, {"First": pd.DataFrame([[1]])})
    write_workbook(second, {"Second": pd.DataFrame([[2]])})
    paths = [first, second]
    if reverse_order:
        paths.reverse()

    parse_calls: list[str] = []
    close_calls: list[pd.ExcelFile] = []
    original_parse = pd.ExcelFile.parse
    original_close = pd.ExcelFile.close

    def track_parse(workbook, sheet_name, *args, **kwargs):
        parse_calls.append(sheet_name)
        return original_parse(workbook, sheet_name, *args, **kwargs)

    def track_close(workbook):
        close_calls.append(workbook)
        return original_close(workbook)

    monkeypatch.setattr(pd.ExcelFile, "parse", track_parse)
    monkeypatch.setattr(pd.ExcelFile, "close", track_close)

    source = ExcelSheetSource(paths)
    with source:
        assert set(source.sheet_names) == {"First", "Second"}
        assert parse_calls == []
        assert source.read_sheet("First").iloc[0, 0] == 1
        assert parse_calls == ["First"]

    assert len(close_calls) == 2
    with pytest.raises(RuntimeError, match="context manager"):
        source.read_sheet("Second")


def test_excel_sheet_source_accepts_a_single_path(tmp_path: Path):
    workbook = tmp_path / "single.xlsx"
    write_workbook(workbook, {"Only": pd.DataFrame([[42]])})

    with ExcelSheetSource(workbook) as source:
        assert list(source.sheet_names) == ["Only"]
        assert source.read_sheet("Only").iloc[0, 0] == 42


def test_excel_sheet_source_rejects_every_duplicate_sheet(tmp_path: Path):
    first = tmp_path / "first.xlsx"
    second = tmp_path / "second.xlsx"
    write_workbook(first, {"Shared A": pd.DataFrame([[1]]), "Shared B": pd.DataFrame([[2]])})
    write_workbook(second, {"Shared A": pd.DataFrame([[3]]), "Shared B": pd.DataFrame([[4]])})

    with pytest.raises(DuplicateSheetNamesError) as error:
        with ExcelSheetSource([first, second]):
            pass

    assert set(error.value.duplicates) == {"Shared A", "Shared B"}
    assert error.value.duplicates["Shared A"] == [first, second]
    assert str(first) in str(error.value)
    assert str(second) in str(error.value)


def test_excel_sheet_source_rejects_empty_input():
    with pytest.raises(ValueError, match="At least one input workbook is required"):
        ExcelSheetSource([])
