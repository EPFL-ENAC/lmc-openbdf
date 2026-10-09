from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from openbdf.lib.converters.lca_results import STAGES, lca_results_wide_to_tall
from openbdf.model.enums.buildings import AboveBelowGround
from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    LCAResultsTallFullRecord,
    LCAResultsWideFullRecord,
)


def bill_material(
    *,
    material_id: str = "mat-1",
    record_id: int | None = 42,
    lca_service_life: Decimal = Decimal(50),
) -> BuildingBillMaterialsSlimRecord:
    return BuildingBillMaterialsSlimRecord(
        id=record_id,
        material_id=material_id,
        material_name_custom="Test material",
        above_below_ground=AboveBelowGround.ABOVE,
        lca_service_life=lca_service_life,
        project_id=1,
    )


def wide_result(*, material_id: str = "mat-1", **values: Any) -> LCAResultsWideFullRecord:
    fields: dict[str, Any] = {
        "material_id": material_id,
        "gwp_total_a1_a3": Decimal(1),
        "gwp_total": Decimal(999),
        "building_bill_materials_slim_record_id": 42,
        **values,
    }
    return LCAResultsWideFullRecord(**fields)


def test_maps_all_supported_stages_in_stable_order():
    stage_values: dict[str, Any] = {
        f"gwp_f_{suffix}": Decimal(index) for index, (_, suffix) in enumerate(STAGES, start=1)
    }

    results = lca_results_wide_to_tall(
        wide_result(**stage_values),
        bill_material(lca_service_life=Decimal(60)),
        LCAResultsTallFullRecord,
    )

    assert [result.lca_stage_or_module for result in results] == [stage for stage, _ in STAGES]
    assert [result.gwp_f for result in results] == [Decimal(index) for index in range(1, len(STAGES) + 1)]


def test_combines_indicators_for_the_same_stage_and_omits_empty_stages():
    exact_value = Decimal("2.500")
    results = lca_results_wide_to_tall(
        wide_result(
            gwp_f_a4=exact_value,
            odp_a4=Decimal("0.003"),
            penrt_b6=Decimal(0),
            ap_c2=Decimal("7.25"),
        ),
        bill_material(lca_service_life=Decimal(75)),
        LCAResultsTallFullRecord,
    )

    assert [result.lca_stage_or_module for result in results] == [
        LCAStageOrModuleOrSubModule.A1_A3,
        LCAStageOrModuleOrSubModule.A4,
        LCAStageOrModuleOrSubModule.B6,
        LCAStageOrModuleOrSubModule.C2,
    ]
    assert results[1].gwp_f is exact_value
    assert results[1].odp == Decimal("0.003")
    assert results[1].ap is None
    assert results[2].penrt == Decimal(0)
    assert results[3].ap == Decimal("7.25")


def test_ignores_overall_summary_fields():
    results = lca_results_wide_to_tall(
        wide_result(odp_total=Decimal(123)),
        bill_material(),
        LCAResultsTallFullRecord,
    )

    assert len(results) == 1
    assert results[0].lca_stage_or_module is LCAStageOrModuleOrSubModule.A1_A3
    assert results[0].odp is None


@pytest.mark.parametrize("record_id", [42, None])
def test_copies_identifiers_and_service_life_without_attaching_relationships(record_id: int | None):
    wide = wide_result()
    service_life = Decimal("80.00")
    bom = bill_material(record_id=record_id, lca_service_life=service_life)
    wide_before = wide.model_dump()
    bom_before = bom.model_dump()

    results = lca_results_wide_to_tall(wide, bom, LCAResultsTallFullRecord)

    assert all(result.material_id == "mat-1" for result in results)
    assert all(result.lca_service_life is service_life for result in results)
    assert all(result.building_bill_materials_slim_record_id == record_id for result in results)
    assert all(result.building_bill_materials_slim_record is None for result in results)
    assert bom.lca_results_tall_full_records == []
    assert wide.model_dump() == wide_before
    assert bom.model_dump() == bom_before


def test_rejects_mismatched_material_ids():
    with pytest.raises(ValueError, match="material_id does not match"):
        lca_results_wide_to_tall(
            wide_result(material_id="wide-material"),
            bill_material(material_id="bom-material"),
            LCAResultsTallFullRecord,
        )
