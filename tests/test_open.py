from pathlib import Path
from typing import Any

import pandas as pd
from typer.testing import CliRunner

import openbdf.main as main_module
from openbdf.main import app

runner = CliRunner()


def write_workbook(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, header=False, index=False)


def default_openbdf_sheets() -> dict[str, pd.DataFrame]:
    project = pd.DataFrame([[None] * 10])
    project.iloc[0, 3] = "project_name"
    project.iloc[0, 9] = "Example project"

    bill_of_materials = pd.DataFrame([[None] * 2 for _ in range(9)])
    bill_of_materials.iloc[7, 1] = "material_id"
    bill_of_materials.iloc[8, 1] = "MAT-1"

    results_wide = pd.DataFrame([[None] * 2 for _ in range(8)])
    results_wide.iloc[6, 1] = "material_id"
    results_wide.iloc[7, 1] = "MAT-1"

    return {
        "General Information": project,
        "Bill of Materials": bill_of_materials,
        "LCA Result (Wide)": results_wide,
    }


def mock_conversion_and_save(monkeypatch, captured_tables: list[Any]) -> None:
    def convert(tables, document_translator, drop_invalid=False):
        captured_tables.append((tables, drop_invalid))
        return object()

    monkeypatch.setattr(main_module, "project_package_from_tables", convert)
    monkeypatch.setattr(main_module, "save_openbdf_to_xlsx", lambda **kwargs: None)


def test_open_command_processes_sheets_split_across_files(tmp_path: Path, monkeypatch):
    sheets = default_openbdf_sheets()
    project = tmp_path / "project.xlsx"
    materials = tmp_path / "materials.xlsx"
    results = tmp_path / "results.xlsx"
    write_workbook(project, {"General Information": sheets["General Information"]})
    write_workbook(materials, {"Bill of Materials": sheets["Bill of Materials"]})
    write_workbook(results, {"LCA Result (Wide)": sheets["LCA Result (Wide)"]})
    captured_tables: list[Any] = []
    mock_conversion_and_save(monkeypatch, captured_tables)

    result = runner.invoke(app, ["open", str(results), str(project), str(materials)])

    assert result.exit_code == 0
    assert len(captured_tables) == 1
    tables, drop_invalid = captured_tables[0]
    assert drop_invalid is False
    assert tables.project.to_dict(orient="records") == [{"field_code": "project_name", "value": "Example project"}]
    assert tables.bill_of_materials.to_dict(orient="records") == [{"material_id": "MAT-1"}]
    assert tables.results_wide.to_dict(orient="records") == [{"material_id": "MAT-1"}]


def test_open_command_accepts_one_file(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "complete.xlsx"
    write_workbook(workbook, default_openbdf_sheets())
    captured_tables: list[Any] = []
    mock_conversion_and_save(monkeypatch, captured_tables)

    result = runner.invoke(app, ["open", str(workbook)])

    assert result.exit_code == 0
    assert len(captured_tables) == 1


def test_open_command_uses_draft_conversion(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "complete.xlsx"
    write_workbook(workbook, default_openbdf_sheets())
    captured_tables: list[Any] = []

    def convert_draft(tables, document_translator, drop_invalid=False):
        captured_tables.append((tables, drop_invalid))
        return object()

    def convert_strict(*args, **kwargs):
        raise AssertionError("strict conversion should not run")

    monkeypatch.setattr(main_module, "project_draft_package_from_tables", convert_draft)
    monkeypatch.setattr(main_module, "project_package_from_tables", convert_strict)
    monkeypatch.setattr(main_module, "save_openbdf_to_xlsx", lambda **kwargs: None)

    result = runner.invoke(app, ["open", str(workbook), "--draft"])

    assert result.exit_code == 0
    assert len(captured_tables) == 1


def test_open_command_drop_invalid_materials_passes_flag(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "complete.xlsx"
    write_workbook(workbook, default_openbdf_sheets())
    captured: list[Any] = []

    def convert_strict(tables, document_translator, drop_invalid=False):
        captured.append(drop_invalid)
        return object()

    monkeypatch.setattr(main_module, "project_package_from_tables", convert_strict)
    monkeypatch.setattr(main_module, "save_openbdf_to_xlsx", lambda **kwargs: None)

    result = runner.invoke(app, ["open", str(workbook), "--drop-invalid-materials"])

    assert result.exit_code == 0
    assert captured == [True]


def test_open_command_drop_invalid_materials_default_is_false(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "complete.xlsx"
    write_workbook(workbook, default_openbdf_sheets())
    captured: list[Any] = []

    def convert_strict(tables, document_translator, drop_invalid=False):
        captured.append(drop_invalid)
        return object()

    monkeypatch.setattr(main_module, "project_package_from_tables", convert_strict)
    monkeypatch.setattr(main_module, "save_openbdf_to_xlsx", lambda **kwargs: None)

    result = runner.invoke(app, ["open", str(workbook)])

    assert result.exit_code == 0
    assert captured == [False]


def test_open_command_reports_duplicate_sheets(tmp_path: Path):
    first = tmp_path / "first.xlsx"
    second = tmp_path / "second.xlsx"
    write_workbook(first, {"Shared": pd.DataFrame([[1]])})
    write_workbook(second, {"Shared": pd.DataFrame([[2]])})

    result = runner.invoke(app, ["open", str(first), str(second)])

    assert result.exit_code == 1
    assert "Duplicate sheet names" in result.output
    assert "Shared" in result.output
    assert str(first) in result.output
    assert str(second) in result.output


def test_open_command_uses_translator_option(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "complete.xlsx"
    translator_path = tmp_path / "translator.xlsx"
    write_workbook(workbook, default_openbdf_sheets())
    captured_paths: list[str] = []
    captured_tables: list[Any] = []
    default_translator = main_module.DocumentTranslator.default_openbdf_translator()

    def load_translator(*, xlsx_path, **kwargs):
        captured_paths.append(xlsx_path)
        return default_translator

    monkeypatch.setattr(main_module.DocumentTranslator, "from_xlsx", load_translator)
    mock_conversion_and_save(monkeypatch, captured_tables)

    result = runner.invoke(app, ["open", str(workbook), "--translator", str(translator_path)])

    assert result.exit_code == 0
    assert captured_paths == [str(translator_path)]
    assert len(captured_tables) == 1
