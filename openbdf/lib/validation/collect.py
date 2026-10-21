from __future__ import annotations

from typing import Any

import pandas as pd

from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.validation.declared_results import check_declared_results
from openbdf.lib.validation.errors import (
    BillOfMaterialsWithoutProjectMaterialDatabaseLine,
    DuplicatedProjectMaterialDatabaseLine,
    DuplicateMaterialId,
    DuplicateMaterialRefId,
    MaterialIdMisalignment,
    MaterialRefIdMismatch,
    MissingMass,
    MissingRequiredField,
    OpenBDFValidationError,
    ProjectMaterialDatabaseWithoutBillOfMaterialsLine,
    RowCountMismatch,
)

BOM_SHEET = COMMON_CATEGORY_PROPERTIES["bom"]["name"]
PMD_SHEET = COMMON_CATEGORY_PROPERTIES["material_database"]["name"]
WIDE_SHEET = COMMON_CATEGORY_PROPERTIES["results_wide"]["name"]

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
    E27 to E31. A material is the pair of its name and its EPD dataset name: every bill of
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
    """E32. Two bill of materials rows with one material_id would share a single tall result set."""
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
    E05 and E06. The bill of materials and the wide results sheet hold one row per material,
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
    E16. A bill of materials row without a mass cannot feed the material efficiency analysis.
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


def validate_project(
    project: Any,
    tables: OpenBDFTables | None = None,
    *,
    document_translator: DocumentTranslator | None = None,
    draft: bool = False,
    dropped_rows: frozenset[int] = frozenset(),
) -> list[OpenBDFValidationError]:
    """
    Collect every finding about a project instead of stopping at the first one.

    The sheet-level checks E05, E06 and E16 need the source tables, so a project restored
    from a database is validated without them. A missing sheet rejects a strict open but
    is tolerated in draft mode, where the missing lines are generated. dropped_rows holds
    the Excel rows the ingest dropped, which the row checks leave out.
    """
    findings = check_duplicate_material_ids(project)
    findings.extend(check_declared_results(project))

    if tables is None:
        return findings

    if document_translator is None:
        document_translator = DocumentTranslator.default_openbdf_translator()
    bill_of_materials = field_code_frame(tables.bill_of_materials, BOM_SHEET, document_translator)

    if tables.project_material_database is None:
        if not draft:
            findings.append(
                MissingRequiredField(
                    "Sheet is missing or empty",
                    source=PMD_SHEET,
                )
            )
    else:
        findings.extend(check_project_material_database(project))

    results_wide = (
        None if tables.results_wide is None else field_code_frame(tables.results_wide, WIDE_SHEET, document_translator)
    )
    findings.extend(check_result_row_alignment(bill_of_materials, results_wide))
    findings.extend(check_missing_mass(bill_of_materials, dropped_rows))
    return findings


def field_code_frame(frame: pd.DataFrame, category: str, document_translator: DocumentTranslator) -> pd.DataFrame:
    """Rename the raw sheet columns to their field codes, ignoring the columns the sheets do not use."""
    columns: dict[str, pd.Series] = {}
    for column in frame.columns:
        for field_code in document_translator.translate(category, str(column)):
            columns[field_code] = frame[column]
    return pd.DataFrame(columns, index=frame.index)


def _without_blank_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop the empty rows of a formatted sheet, which are not data rows."""
    return frame[~frame.apply(lambda row: all(_is_blank(value) for value in row), axis=1)]


def _material_ids(frame: pd.DataFrame) -> list[str | None]:
    """Return the material_id of each row, or the ids the parser generates when the sheet has none."""
    if "material_id" not in frame.columns:
        return [f"MAT-{position}" for position in range(1, len(frame) + 1)]
    return [None if _is_blank(value) else str(value) for value in frame["material_id"]]


def _is_blank(value: Any) -> bool:
    return bool(pd.isna(value)) or (isinstance(value, str) and not value.strip())


def _text(value: str | None) -> str:
    return "<empty>" if value is None else value
