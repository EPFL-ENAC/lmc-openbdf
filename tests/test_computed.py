from __future__ import annotations

from decimal import Decimal
from typing import Any

import pandas as pd

from openbdf.lib.computed import fill_computed
from openbdf.lib.computed.elements import fill_bill_of_materials_elements
from openbdf.lib.converters.translators import FLOOR_LEVEL_CATEGORY, DocumentTranslator
from openbdf.lib.validation.errors import AutomaticFieldSupplied, OpenBDFValidationError, UnmappedNationalValue
from openbdf.model.enums.buildings import AboveBelowGround, GFAMeasurementMethod
from openbdf.model.enums.lca import (
    AssessmentType_EN15978,
    DataWeightingBasis,
    LCADatabaseSystemModel,
    LCAStageOrModuleOrSubModule,
    LifeCycleSystemBoundary,
)
from openbdf.model.enums.materials import MaterialDataType
from openbdf.model.enums.project import ProjectPhase, ProjectPhaseCommon, ProjectUnits, RecordType
from openbdf.model.tables import (
    BuildingBillMaterialsSlimRecord,
    LCAResultsTallFullRecord,
    ProjectMaterialDatabaseRecord,
    ProjectRecord,
)

SHARE_FIELDS = (
    "lca_data_cpr_share",
    "lca_data_ecodesign_share",
    "lca_data_project_specific_share",
    "lca_data_product_specific_share",
    "lca_data_product_group_average_share",
    "lca_data_generic_share",
    "lca_data_default_share",
    "lca_data_undeclared_share",
)


def project_record(**overrides: Any) -> ProjectRecord:
    """Build a project that carries the required General Information values."""
    values: dict[str, Any] = {
        "record_type": RecordType.REAL_BUILDING,
        "project_units": ProjectUnits.METRIC,
        "project_assessment_type": AssessmentType_EN15978.TYPE_1,
        "project_gfa_method": GFAMeasurementMethod.IPMS,
        "building_gross_floor_area": Decimal(100),
        "lca_database_system_model": LCADatabaseSystemModel.CUT_OFF,
        "lca_cycle_system_boundary": LifeCycleSystemBoundary.CRADLE_TO_GATE,
    }
    values.update(overrides)
    return ProjectRecord(**values)


def database_line(name: str, material_ref_id: str | None = None, **overrides: Any) -> ProjectMaterialDatabaseRecord:
    """Build a Project Material Database line that names a material."""
    return ProjectMaterialDatabaseRecord(
        project_record_id=1,
        custom_material_name=name,
        material_ref_id=material_ref_id,
        **overrides,
    )


def bom_row(material_id: str, name: str, **overrides: Any) -> BuildingBillMaterialsSlimRecord:
    """Build a Bill of Materials row that names a material."""
    return BuildingBillMaterialsSlimRecord(
        material_id=material_id,
        custom_material_name=name,
        project_id=1,
        **overrides,
    )


class MappingTranslator:
    """Stand-in for a DocumentTranslator that returns the mapping of the test, or the value itself."""

    def __init__(self, mappings: dict[str, dict[str, str]]) -> None:
        self.mappings = mappings

    def translate(self, category: str, value: str) -> list[str]:
        return [self.mappings.get(category, {}).get(value, value)]


def test_a_contributor_value_on_a_derived_field_is_overwritten_and_reported_as_e04():
    project = project_record(
        project_material_database=[
            database_line("Concrete", "M0001", bom_row_count=99),
            database_line("Wood", "M0002", bom_row_count=1),
        ],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100)),
            bom_row("MAT-2", "Wood", material_weight_kg=Decimal(100)),
        ],
    )

    findings = fill_computed(project)

    assert [str(finding) for finding in findings] == [
        "E04: Field bom_row_count is derived; the given value was discarded"
    ]
    assert isinstance(findings[0], AutomaticFieldSupplied)
    assert findings[0].source == "Project Material Database"
    # The given 99 is replaced by the counted row. The given 1 matches the count, so it is not reported.
    assert [line.bom_row_count for line in project.project_material_database] == [1, 1]


