from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd
import pytest
from typer.testing import CliRunner

import openbdf.main as main_module
from openbdf.lib.validation import (
    DeclaredIndicatorWithoutResults,
    OpenBDFValidationErrors,
    ResultsWithoutIndicatorDeclaration,
    Severity,
    check_declared_results,
    format_findings,
)
from openbdf.lib.validation.declared_results import TALL_SHEET, WIDE_SHEET, wide_blocks
from openbdf.main import app
from openbdf.model.enums.lca import LCIAMethodology
from openbdf.model.lca_results import GWP_TOTAL_STAGES, INDICATORS
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase

runner = CliRunner()

TRACI = LCIAMethodology.US_EPA_TRACI_2_1
EN_15804_A2 = LCIAMethodology.EN_15804_2012_A2_2019

_STAGE_BY_SUFFIX = {suffix: stage.value for stage, suffix in GWP_TOTAL_STAGES}


def aligned_suffixes(code: str, methodology: LCIAMethodology) -> list[str]:
    return [suffix for suffix, alignment in wide_blocks()[code] if methodology.value in alignment]


def wide_record(material_id: str, **values: Any) -> LCAResultsWideFullBase:
    return LCAResultsWideFullBase(material_id=material_id, **values)


def tall_record(material_id: str, stage: str, **values: Any) -> LCAResultsTallBase:
    return LCAResultsTallBase(material_id=material_id, lca_stage_module_submodule=stage, **values)


def results(code: str, methodology: LCIAMethodology, value: str = "1", **overrides: Any) -> dict[str, Decimal]:
    return {f"{code}_{suffix}": Decimal(value) for suffix in aligned_suffixes(code, methodology)} | overrides


def tall_results(code: str, methodology: LCIAMethodology, value: str = "1", material_id: str = "MAT-1"):
    return [
        tall_record(material_id, _STAGE_BY_SUFFIX[suffix], **{code: Decimal(value)})
        for suffix in aligned_suffixes(code, methodology)
        if suffix in _STAGE_BY_SUFFIX
    ]


def material(material_id: str = "MAT-1", wide: Any = None, tall: list[Any] | None = None):
    return SimpleNamespace(
        material_id=material_id,
        lca_results_full_record=wide,
        lca_results_tall_full_records=list(tall or []),
    )


def project(methodology: LCIAMethodology | None, materials: list[Any], **declared: bool | None):
    flags: dict[str, bool | None] = {f"lca_{indicator.code}_declared": None for indicator in INDICATORS}
    flags.update({f"lca_{code}_declared": value for code, value in declared.items()})
    return SimpleNamespace(lcia_methodology=methodology, bill_of_materials=materials, **flags)


def test_a_declared_indicator_with_all_aligned_results_passes():
    wide = wide_record("MAT-1", **results("gwp_total", EN_15804_A2))
    tall = tall_results("gwp_total", EN_15804_A2)

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide, tall=tall)], gwp_total=True))

    assert findings == []


def test_a_declared_indicator_missing_one_aligned_column_warns_on_the_wide_sheet():
    wide = wide_record("MAT-1", **results("gwp_total", EN_15804_A2, gwp_total_d=None))
    tall = tall_results("gwp_total", EN_15804_A2)

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide, tall=tall)], gwp_total=True))

    assert [finding.source for finding in findings] == [WIDE_SHEET]
    assert str(findings[0]) == ("E25: Indicator gwp_total is declared but carries no result in d for material MAT-1")
    assert findings[0].severity is Severity.WARNING


def test_a_declared_indicator_missing_one_aligned_row_warns_on_the_tall_sheet():
    wide = wide_record("MAT-1", **results("gwp_total", EN_15804_A2))
    tall = [record for record in tall_results("gwp_total", EN_15804_A2) if record.lca_stage_module_submodule != "D"]

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide, tall=tall)], gwp_total=True))

    assert [finding.source for finding in findings] == [TALL_SHEET]
    assert "carries no result in d for material MAT-1" in str(findings[0])


def test_a_result_behind_an_undeclared_indicator_rejects_the_file_even_when_the_column_is_not_aligned():
    assert "b8" not in aligned_suffixes("gwp_total", EN_15804_A2)
    wide = wide_record("MAT-1", gwp_total_b8=Decimal("1"))

    with pytest.raises(OpenBDFValidationErrors) as raised:
        check_declared_results(project(EN_15804_A2, [material(wide=wide)], gwp_total=False))

    assert str(raised.value.findings[0]) == (
        "E26: Indicator gwp_total carries a result in b8 but is not declared for material MAT-1"
    )
    assert [finding.source for finding in raised.value.findings] == [WIDE_SHEET]
    assert raised.value.errors == raised.value.findings
    assert raised.value.warnings == []


