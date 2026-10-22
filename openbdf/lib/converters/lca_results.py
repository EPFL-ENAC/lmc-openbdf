from __future__ import annotations

from typing import Any, Protocol, TypeVar, cast

from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule
from openbdf.model.lca_results import GWP_TOTAL_STAGES, INDICATORS, STAGES
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase


class BillMaterialLike(Protocol):
    """Structural type for a bill of materials record used by wide-to-tall conversion."""

    material_id: str
    id: int | None


TallRecordT = TypeVar("TallRecordT", bound=LCAResultsTallBase)


def derive_lca_stage_chain(
    stage_or_module: LCAStageOrModuleOrSubModule,
) -> tuple[
    LCAStageOrModuleOrSubModule | None,
    LCAStageOrModuleOrSubModule | None,
    LCAStageOrModuleOrSubModule | None,
]:
    """
    Derive (lca_stage, lca_module, lca_submodule) by walking the enum parent chain.

    Stage values (example 'A1-A3') have no parent, module values (example 'A5') have
    a stage parent, and sub-module values (example 'A5.1') have a module parent that
    itself has a stage parent.
    """
    parent = stage_or_module.parent_category
    if parent is None:
        return stage_or_module, None, None
    parent = cast(LCAStageOrModuleOrSubModule, parent)
    grandparent = cast("LCAStageOrModuleOrSubModule | None", parent.parent_category)
    if grandparent is not None:
        return grandparent, parent, stage_or_module
    return parent, stage_or_module, None


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

    def append_tall_record(stage: LCAStageOrModuleOrSubModule, impact_values: dict[str, Any]) -> None:
        lca_stage, lca_module, lca_submodule = derive_lca_stage_chain(stage)
        record_values: dict[str, Any] = {
            "material_id": wide_result.material_id,
            "lca_stage_module_submodule": stage,
            "lca_stage": lca_stage,
            "lca_module": lca_module,
            "lca_submodule": lca_submodule,
            **impact_values,
        }
        if bill_material.id is not None:
            record_values["building_bill_materials_slim_record_id"] = bill_material.id

        tall_results.append(tall_model_cls(**record_values))

    for stage, suffix in STAGES:
        impact_values = {indicator.code: getattr(wide_result, f"{indicator.code}_{suffix}") for indicator in INDICATORS}
        if not any(value is not None for value in impact_values.values()):
            continue

        append_tall_record(stage, impact_values)

    # The STAGES iteration covers the plain stage and module columns only; gwp_total
    # additionally carries sub-module columns (absent from STAGES) that become their
    # own tall rows with only the gwp_total indicator populated.
    covered_stages = {stage for stage, _ in STAGES}
    for stage, suffix in GWP_TOTAL_STAGES:
        if stage in covered_stages:
            continue

        gwp_total = getattr(wide_result, f"gwp_total_{suffix}")
        if gwp_total is None:
            continue

        append_tall_record(stage, {"gwp_total": gwp_total})

    return tall_results
