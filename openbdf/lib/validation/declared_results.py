from __future__ import annotations

from collections import defaultdict
from functools import cache
from typing import Any

from openbdf.lib.types.fields import field_metadata
from openbdf.lib.validation.errors import (
    DeclaredIndicatorWithoutResults,
    OpenBDFValidationError,
    ResultsWithoutIndicatorDeclaration,
)
from openbdf.model.enums.lca import LCIAMethodology
from openbdf.model.lca_results import GWP_TOTAL_STAGES, INDICATORS
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase

WIDE_SHEET = "LCA Result (Wide)"
TALL_SHEET = "LCA Result (Tall)"

# A tall row names its stage with the enum value, a wide column with a suffix. The wide
# naming is the reference, so the suffix is resolved once for both sheets.
_SUFFIX_BY_STAGE = {stage.value: suffix for stage, suffix in GWP_TOTAL_STAGES}
# The whole-life total column has no tall row of its own.
_TALL_SUFFIXES = frozenset(_SUFFIX_BY_STAGE.values())


@cache
def wide_blocks() -> dict[str, tuple[tuple[str, str], ...]]:
    """
    Map each indicator code to the (suffix, reference alignment) pairs of its wide columns.

    Indicator codes are not prefix free (`ap` matches `ap_ae_*`), so the longest code wins.
    """
    codes = sorted((indicator.code for indicator in INDICATORS), key=len, reverse=True)
    blocks: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for field in LCAResultsWideFullBase.model_fields.values():
        extra = field_metadata(field)
        field_code = extra.get("field_code") or ""
        code = next((code for code in codes if field_code == code or field_code.startswith(f"{code}_")), None)
        if code is None:
            continue
        blocks[code].append((field_code[len(code) + 1 :], extra.get("reference_alignment") or ""))

    return {code: tuple(columns) for code, columns in blocks.items()}


def check_declared_results(project: Any) -> list[OpenBDFValidationError]:
    """
    Compare the lca_<indicator>_declared flags of the project with the LCA results of its materials.

    A declared indicator must fill every result column whose reference alignment contains the
    chosen LCIA methodology, an undeclared indicator must fill none of them. The check is
    skipped when no methodology is given, and an empty flag means unknown.
    """
    methodology = getattr(project, "lcia_methodology", None)
    if methodology is None:
        return []

    findings: list[OpenBDFValidationError] = []
    for material in project.bill_of_materials:
        for indicator in INDICATORS:
            declared = getattr(project, f"lca_{indicator.code}_declared", None)
            if declared is None:
                continue
            findings.extend(
                _check_indicator(
                    material_id=material.material_id,
                    code=indicator.code,
                    declared=declared,
                    methodology=methodology,
                    wide=material.lca_results_full_record,
                    tall=material.lca_results_tall_full_records or [],
                )
            )

    return findings


def _check_indicator(
    material_id: str,
    code: str,
    declared: bool,
    methodology: LCIAMethodology,
    wide: Any,
    tall: list[Any],
) -> list[OpenBDFValidationError]:
    columns = wide_blocks().get(code, ())
    aligned = [suffix for suffix, alignment in columns if methodology.value in alignment]

    wide_values = {suffix: getattr(wide, f"{code}_{suffix}", None) for suffix in dict.fromkeys(s for s, _ in columns)}
    tall_values = {
        suffix: getattr(row, code, None)
        for row in tall
        if (suffix := _SUFFIX_BY_STAGE.get(str(row.lca_stage_module_submodule))) is not None
    }

    findings: list[OpenBDFValidationError] = []
    if declared:
        missing = [suffix for suffix in aligned if wide_values.get(suffix) is None]
        if missing:
            findings.append(
                DeclaredIndicatorWithoutResults(
                    f"Indicator {code} is declared but carries no result in {', '.join(missing)} "
                    f"for material {material_id}",
                    source=WIDE_SHEET,
                )
            )
        missing_tall = [suffix for suffix in aligned if suffix in _TALL_SUFFIXES and tall_values.get(suffix) is None]
        if missing_tall:
            findings.append(
                DeclaredIndicatorWithoutResults(
                    f"Indicator {code} is declared but carries no result in {', '.join(missing_tall)} "
                    f"for material {material_id}",
                    source=TALL_SHEET,
                )
            )
    else:
        undeclared = [suffix for suffix, value in wide_values.items() if value is not None]
        if undeclared:
            findings.append(
                ResultsWithoutIndicatorDeclaration(
                    f"Indicator {code} carries a result in {', '.join(undeclared)} "
                    f"but is not declared for material {material_id}",
                    source=WIDE_SHEET,
                )
            )
        undeclared_tall = [suffix for suffix, value in tall_values.items() if value is not None]
        if undeclared_tall:
            findings.append(
                ResultsWithoutIndicatorDeclaration(
                    f"Indicator {code} carries a result in {', '.join(undeclared_tall)} "
                    f"but is not declared for material {material_id}",
                    source=TALL_SHEET,
                )
            )
    return findings
