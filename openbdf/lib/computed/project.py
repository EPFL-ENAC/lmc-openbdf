"""Derive the project level data quality fields: the common phase, the weighted shares and completeness."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import field_metadata
from openbdf.lib.validation.collect import group_by_material_pair, material_pair
from openbdf.lib.validation.errors import OpenBDFValidationError, ShareSumMismatch
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.enums.lca import DataWeightingBasis
from openbdf.model.enums.materials import MaterialDataType
from openbdf.model.enums.project import ProjectPhase, ProjectPhaseCommon
from openbdf.model.enums.requirement import Requirement, requirement_of
from openbdf.model.general_info import ProjectRecordBase
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase
from openbdf.model.tables import ProjectRecord

from .write import write_automatic

PROJECT_SHEET = COMMON_CATEGORY_PROPERTIES["project"]["name"]
SHARE_QUANTUM = Decimal("0.0001")
SHARE_TOLERANCE = Decimal("0.1")

# The common definition of the design steps is an OpenBDF enum, so the mapping between the
# national phase and the common phase is fixed in the code and not in a translator sheet.
PHASE_COMMON: dict[ProjectPhase, ProjectPhaseCommon] = {
    ProjectPhase.RIBA_UK_0: ProjectPhaseCommon.PHASE_0,
    ProjectPhase.RIBA_UK_1: ProjectPhaseCommon.PHASE_1,
    ProjectPhase.RIBA_UK_2: ProjectPhaseCommon.PHASE_2,
    ProjectPhase.RIBA_UK_3: ProjectPhaseCommon.PHASE_3,
    ProjectPhase.RIBA_UK_4: ProjectPhaseCommon.PHASE_4,
    ProjectPhase.RIBA_UK_5: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.RIBA_UK_6: ProjectPhaseCommon.PHASE_6,
    ProjectPhase.RIBA_UK_7: ProjectPhaseCommon.PHASE_7,
    ProjectPhase.HOAI_DE_LP1: ProjectPhaseCommon.PHASE_1,
    ProjectPhase.HOAI_DE_LP2: ProjectPhaseCommon.PHASE_2,
    ProjectPhase.HOAI_DE_LP3: ProjectPhaseCommon.PHASE_3,
    ProjectPhase.HOAI_DE_LP4: ProjectPhaseCommon.PHASE_4,
    ProjectPhase.HOAI_DE_LP5: ProjectPhaseCommon.PHASE_4,
    ProjectPhase.HOAI_DE_LP6: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.HOAI_DE_LP7: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.HOAI_DE_LP8: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.HOAI_DE_LP9: ProjectPhaseCommon.PHASE_6,
    ProjectPhase.AIA_US_SD: ProjectPhaseCommon.PHASE_2,
    ProjectPhase.AIA_US_DD: ProjectPhaseCommon.PHASE_3,
    ProjectPhase.AIA_US_CD: ProjectPhaseCommon.PHASE_4,
    ProjectPhase.AIA_US_BN: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.AIA_US_CA: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.SIA_CH_1: ProjectPhaseCommon.PHASE_0,
    ProjectPhase.SIA_CH_2: ProjectPhaseCommon.PHASE_1,
    ProjectPhase.SIA_CH_3: ProjectPhaseCommon.PHASE_3,
    ProjectPhase.SIA_CH_4: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.SIA_CH_5: ProjectPhaseCommon.PHASE_5,
    ProjectPhase.SIA_CH_6: ProjectPhaseCommon.PHASE_7,
    ProjectPhase.GBDI_END_OF_USE: ProjectPhaseCommon.PHASE_8,
    ProjectPhase.OTHER_NATIONAL: ProjectPhaseCommon.OTHER,
}

SHARE_FIELD: dict[MaterialDataType, str] = {
    MaterialDataType.CPR_DOPC: "lca_data_cpr_share",
    MaterialDataType.ECODESIGN: "lca_data_ecodesign_share",
    MaterialDataType.PROJECT_SPECIFIC: "lca_data_project_specific_share",
    MaterialDataType.PRODUCT_SPECIFIC: "lca_data_product_specific_share",
    MaterialDataType.PRODUCT_GROUP_AVERAGE: "lca_data_product_group_average_share",
    MaterialDataType.GENERIC: "lca_data_generic_share",
    MaterialDataType.DEFAULT_VALUE: "lca_data_default_share",
}

SHARE_FIELDS = (*SHARE_FIELD.values(), "lca_data_undeclared_share")

COUNTED_REQUIREMENTS = (Requirement.REQUIRED, Requirement.STRONGLY_RECOMMENDED)


def fill_project_quantities(project: ProjectRecord, findings: list[OpenBDFValidationError]) -> None:
    """Fill the common project phase, the data quality shares and the completeness score."""
    write_automatic(
        project,
        "project_phase_common",
        PHASE_COMMON.get(project.project_phase) if project.project_phase is not None else None,
        findings,
        source=PROJECT_SHEET,
    )

    basis, weights = _weights(project)
    write_automatic(project, "lca_data_weighting_basis", basis, findings, source=PROJECT_SHEET)
    _fill_shares(project, basis, weights, findings)

    write_automatic(project, "lca_completeness_score", _completeness(project), findings, source=PROJECT_SHEET)


def _weights(project: ProjectRecord) -> tuple[DataWeightingBasis | None, dict[int, Decimal]]:
    """Return the weighting basis of the shares and the weight of every database line."""
    lines = list(getattr(project, "project_material_database", None) or [])
    if not lines:
        return None, {}

    rows_by_pair = group_by_material_pair(getattr(project, "bill_of_materials", None) or [])

    fossil = _fossil_weights(lines, rows_by_pair)
    if fossil is not None:
        return DataWeightingBasis.GWP_FOSSIL_A1_A3, fossil

    if all(line.material_mass_kg is not None for line in lines):
        return DataWeightingBasis.MASS, {id(line): line.material_mass_kg for line in lines}

    return None, {}


def _fossil_weights(lines: list[Any], rows_by_pair: dict[Any, list[Any]]) -> dict[int, Decimal] | None:
    """Return the fossil A1-A3 weight of every line, or None when a line has no such result."""
    weights: dict[int, Decimal] = {}
    for line in lines:
        total = Decimal(0)
        for row in rows_by_pair.get(material_pair(line.custom_material_name, line.lca_dataset_material_name), []):
            value = getattr(row.lca_results_full_record, "gwp_f_a1_a3", None)
            if value is None:
                return None
            total += value * (row.floor_repetition or 1)
        weights[id(line)] = total
    return weights


def _fill_shares(
    project: ProjectRecord,
    basis: DataWeightingBasis | None,
    weights: dict[int, Decimal],
    findings: list[OpenBDFValidationError],
) -> None:
    """Spread the weights of the database lines over the eight data type shares."""
    lines = list(getattr(project, "project_material_database", None) or [])
    total = sum((weights.get(id(line), Decimal(0)) for line in lines), Decimal(0))

    if basis is None or total <= 0:
        for field_name in SHARE_FIELDS:
            write_automatic(project, field_name, None, findings, source=PROJECT_SHEET)
        return

    shares = dict.fromkeys(SHARE_FIELDS, Decimal(0))
    for line in lines:
        field_name = SHARE_FIELD.get(line.material_data_type, "lca_data_undeclared_share")
        shares[field_name] += weights.get(id(line), Decimal(0)) / total * 100

    for field_name, share in shares.items():
        write_automatic(
            project,
            field_name,
            share.quantize(SHARE_QUANTUM, rounding=ROUND_HALF_UP),
            findings,
            source=PROJECT_SHEET,
        )

    written = [getattr(project, field_name) for field_name in SHARE_FIELDS]
    if all(share is not None for share in written) and abs(sum(written, Decimal(0)) - 100) > SHARE_TOLERANCE:
        findings.append(ShareSumMismatch("The eight data type shares must add up to 100", source=PROJECT_SHEET))


def _completeness(project: ProjectRecord) -> Decimal | None:
    """
    Return the percentage of the required and strongly recommended fields that carry a value.

    A field that repeats over the rows of a sheet counts once, and it is filled when any
    row carries a value. Automatic fields are left out: the tool writes them, so they say
    nothing about the submission. An empty sheet is left out too.
    """
    counted = 0
    filled = 0

    for model_cls, records in _sheets(project):
        if not records:
            continue
        for field_name, field in model_cls.model_fields.items():
            _, optional = unwrap_optional(field.annotation)
            if requirement_of(field_metadata(field), optional) not in COUNTED_REQUIREMENTS:
                continue
            counted += 1
            if any(getattr(record, field_name, None) is not None for record in records):
                filled += 1

    if not counted:
        return None
    return (Decimal(filled) / Decimal(counted) * 100).quantize(SHARE_QUANTUM, rounding=ROUND_HALF_UP)


def _sheets(project: ProjectRecord) -> list[tuple[type[Any], list[Any]]]:
    """Return the model and the records of every sheet of the project."""
    bill_of_materials = getattr(project, "bill_of_materials", None) or []
    return [
        (ProjectRecordBase, [project]),
        (BuildingBillMaterialsSlimRecordBase, bill_of_materials),
        (ProjectMaterialDatabaseBase, list(getattr(project, "project_material_database", None) or [])),
        (
            LCAResultsTallBase,
            [tall for row in bill_of_materials for tall in row.lca_results_tall_full_records],
        ),
    ]
