from __future__ import annotations

import re
from typing import Any

import pandas as pd

from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator, field_code_frame
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.validation.declared_results import check_declared_results, check_stage_totals, wide_blocks
from openbdf.lib.validation.errors import (
    BillOfMaterialsWithoutProjectMaterialDatabaseLine,
    DroppedLineWithData,
    DuplicatedProjectMaterialDatabaseLine,
    DuplicateMaterialId,
    DuplicateMaterialRefId,
    MaterialIdMisalignment,
    MaterialRefIdMismatch,
    MissingAllocationApproach,
    MissingMass,
    MissingSheet,
    OpenBDFValidationError,
    ProjectMaterialDatabaseWithoutBillOfMaterialsLine,
    ReferenceStudyPeriodMissing,
    ReferenceStudyPeriodNotFifty,
    RowCountMismatch,
    SharedComponentsNotAllocated,
)
from openbdf.model.lca_results import TOTAL_STAGE_SUFFIXES

BOM_SHEET = COMMON_CATEGORY_PROPERTIES["bom"]["name"]
PMD_SHEET = COMMON_CATEGORY_PROPERTIES["material_database"]["name"]
WIDE_SHEET = COMMON_CATEGORY_PROPERTIES["results_wide"]["name"]
GENERAL_INFO_SHEET = "General Information"

# The member states of the European Union, as ISO 3166-1 alpha-3 codes. The reference
# study period of Regulation (EU) 2026/52 applies to these submissions only.
EU_COUNTRY_CODES = frozenset({
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
})

MaterialPair = tuple[str, str | None]


def material_pair(
    custom_material_name: str | None,
    lca_dataset_material_name: str | None,
) -> MaterialPair | None:
    """
    Return the normalized pair that identifies a material, or None when it has no name.
    Names and EPD dataset names compare without surrounding spaces and without case,
    and a missing EPD dataset is the same as a blank one.
    """
    name = (custom_material_name or "").strip().casefold()
    if not name:
        return None
    return name, (lca_dataset_material_name or "").strip().casefold() or None


def material_pair_label(record: Any) -> str:
    """Describe a material pair as written in the workbook, for a finding."""
    name = (record.custom_material_name or "").strip()
    dataset = (record.lca_dataset_material_name or "").strip()
    return f"{name!r} with EPD dataset {dataset!r}" if dataset else f"{name!r} without an EPD dataset"


def group_by_material_pair(records: list[Any]) -> dict[MaterialPair, list[Any]]:
    """Group records by material pair and drop the records that carry no material name."""
    grouped: dict[MaterialPair, list[Any]] = {}
    for record in records:
        pair = material_pair(record.custom_material_name, record.lca_dataset_material_name)
        if pair is not None:
            grouped.setdefault(pair, []).append(record)
    return grouped


def check_project_material_database(project: Any) -> list[OpenBDFValidationError]:
    """
    E011 to E015. A material is the pair of its name and its EPD dataset name: every bill of
    materials material needs exactly one project material database line, the line and its
    rows must carry the same material_ref_id, and a material_ref_id must name one line only.
    """
    bom_rows_by_pair = group_by_material_pair(project.bill_of_materials)
    lines = getattr(project, "project_material_database", None) or []
    pmd_lines_by_pair = group_by_material_pair(lines)

    findings: list[OpenBDFValidationError] = []

    for pair, pair_lines in pmd_lines_by_pair.items():
        if pair not in bom_rows_by_pair:
            findings.append(
                ProjectMaterialDatabaseWithoutBillOfMaterialsLine(
                    f"Project material database line {material_pair_label(pair_lines[0])} "
                    "has no bill of materials material",
                    source=PMD_SHEET,
                )
            )

    for pair, rows in bom_rows_by_pair.items():
        if pair not in pmd_lines_by_pair:
            findings.append(
                BillOfMaterialsWithoutProjectMaterialDatabaseLine(
                    f"Bill of materials material {material_pair_label(rows[0])} has no project material database line",
                    source=BOM_SHEET,
                )
            )

    for pair, pair_lines in pmd_lines_by_pair.items():
        if pair in bom_rows_by_pair and len(pair_lines) > 1:
            findings.append(
                DuplicatedProjectMaterialDatabaseLine(
                    f"Bill of materials material {material_pair_label(pair_lines[0])} "
                    f"has {len(pair_lines)} project material database lines",
                    source=PMD_SHEET,
                )
            )

    for pair, pair_lines in pmd_lines_by_pair.items():
        if pair not in bom_rows_by_pair or len(pair_lines) != 1:
            continue
        expected = pair_lines[0].material_ref_id
        wrong_ref_ids = sorted({
            row.material_ref_id
            for row in bom_rows_by_pair[pair]
            if row.material_ref_id and row.material_ref_id != expected
        })
        if wrong_ref_ids:
            findings.append(
                MaterialRefIdMismatch(
                    f"Bill of materials rows of material {material_pair_label(pair_lines[0])} carry material_ref_id "
                    f"{', '.join(repr(ref_id) for ref_id in wrong_ref_ids)} instead of {expected!r}",
                    source=BOM_SHEET,
                )
            )

    ref_id_counts: dict[str, int] = {}
    for line in lines:
        if line.material_ref_id:
            ref_id_counts[line.material_ref_id] = ref_id_counts.get(line.material_ref_id, 0) + 1
    for ref_id, count in ref_id_counts.items():
        if count > 1:
            findings.append(
                DuplicateMaterialRefId(
                    f"material_ref_id {ref_id!r} is used by {count} project material database lines",
                    source=PMD_SHEET,
                )
            )

    return findings


