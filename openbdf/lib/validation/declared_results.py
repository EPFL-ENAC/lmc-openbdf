from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from functools import cache
from typing import Any

from openbdf.lib.types.fields import field_metadata
from openbdf.lib.validation.errors import (
    AggregateAndSubModulesBothFilled,
    DeclaredIndicatorWithoutResults,
    MinorTotalSumMismatch,
    ModuleDInTotal,
    OpenBDFValidationError,
    ResultsWithoutIndicatorDeclaration,
    TotalSumMismatch,
)
from openbdf.model.enums.lca import LCIAMethodology
from openbdf.model.lca_results import (
    AC_STAGE_SUFFIXES,
    AGGREGATE_CHILDREN,
    GWP_TOTAL_STAGES,
    INDICATORS,
    STAGE_DISPLAY_BY_SUFFIX,
    SUB_MODULE_CHILDREN,
)
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase

WIDE_SHEET = "LCA Result (Wide)"
TALL_SHEET = "LCA Result (Tall)"

# A tall row names its stage with the enum value, a wide column with a suffix. The wide
# naming is the reference, so the suffix is resolved once for both sheets.
_SUFFIX_BY_STAGE = {stage.value: suffix for stage, suffix in GWP_TOTAL_STAGES}
# The whole-life total column has no tall row of its own.
_TALL_SUFFIXES = frozenset(_SUFFIX_BY_STAGE.values())

# The specification names a tolerance without giving a value, so a relative deviation of
# 1 per cent is the working choice. Below 5 per cent the mismatch is W011, at or above it E019.
_RELATIVE_TOLERANCE = Decimal("0.01")
_MINOR_DEVIATION = Decimal("0.05")


def check_stage_totals(project: Any) -> list[OpenBDFValidationError]:
    """
    E017 to E019 and W011, on the wide results of each material. An aggregate stage and
    its sub-modules must not carry values beside each other, and the total column must
    match the sum over the modules A to C, with module D left out.
    """
    findings: list[OpenBDFValidationError] = []
    for material in project.bill_of_materials:
        wide = material.lca_results_full_record
        if wide is None:
            continue
        for indicator in INDICATORS:
            code = indicator.code
            suffixes = {suffix for suffix, _ in wide_blocks().get(code, ()) if suffix and suffix != "total"}
            values = {suffix: getattr(wide, f"{code}_{suffix}", None) for suffix in suffixes}
            findings.extend(_check_stage_coexistence(material.material_id, code, values))
            findings.extend(_check_total(material.material_id, code, wide, values))
    return findings


def _check_stage_coexistence(material_id: str, code: str, values: dict[str, Any]) -> list[OpenBDFValidationError]:
    findings: list[OpenBDFValidationError] = []
    for aggregate, children in AGGREGATE_CHILDREN.items():
        if values.get(aggregate) is None:
            continue
        filled = [child for child in children if values.get(child) is not None]
        if filled:
            names = ", ".join(STAGE_DISPLAY_BY_SUFFIX.get(child, child) for child in filled)
            findings.append(
                AggregateAndSubModulesBothFilled(
                    f"Module {STAGE_DISPLAY_BY_SUFFIX.get(aggregate, aggregate)} and its sub-modules {names} "
                    f"are both populated for material {material_id}",
                    source=WIDE_SHEET,
                )
            )
    return findings


def _check_total(
    material_id: str,
    code: str,
    wide: Any,
    values: dict[str, Any],
) -> list[OpenBDFValidationError]:
    total_code = f"{code}_total"
    total = getattr(wide, total_code, None)
    if total is None:
        return []
    ac_sum = _sum_ac_stages(values)
    if ac_sum is None:
        return []
    deviation = _relative_deviation(total, ac_sum)
    if deviation <= _RELATIVE_TOLERANCE:
        return []
    d, d1, d2 = (values.get(suffix) or 0 for suffix in ("d", "d1", "d2"))
    # Module D is declared as d, or as d1 and d2, and some workbooks add both.
    if any(_relative_deviation(total, ac_sum + with_d) <= _RELATIVE_TOLERANCE for with_d in (d, d1 + d2, d + d1 + d2)):
        return [
            ModuleDInTotal(
                f"{total_code} adds module D to the whole-life total, the modules A to C sum to {ac_sum}",
                source=WIDE_SHEET,
            )
        ]
    message = f"{total_code} is {total}, the modules sum to {ac_sum}"
    mismatch = MinorTotalSumMismatch if deviation < _MINOR_DEVIATION else TotalSumMismatch
    return [mismatch(message, source=WIDE_SHEET)]


def _sum_ac_stages(values: dict[str, Any]) -> Decimal | None:
    """Sum the modules A to C. An aggregate column stands in for its empty sub-modules."""
    stage_values: list[Decimal] = []
    for suffix in AC_STAGE_SUFFIXES:
        if suffix not in values:
            continue
        value = values[suffix]
        if value is None:
            value = _sum_children(suffix, values)
        if value is not None:
            stage_values.append(value)
    return sum(stage_values, Decimal(0)) if stage_values else None


def _sum_children(suffix: str, values: dict[str, Any]) -> Decimal | None:
    children = AGGREGATE_CHILDREN.get(suffix) or SUB_MODULE_CHILDREN.get(suffix)
    if children is None:
        return None
    child_values = [values[child] for child in children if values.get(child) is not None]
    return sum(child_values, Decimal(0)) if child_values else None


def _relative_deviation(value: Decimal, reference: Decimal) -> Decimal:
    """Return how far the value is from the reference, relative to the reference."""
    if value == reference:
        return Decimal(0)
    if reference == 0:
        return Decimal("Infinity")
    return abs(value - reference) / abs(reference)


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
        missing = _unfilled(aligned, wide_values)
        if missing:
            findings.append(
                DeclaredIndicatorWithoutResults(
                    f"Indicator {code} is declared but carries no result in {', '.join(missing)} "
                    f"for material {material_id}",
                    source=WIDE_SHEET,
                )
            )
        missing_tall = [suffix for suffix in _unfilled(aligned, tall_values) if suffix in _TALL_SUFFIXES]
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


def _unfilled(suffixes: list[str], values: dict[str, Any]) -> list[str]:
    """
    Return the suffixes that carry no value. E017 forbids an aggregate stage beside its
    sub-modules, so a filled aggregate stands for its sub-modules, and the other way round.
    """
    filled = {suffix for suffix, value in values.items() if value is not None}
    covered: set[str] = set()
    for aggregate, children in AGGREGATE_CHILDREN.items():
        if aggregate in filled:
            covered.update(children)
        if filled.intersection(children):
            covered.add(aggregate)
    return [suffix for suffix in suffixes if suffix not in filled and suffix not in covered]