def test_material_ref_id_is_kept_or_taken_from_a_row_or_allocated_after_the_highest_id():
    kept = project_record(
        project_material_database=[database_line("Concrete", "M0042")],
        bill_of_materials=[bom_row("MAT-1", "Concrete")],
    )

    fill_computed(kept)

    assert kept.project_material_database[0].material_ref_id == "M0042"
    assert kept.bill_of_materials[0].material_ref_id == "M0042"

    taken = project_record(
        project_material_database=[database_line("Concrete"), database_line("Wood")],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_ref_id="M0007"),
            bom_row("MAT-2", "Wood"),
        ],
    )

    fill_computed(taken)

    assert [line.material_ref_id for line in taken.project_material_database] == ["M0007", "M0008"]
    assert [row.material_ref_id for row in taken.bill_of_materials] == ["M0007", "M0008"]

    allocated = project_record(
        project_material_database=[database_line("Concrete"), database_line("Wood")],
        bill_of_materials=[bom_row("MAT-1", "Concrete"), bom_row("MAT-2", "Wood")],
    )

    fill_computed(allocated)

    assert [line.material_ref_id for line in allocated.project_material_database] == ["M0001", "M0002"]
    assert [row.material_ref_id for row in allocated.bill_of_materials] == ["M0001", "M0002"]


def test_mass_and_row_count_use_floor_repetition_and_the_share_is_a_percentage_of_the_total_mass():
    project = project_record(
        project_material_database=[database_line("Concrete", "M0001"), database_line("Wood", "M0002")],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100)),
            bom_row("MAT-2", "Wood", material_weight_kg=Decimal(50), floor_repetition=6),
            bom_row("MAT-3", "Wood", material_weight_kg=Decimal(0)),
        ],
    )

    fill_computed(project)

    concrete, wood = project.project_material_database
    # The first and the third row have no floor repetition, so one repetition counts.
    assert (concrete.bom_row_count, concrete.material_mass_kg, concrete.material_mass_share) == (
        1,
        Decimal(100),
        Decimal("25.0000"),
    )
    assert (wood.bom_row_count, wood.material_mass_kg, wood.material_mass_share) == (
        2,
        Decimal(300),
        Decimal("75.0000"),
    )


def test_the_data_type_shares_divide_the_mass_and_the_undeclared_line_falls_in_the_undeclared_share():
    project = project_record(
        project_material_database=[
            database_line("Concrete", "M0001", material_data_type=MaterialDataType.CPR_DOPC),
            database_line("Wood", "M0002", material_data_type=MaterialDataType.GENERIC),
            database_line("Steel", "M0003"),
        ],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100)),
            bom_row("MAT-2", "Wood", material_weight_kg=Decimal(200)),
            bom_row("MAT-3", "Steel", material_weight_kg=Decimal(100)),
        ],
    )

    fill_computed(project)

    # No row carries a wide result, so the shares use the mass basis of 100, 200 and 100 kg.
    assert {field_name: getattr(project, field_name) for field_name in SHARE_FIELDS} == {
        "lca_data_cpr_share": Decimal("25.0000"),
        "lca_data_ecodesign_share": Decimal("0.0000"),
        "lca_data_project_specific_share": Decimal("0.0000"),
        "lca_data_product_specific_share": Decimal("0.0000"),
        "lca_data_product_group_average_share": Decimal("0.0000"),
        "lca_data_generic_share": Decimal("50.0000"),
        "lca_data_default_share": Decimal("0.0000"),
        "lca_data_undeclared_share": Decimal("25.0000"),
    }