def check_duplicate_material_ids(project: Any) -> list[OpenBDFValidationError]:
    """E016. Two bill of materials rows with one material_id would share a single tall result set."""
    counts: dict[str, int] = {}
    for row in project.bill_of_materials:
        if row.material_id:
            counts[row.material_id] = counts.get(row.material_id, 0) + 1

    return [
        DuplicateMaterialId(
            f"material_id {material_id!r} is used by {count} bill of materials rows",
            source=BOM_SHEET,
        )
        for material_id, count in counts.items()
        if count > 1
    ]


def check_result_row_alignment(
    bill_of_materials: pd.DataFrame,
    results_wide: pd.DataFrame | None,
) -> list[OpenBDFValidationError]:
    """
    E004 and E005. The bill of materials and the wide results sheet hold one row per material,
    so they are compared by position. The check reads the source rows, before any invalid
    line is dropped, because dropping a row would shift every later row.
    """
    if results_wide is None:
        return []
    bill_of_materials = _without_blank_rows(bill_of_materials)
    results_wide = _without_blank_rows(results_wide)

    findings: list[OpenBDFValidationError] = []
    if len(bill_of_materials) != len(results_wide):
        findings.append(
            RowCountMismatch(
                f"Bill of Materials has {len(bill_of_materials)} rows, {WIDE_SHEET} has {len(results_wide)}",
                source=WIDE_SHEET,
            )
        )

    for bom_row, bom_id, wide_id in zip(
        bill_of_materials.index,
        _material_ids(bill_of_materials),
        _material_ids(results_wide),
    ):
        if bom_id != wide_id:
            row = int(bom_row) + 1
            findings.append(
                MaterialIdMisalignment(
                    f"Row {row}: material_id {_text(bom_id)} in the inventory, {_text(wide_id)} in the results",
                    source=WIDE_SHEET,
                    row=row,
                )
            )

    return findings


def check_missing_mass(
    bill_of_materials: pd.DataFrame,
    dropped_rows: frozenset[int] = frozenset(),
) -> list[OpenBDFValidationError]:
    """
    W002. A bill of materials row without a mass cannot feed the material efficiency analysis.
    A dropped row is skipped, because it is no longer part of the project.
    """
    bill_of_materials = _without_blank_rows(bill_of_materials)
    if "material_weight_kg" not in bill_of_materials.columns:
        return []

    findings: list[OpenBDFValidationError] = []
    for row_index, row in bill_of_materials.iterrows():
        if not _is_blank(row["material_weight_kg"]):
            continue
        row_number = int(row_index) + 1
        if row_number in dropped_rows:
            continue
        findings.append(
            MissingMass(
                f"Row {row_number} has no mass, material efficiency analysis is not possible",
                source=BOM_SHEET,
                row=row_number,
            )
        )
    return findings


def check_dropped_data(
    bill_of_materials: pd.DataFrame,
    results_wide: pd.DataFrame | None,
    dropped_rows: frozenset[int],
) -> list[OpenBDFValidationError]:
    """
    W012. A dropped line leaves the project with its mass and its results, so the project
    totals are lower than the workbook's. Its results row is found by position, as in E005.
    """
    if not dropped_rows:
        return []
    bill_of_materials = _without_blank_rows(bill_of_materials)
    results = None
    if results_wide is not None:
        result_codes = {f"{code}_{suffix}" for code, columns in wide_blocks().items() for suffix, _ in columns}
        results = _without_blank_rows(results_wide)
        results = results[[column for column in results.columns if column in result_codes]]

    findings: list[OpenBDFValidationError] = []
    for position, (row_index, row) in enumerate(bill_of_materials.iterrows()):
        row_number = int(row_index) + 1
        if row_number not in dropped_rows:
            continue
        carried = []
        mass = row.get("material_weight_kg")
        if _carries_data(mass):
            carried.append(f"a mass of {mass} kg")
        if results is not None and position < len(results) and any(map(_carries_data, results.iloc[position])):
            carried.append("LCA results")
        if carried:
            findings.append(
                DroppedLineWithData(
                    f"Row {row_number}: the dropped line carried {' and '.join(carried)}, left out of every total",
                    source=BOM_SHEET,
                    row=row_number,
                )
            )
    return findings


