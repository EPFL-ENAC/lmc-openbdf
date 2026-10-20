from pathlib import Path

import pandas as pd
import pytest

from openbdf.lib.converters.translators import DocumentTranslator, SheetTranslation, TranslationsLibrary
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.sources import DuplicateSheetNamesError, ExcelSheetSource


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
                original_name="Materials Database Input",
                translated_name="Project Material Database",
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


def test_openbdf_tables_from_source_uses_only_the_sheet_source_interface():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
        "Materials Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
        "Materials Database Input": pd.DataFrame([["material_ref_id"], ["M0001"]]),
        "Wide Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
        "Tall Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
    })

    tables = OpenBDFTables.from_source(source, table_translator())

    assert tables is not None
    assert tables.project.to_dict(orient="records") == [{"field_code": "project_name", "value": "Example project"}]
    assert tables.bill_of_materials.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.project_material_database.to_dict(orient="records") == [{"material_ref_id": "M0001"}]
    assert tables.results_wide is not None
    assert tables.results_wide.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.results_tall is not None
    assert tables.results_tall.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert source.read_sheets == [
        "Project Input",
        "Materials Input",
        "Materials Database Input",
        "Wide Input",
        "Tall Input",
    ]


def test_openbdf_tables_from_source_allows_missing_optional_sheets():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
        "Materials Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
        "Materials Database Input": pd.DataFrame([["material_ref_id"], ["M0001"]]),
    })

    tables = OpenBDFTables.from_source(source, table_translator())

    assert tables is not None
    assert tables.results_wide is None
    assert tables.results_tall is None


def test_openbdf_tables_from_source_returns_none_when_a_required_sheet_is_missing():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
    })

    assert OpenBDFTables.from_source(source, table_translator()) is None
    assert source.read_sheets == ["Project Input"]


def test_openbdf_tables_from_source_leaves_the_project_material_database_empty_when_the_sheet_is_missing():
    source = MemorySheetSource({
        "Project Input": pd.DataFrame([["project_name", "Example project"]]),
        "Materials Input": pd.DataFrame([["material_id"], ["MAT-1"]]),
    })

    tables = OpenBDFTables.from_source(source, table_translator())

    assert tables is not None
    assert tables.bill_of_materials.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.project_material_database is None


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


def cola_translator_args() -> dict:
    return {
        "attribute_name_col": 0,
        "translated_name_col": 1,
        "default_value_col": 5,
        "preprocess_rule_col": 6,
        "header_row": 0,
    }


def translator_path(filename: str) -> Path:
    return Path(__file__).parents[1] / "translators" / filename


def test_cola_translator_maps_material_reference_service_life():
    translator = DocumentTranslator.from_xlsx(
        translator_path("translator_at_v2.0.0.xlsx"),
        **cola_translator_args(),
    )

    assert translator.translate("Bill of Materials", "Lebensdauer (Jahre)") == ["material_reference_service_life"]


def test_bec_translator_maps_building_element_classification():
    translator = DocumentTranslator.from_xlsx(
        translator_path("translator_bec_at_v2.0.0.xlsx"),
        **cola_translator_args(),
    )

    assert translator.translate("OpenBDFBuildingElementClassific", "2 Bauwerk-Rohbau") == ["2"]
    assert translator.translate("OpenBDFBuildingElementClassific", "2C Gründungen, Unterbau") == ["1.1"]
    assert translator.translate("OpenBDFBuildingElementClassific", "2E Vertikale Rohbaukonstruktionen") == ["2.1"]


def test_bmc_translator_maps_material_classification():
    translator = DocumentTranslator.from_xlsx(
        translator_path("translator_bmc_at_v2.0.0.xlsx"),
        **cola_translator_args(),
    )

    assert translator.translate("OpenBDFMaterialClassification", "i9") == ["1.1"]
    assert translator.translate("OpenBDFMaterialClassification", "n") == ["2.1"]
    assert translator.translate("OpenBDFMaterialClassification", "n6") == ["2.2"]


def test_cola_translator_set_maps_attributes_and_classification():
    translator = DocumentTranslator()
    for filename in (
        "translator_at_v2.0.0.xlsx",
        "translator_bec_at_v2.0.0.xlsx",
        "translator_bmc_at_v2.0.0.xlsx",
    ):
        translator = translator + DocumentTranslator.from_xlsx(
            translator_path(filename),
            **cola_translator_args(),
        )

    assert translator.translate("Bill of Materials", "Lebensdauer (Jahre)") == ["material_reference_service_life"]
    assert translator.translate("OpenBDFBuildingElementClassific", "2 Bauwerk-Rohbau") == ["2"]
    assert translator.translate("OpenBDFMaterialClassification", "i9") == ["1.1"]
