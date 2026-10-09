from __future__ import annotations

from typing import Any, Protocol, TypeVar

from openbdf.model.lca_results import INDICATORS, STAGES
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase


class BillMaterialLike(Protocol):
    """Structural type for a bill of materials record used by wide-to-tall conversion."""

    material_id: str
    id: int | None


TallRecordT = TypeVar("TallRecordT", bound=LCAResultsTallBase)


def lca_results_wide_to_tall(
    wide_result: LCAResultsWideFullBase,
    bill_material: BillMaterialLike,
    tall_model_cls: type[TallRecordT],
) -> list[TallRecordT]:
    """Convert a wide LCA result into its populated stage/module rows."""
    if wide_result.material_id != bill_material.material_id:
        raise ValueError(
            "The wide LCA result material_id does not match the bill of materials material_id: "
            f"{wide_result.material_id!r} != {bill_material.material_id!r}"
        )

    tall_results: list[TallRecordT] = []

    for stage, suffix in STAGES:
        impact_values = {indicator.code: getattr(wide_result, f"{indicator.code}_{suffix}") for indicator in INDICATORS}
        if not any(value is not None for value in impact_values.values()):
            continue

        record_values: dict[str, Any] = {
            "material_id": wide_result.material_id,
            "lca_stage_module_submodule": stage,
            **impact_values,
        }
        if bill_material.id is not None:
            record_values["building_bill_materials_slim_record_id"] = bill_material.id

        tall_results.append(tall_model_cls(**record_values))

    return tall_results