def check_general_information(project: Any) -> list[OpenBDFValidationError]:
    """
    E020, W008, W009 and W010. The reference study period is required when the boundary
    reaches beyond stage A, an EU submission must declare 50 years, and the allocation
    fields must be filled when their trigger is present.
    """
    findings: list[OpenBDFValidationError] = []
    period = getattr(project, "lca_reference_study_period", None)
    if isinstance(period, str) and not period.strip():
        period = None
    if period is None and _boundary_reaches_b_or_c(project):
        findings.append(
            ReferenceStudyPeriodMissing(
                "A reference study period is required beyond stage A",
                source=GENERAL_INFO_SHEET,
            )
        )

    country = getattr(project, "project_country", None)
    if period is not None and country is not None and str(country).upper() in EU_COUNTRY_CODES:
        years = _study_period_years(period)
        if years is not None and years != 50:
            findings.append(
                ReferenceStudyPeriodNotFifty(
                    f"Regulation (EU) 2026/52 fixes the reference period at 50 years, "
                    f"the submission declares {period.strip()!r}",
                    source=GENERAL_INFO_SHEET,
                )
            )

    bipv = getattr(project, "building_bipv_description", None)
    if isinstance(bipv, str) and bipv.strip() and getattr(project, "lca_onsite_renewable_allocation", None) is None:
        findings.append(
            MissingAllocationApproach(
                "State approach A, B1 or B2 for the embodied emissions of on-site generation",
                source=GENERAL_INFO_SHEET,
            )
        )

    buildings = getattr(project, "project_no_of_buildings", None)
    if (
        isinstance(buildings, int)
        and buildings > 1
        and getattr(project, "lca_shared_component_allocation_rule", None) is None
    ):
        findings.append(
            SharedComponentsNotAllocated(
                "State the rule used to allocate the emissions of shared components",
                source=GENERAL_INFO_SHEET,
            )
        )
    return findings


def _boundary_reaches_b_or_c(project: Any) -> bool:
    """The declared boundary names the modules B or C, or a B or C result column carries a value."""
    boundary = getattr(project, "lca_cycle_system_boundary", None)
    if boundary is not None and str(boundary) in {"cradle_to_grave", "cradle_to_grave_d"}:
        return True
    for code, columns in wide_blocks().items():
        for suffix, _ in columns:
            if not suffix or suffix in TOTAL_STAGE_SUFFIXES or not suffix.startswith(("b", "c")):
                continue
            for material in project.bill_of_materials:
                wide = material.lca_results_full_record
                if wide is not None and getattr(wide, f"{code}_{suffix}", None) is not None:
                    return True
    return False


def _study_period_years(period: str) -> int | None:
    """Return the duration in years a period declares, or None when it cannot be judged.

    A number of 4 digits or more is read as a calendar year, not as a duration.
    """
    for match in re.finditer(r"\d+", period):
        years = int(match.group())
        if years < 1000:
            return years
    return None


def validate_project(
    project: Any,
    tables: OpenBDFTables | None = None,
    *,
    document_translator: DocumentTranslator | None = None,
    dropped_rows: frozenset[int] = frozenset(),
) -> list[OpenBDFValidationError]:
    """
    Collect every finding about a project instead of stopping at the first one.

    The sheet-level checks E004, E005, W002 and W012 need the source tables, so a project restored
    from a database is validated without them. A missing project material database sheet is
    an W006 warning, because its lines are generated from the bill of materials. dropped_rows
    holds the Excel rows the ingest dropped, which the row checks leave out.
    """
    findings = check_duplicate_material_ids(project)
    findings.extend(check_declared_results(project))
    findings.extend(check_stage_totals(project))
    findings.extend(check_general_information(project))

    if tables is None:
        return findings

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()
    bill_of_materials = field_code_frame(tables.bill_of_materials, BOM_SHEET, document_translator)

    if tables.project_material_database is None:
        findings.append(
            MissingSheet(
                "Sheet is missing or empty, its lines were generated from the bill of materials", source=PMD_SHEET
            )
        )
    else:
        findings.extend(check_project_material_database(project))

    results_wide = (
        None if tables.results_wide is None else field_code_frame(tables.results_wide, WIDE_SHEET, document_translator)
    )
    findings.extend(check_result_row_alignment(bill_of_materials, results_wide))
    findings.extend(check_missing_mass(bill_of_materials, dropped_rows))
    findings.extend(check_dropped_data(bill_of_materials, results_wide, dropped_rows))
    return findings


def _without_blank_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop the empty rows of a formatted sheet, which are not data rows."""
    return frame[~frame.apply(lambda row: all(_is_blank(value) for value in row), axis=1)]


def _material_ids(frame: pd.DataFrame) -> list[str | None]:
    """Return the material_id of each row, or the ids the parser generates when the sheet has none."""
    if "material_id" not in frame.columns:
        return [f"MAT-{position}" for position in range(1, len(frame) + 1)]
    return [None if _is_blank(value) else str(value) for value in frame["material_id"]]


def _is_blank(value: Any) -> bool:
    """A cell is blank when it is empty, holds only spaces, or holds the '…' placeholder of an example row."""
    return bool(pd.isna(value)) or (isinstance(value, str) and value.strip() in {"", "…", "..."})


def _carries_data(value: Any) -> bool:
    """A cell carries data when it is not blank and not a zero, which adds nothing to a total."""
    if _is_blank(value):
        return False
    try:
        return float(value) != 0
    except (TypeError, ValueError):
        return True


def _text(value: str | None) -> str:
    return "<empty>" if value is None else value
