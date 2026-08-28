from __future__ import annotations

from openbdf.model.lca_results import INDICATORS, STAGES
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    LCAResultsTallFullRecord,
    LCAResultsWideFullRecord,
)


def lca_results_wide_to_tall(
    wide_result: LCAResultsWideFullRecord,
    bill_material: BuildingBillMaterialsSlimRecord,
) -> list[LCAResultsTallFullRecord]:
    """Convert a wide LCA result into its populated stage/module rows."""
    if wide_result.material_id != bill_material.material_id:
        raise ValueError(
            "The wide LCA result material_id does not match the bill of materials material_id: "
            f"{wide_result.material_id!r} != {bill_material.material_id!r}"
        )

    tall_results: list[LCAResultsTallFullRecord] = []

    for stage, suffix in STAGES:
        impact_values = {indicator.code: getattr(wide_result, f"{indicator.code}_{suffix}") for indicator in INDICATORS}
        if not any(value is not None for value in impact_values.values()):
            continue

        record_values: dict[str, object] = {
            "material_id": wide_result.material_id,
            "lca_service_life": bill_material.lca_service_life,
            "lca_stage_or_module": stage,
            **impact_values,
        }
        if bill_material.id is not None:
            record_values["building_bill_materials_slim_record_id"] = bill_material.id

        tall_results.append(LCAResultsTallFullRecord(**record_values))

    return tall_results
