from __future__ import annotations

from openbdf.model.enums.lca import LCAStageOrModule
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    LCAResultsTallFullRecord,
    LCAResultsWideFullRecord,
)

STAGES: tuple[tuple[LCAStageOrModule, str], ...] = (
    (LCAStageOrModule.A1_A3, "a1_a3"),
    (LCAStageOrModule.A4, "a4"),
    (LCAStageOrModule.A5, "a5"),
    (LCAStageOrModule.B1, "b1"),
    (LCAStageOrModule.B2, "b2"),
    (LCAStageOrModule.B3, "b3"),
    (LCAStageOrModule.B4, "b4"),
    (LCAStageOrModule.B5, "b5"),
    (LCAStageOrModule.B6, "b6"),
    (LCAStageOrModule.C1, "c1"),
    (LCAStageOrModule.C2, "c2"),
    (LCAStageOrModule.C3, "c3"),
    (LCAStageOrModule.C4, "c4"),
    (LCAStageOrModule.D, "d"),
    (LCAStageOrModule.D1, "d1"),
    (LCAStageOrModule.D2, "d2"),
)

_IMPACT_INDICATORS = (
    "gwp_total",
    "gwp_f",
    "gwp_b",
    "gwp_luc",
    "odp",
    "ap",
    "ep",
    "ep_af",
    "ep_am",
    "ep_t",
    "pocp",
    "sfp",
    "pofp",
    "adpmm",
    "adpf",
    "wdp",
    "pere",
    "penre",
    "pert",
    "penrt",
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
        impact_values = {indicator: getattr(wide_result, f"{indicator}_{suffix}") for indicator in _IMPACT_INDICATORS}
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