def test_the_weighting_basis_is_mass_and_the_shares_stay_empty_without_a_basis():
    weighted = project_record(
        project_material_database=[
            database_line("Concrete", "M0001", material_data_type=MaterialDataType.CPR_DOPC),
            database_line("Wood", "M0002", material_data_type=MaterialDataType.GENERIC),
        ],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100)),
            bom_row("MAT-2", "Wood", material_weight_kg=Decimal(300)),
        ],
    )

    fill_computed(weighted)

    # Every line has a mass and no row has a fossil A1-A3 result, so the mass weights the shares.
    assert weighted.lca_data_weighting_basis is DataWeightingBasis.MASS
    assert weighted.lca_data_cpr_share == Decimal("25.0000")
    assert weighted.lca_data_generic_share == Decimal("75.0000")

    unweighted = project_record(bill_of_materials=[bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100))])

    fill_computed(unweighted)

    # Without a database line there is no weight, so the eight shares carry no value.
    assert unweighted.lca_data_weighting_basis is None
    assert [getattr(unweighted, field_name) for field_name in SHARE_FIELDS] == [None] * len(SHARE_FIELDS)


def test_a_normal_fill_does_not_report_a_share_sum_mismatch():
    project = project_record(
        project_material_database=[
            database_line("Concrete", "M0001", material_data_type=MaterialDataType.CPR_DOPC),
            database_line("Wood", "M0002", material_data_type=MaterialDataType.GENERIC),
            database_line("Steel", "M0003"),
        ],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100)),
            bom_row("MAT-2", "Wood", material_weight_kg=Decimal(200)),
            bom_row("MAT-3", "Steel", material_weight_kg=Decimal(100)),
        ],
    )

    findings = fill_computed(project)

    # The filler divides the same weights that it adds up, so the eight shares add up to 100 on their own.
    written = [getattr(project, field_name) for field_name in SHARE_FIELDS]
    assert all(share is not None for share in written)
    assert sum((share for share in written if share is not None), Decimal(0)) == Decimal(100)
    assert [finding for finding in findings if finding.code == "E14"] == []


def test_common_floor_level_uses_the_number_mapping_then_the_label_and_reports_one_e19_per_unmapped_label():
    translator = MappingTranslator({
        FLOOR_LEVEL_CATEGORY: {"Second floor": "2"},
        AboveBelowGround.__name__: {"Second floor": "above", "OG 2": "above"},
    })
    project = project_record(
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", custom_floor_level="Second floor"),
            bom_row("MAT-2", "Wood", custom_floor_level="OG 2"),
            bom_row("MAT-3", "Steel", custom_floor_level="roof"),
            bom_row("MAT-4", "Glass", custom_floor_level="roof"),
        ],
    )
    findings: list[OpenBDFValidationError] = []

    fill_bill_of_materials_elements(project, translator, findings)

    # The first label comes from the number mapping and the second one carries its number in the text.
    assert [row.common_floor_level for row in project.bill_of_materials] == [2, 2, None, None]
    assert [str(finding) for finding in findings] == [
        "E19: 'roof' has no mapping; the field was left empty and not guessed"
    ]
    assert isinstance(findings[0], UnmappedNationalValue)
    assert findings[0].source == "Bill of Materials"


def test_a_bare_int_rule_with_an_empty_level_keeps_the_label_and_takes_its_number():
    floor_sheet = pd.DataFrame({"source": ["EG", "@INT"], "level": ["0", float("nan")]})
    translator = DocumentTranslator.from_dataframes(
        {FLOOR_LEVEL_CATEGORY: floor_sheet},
        attribute_name_col=0,
        translated_name_col=1,
    )
    project = project_record(
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", custom_floor_level="2.OG"),
            bom_row("MAT-2", "Wood", custom_floor_level="EG"),
            bom_row("MAT-3", "Steel", custom_floor_level="roof"),
        ],
    )
    findings: list[OpenBDFValidationError] = []

    fill_bill_of_materials_elements(project, translator, findings)

    # The empty level keeps the label unchanged, so the number in the label is used.
    assert translator.translate(FLOOR_LEVEL_CATEGORY, "2.OG") == ["2.OG"]
    assert [row.common_floor_level for row in project.bill_of_materials] == [2, 0, None]
    assert [str(finding) for finding in findings] == [
        "E19: 'roof' has no mapping; the field was left empty and not guessed"
    ]


