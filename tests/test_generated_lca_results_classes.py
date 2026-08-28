from __future__ import annotations

from pathlib import Path

from openbdf.model import lca_results

_MODEL_DIR = Path(lca_results.__file__).resolve().parent


def _formatted(filename: str) -> str:
    """Render and format a generated model module exactly as the generator does."""
    renders = dict(lca_results.GENERATED_MODULES)
    render = renders[filename]
    return lca_results.format_module_source(render())


def test_generated_classes_are_in_sync_with_the_registry():
    """The committed generated modules must match what the generator produces."""
    for filename, _ in lca_results.GENERATED_MODULES:
        expected = _formatted(filename)
        actual = (_MODEL_DIR / filename).read_text(encoding="utf-8")
        assert actual == expected, (
            f"{filename} is out of sync with the registry. Run: make generate-lca-results-classes"
        )


def test_tall_module_has_static_fields():
    tall = _formatted("lca_results_full_tall.py")
    assert "material_id: str = Field(" in tall
    assert "lca_service_life: Decimal = Field(" in tall
    assert "lca_stage_or_module: LCAStageOrModule = Field(" in tall


def test_wide_module_gwp_total_special_cases():
    """gwp_total keeps a bare required total field and a required a1-a3 field."""
    wide = _formatted("lca_results_full_wide.py")
    assert "    gwp_total: Decimal = Field(" in wide
    assert "gwp_total_total" not in wide
    assert 'attribute_name="Total Global Warming Potential"' in wide
    assert "    gwp_total_a1_a3: Decimal = Field(" in wide
    assert 'requirements="Required"' in wide


def test_wide_module_has_expected_field_count():
    """One material id plus 20 indicators x (16 stages + 1 total) fields."""
    wide = _formatted("lca_results_full_wide.py")
    field_count = sum(1 for line in wide.splitlines() if " = Field(" in line)
    assert field_count == 1 + len(lca_results.INDICATORS) * (len(lca_results.STAGES) + 1)


def test_generated_files_warn_against_manual_edits():
    for filename, _ in lca_results.GENERATED_MODULES:
        content = (_MODEL_DIR / filename).read_text(encoding="utf-8")
        assert "Do not edit by hand" in content
        assert "generate-lca-results-classes" in content