def test_a_zero_counts_as_a_result():
    wide = wide_record("MAT-1", **results("gwp_total", EN_15804_A2, value="0"))
    tall = tall_results("gwp_total", EN_15804_A2, value="0")

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide, tall=tall)], gwp_total=True))

    assert findings == []


def test_a_material_without_any_result_row_is_flagged_for_every_aligned_column():
    findings = check_declared_results(project(EN_15804_A2, [material()], gwp_total=True))

    assert [finding.source for finding in findings] == [WIDE_SHEET, TALL_SHEET]
    assert all(isinstance(finding, DeclaredIndicatorWithoutResults) for finding in findings)


def test_an_empty_declaration_flag_skips_the_indicator():
    wide = wide_record("MAT-1", **results("gwp_total", EN_15804_A2))

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide)]))

    assert findings == []


def test_the_check_is_skipped_without_a_methodology():
    wide = wide_record("MAT-1", gwp_total_b8=Decimal("1"))
    tall = [tall_record("MAT-1", "B8", gwp_total=Decimal("1"))]

    findings = check_declared_results(project(None, [material(wide=wide, tall=tall)], gwp_total=False))

    assert findings == []


def test_a_methodology_without_aligned_columns_requires_nothing():
    assert aligned_suffixes("gwp_total", LCIAMethodology.EN_15978_2026) == []
    wide = wide_record("MAT-1", gwp_total_a1_a3=Decimal("1"))

    findings = check_declared_results(project(LCIAMethodology.EN_15978_2026, [material(wide=wide)], gwp_total=True))

    assert findings == []


def test_draft_mode_downgrades_a_reject_to_a_warning():
    wide = wide_record("MAT-1", gwp_total_b8=Decimal("1"))

    findings = check_declared_results(project(EN_15804_A2, [material(wide=wide)], gwp_total=False), draft=True)

    assert [finding.severity for finding in findings] == [Severity.WARNING]
    assert isinstance(findings[0], ResultsWithoutIndicatorDeclaration)


def test_findings_are_capped_per_sheet_in_the_terminal_output():
    findings = [DeclaredIndicatorWithoutResults(f"finding {index}", source=WIDE_SHEET) for index in range(53)]

    lines = format_findings(findings, limit=50)

    assert lines[0] == f"{WIDE_SHEET}:"
    assert lines[1] == "  E25: finding 0"
    assert lines[-1] == "  ... 3 more findings not shown"
    assert len(lines) == 52


def write_workbook(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, header=False, index=False)


def default_openbdf_sheets() -> dict[str, pd.DataFrame]:
    project = pd.DataFrame([[None] * 11])
    project.iloc[0, 3] = "project_name"
    project.iloc[0, 10] = "Example project"

    # Generated template layout: field codes in row 2, data from row 10.
    def horizontal_sheet(field_code: str, value: str) -> pd.DataFrame:
        dataframe = pd.DataFrame([[None] * 2 for _ in range(10)])
        dataframe.iloc[1, 1] = field_code
        dataframe.iloc[9, 1] = value
        return dataframe

    return {
        "General Information": project,
        "Bill of Materials": horizontal_sheet("material_id", "MAT-1"),
        "Project Material Database": horizontal_sheet("material_ref_id", "M0001"),
        "LCA Result (Wide)": horizontal_sheet("material_id", "MAT-1"),
    }


def run_open(tmp_path: Path, monkeypatch, project_object: Any, *arguments: str) -> tuple[Any, Path]:
    source = tmp_path / "project.xlsx"
    output = tmp_path / "output.xlsx"
    write_workbook(source, default_openbdf_sheets())

    def fake_save(xlsx_path: str, project: Any) -> None:
        Path(xlsx_path).write_text("exported")

    monkeypatch.setattr(main_module, "project_package_from_tables", lambda *args, **kwargs: project_object)
    monkeypatch.setattr(main_module, "save_openbdf_to_xlsx", fake_save)
    result = runner.invoke(app, ["open", str(source), "--output-path", str(output), *arguments])
    return result, output


def rejecting_project() -> Any:
    wide = wide_record("MAT-1", gwp_total_b8=Decimal("1"))
    return project(EN_15804_A2, [material(wide=wide)], gwp_total=False)


def test_open_command_rejects_the_file_and_skips_the_export(tmp_path: Path, monkeypatch):
    result, output = run_open(tmp_path, monkeypatch, rejecting_project())

    assert result.exit_code == 1
    assert "E26: Indicator gwp_total carries a result in b8 but is not declared for material MAT-1" in result.output
    assert not output.exists()


def test_open_command_exports_the_file_in_draft_mode_despite_a_reject(tmp_path: Path, monkeypatch):
    result, output = run_open(tmp_path, monkeypatch, rejecting_project(), "--draft")

    assert result.exit_code == 0
    assert "E26: Indicator gwp_total carries a result in b8 but is not declared for material MAT-1" in result.output
    assert output.read_text() == "exported"