def test_common_above_below_ground_prefers_the_mapping_and_else_uses_the_sign_of_the_floor_level():
    translator = MappingTranslator({
        FLOOR_LEVEL_CATEGORY: {"Basement": "1", "Roof": "-3"},
        AboveBelowGround.__name__: {"Basement": "below", "Roof": "above"},
    })
    project = project_record(
        bill_of_materials=[
            bom_row("MAT-1", "Concrete", custom_floor_level="Basement"),
            bom_row("MAT-2", "Wood", custom_floor_level="Roof"),
            bom_row("MAT-3", "Steel", custom_floor_level="-2"),
            bom_row("MAT-4", "Glass", custom_floor_level="0"),
            bom_row("MAT-5", "Brick", custom_floor_level="3"),
        ],
    )
    findings: list[OpenBDFValidationError] = []

    fill_bill_of_materials_elements(project, translator, findings)

    # The mapping sets the side of the two labels. The sign of the number sets the side of the other three.
    assert [(row.common_floor_level, row.common_above_below_ground) for row in project.bill_of_materials] == [
        (-1, AboveBelowGround.BELOW),
        (3, AboveBelowGround.ABOVE),
        (-2, AboveBelowGround.BELOW),
        (0, AboveBelowGround.ABOVE),
        (3, AboveBelowGround.ABOVE),
    ]


def test_lca_stage_module_and_submodule_are_derived_from_the_full_life_cycle_module_code():
    row = bom_row("MAT-1", "Concrete")
    tall = LCAResultsTallFullRecord(
        material_id="MAT-1",
        lca_stage_module_submodule=LCAStageOrModuleOrSubModule.A5_1,
        building_bill_materials_slim_record_id=1,
    )
    row.lca_results_tall_full_records = [tall]
    project = project_record(bill_of_materials=[row])

    fill_computed(project)

    assert tall.lca_stage is LCAStageOrModuleOrSubModule.A4_A5
    assert tall.lca_module is LCAStageOrModuleOrSubModule.A5
    assert tall.lca_submodule is LCAStageOrModuleOrSubModule.A5_1
    assert (tall.lca_stage.value, tall.lca_module.value, tall.lca_submodule.value) == ("A4-A5", "A5", "A5.1")


def test_project_phase_common_maps_the_national_phase_and_stays_empty_without_one():
    mapped = project_record(project_phase=ProjectPhase.RIBA_UK_3)

    fill_computed(mapped)

    assert mapped.project_phase_common is ProjectPhaseCommon.PHASE_3

    unmapped = project_record()

    fill_computed(unmapped)

    assert unmapped.project_phase is None
    assert unmapped.project_phase_common is None


def test_lca_completeness_score_is_a_percentage_between_zero_and_one_hundred_for_a_partly_filled_project():
    project = project_record(
        project_material_database=[database_line("Concrete", "M0001")],
        bill_of_materials=[bom_row("MAT-1", "Concrete", material_weight_kg=Decimal(100))],
    )

    fill_computed(project)

    score = project.lca_completeness_score
    assert score is not None
    assert Decimal(0) < score < Decimal(100)


def test_a_material_data_type_on_a_row_without_a_database_line_is_cleared_without_e19():
    project = project_record(
        project_material_database=[
            database_line("Concrete", "M0001", material_data_type=MaterialDataType.CPR_DOPC),
        ],
        bill_of_materials=[
            bom_row("MAT-1", "Concrete"),
            bom_row("MAT-2", "Wood", material_data_type=MaterialDataType.GENERIC),
        ],
    )

    findings = fill_computed(project)

    assert [str(finding) for finding in findings] == []
    # The row of the line takes its data type. The Wood row has no line, so its given type is discarded.
    assert [row.material_data_type for row in project.bill_of_materials] == [
        MaterialDataType.CPR_DOPC,
        None,
    ]
