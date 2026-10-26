"""Derive the material reference ids, the project material database lines and their rollups."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Optional

from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator
from openbdf.lib.validation.collect import MaterialPair, group_by_material_pair, material_pair
from openbdf.lib.validation.errors import OpenBDFValidationError
from openbdf.model.enums.materials import OpenBDFMaterialClassification
from openbdf.model.tables import ProjectMaterialDatabaseRecord, ProjectRecord

from .write import mapped_value, report_missing, write_automatic

BOM_SHEET = COMMON_CATEGORY_PROPERTIES["bom"]["name"]
PMD_SHEET = COMMON_CATEGORY_PROPERTIES["material_database"]["name"]
SHARE_QUANTUM = Decimal("0.0001")


def fill_materials(
    project: ProjectRecord,
    document_translator: DocumentTranslator | None,
    findings: list[OpenBDFValidationError],
    *,
    generate_missing_lines: bool,
) -> None:
    """
    Give every material pair a reference id and roll its bill of materials rows up into a
    project material database line. When generate_missing_lines is set, a pair without a line
    gets one, so the workbook can be saved before the contributor fills the sheet.
    """
    lines = list(getattr(project, "project_material_database", None) or [])
    rows = getattr(project, "bill_of_materials", None) or []
    rows_by_pair = group_by_material_pair(rows)

    line_by_pair: dict[MaterialPair, ProjectMaterialDatabaseRecord] = {}
    for line in lines:
        pair = material_pair(line.custom_material_name, line.lca_dataset_material_name)
        if pair is not None:
            line_by_pair.setdefault(pair, line)

    highest_id = max((_ref_id_number(record.material_ref_id) for record in (*lines, *rows)), default=0)

    if generate_missing_lines:
        for pair, pair_rows in rows_by_pair.items():
            if pair in line_by_pair:
                continue
            highest_id += 1
            line = ProjectMaterialDatabaseRecord(
                material_ref_id=f"M{highest_id:04d}",
                custom_material_name=_first_text(pair_rows, "custom_material_name"),
                lca_dataset_material_name=_first_text(pair_rows, "lca_dataset_material_name"),
                lca_database_name=_first_text(pair_rows, "lca_database_name"),
            )
            lines.append(line)
            project.project_material_database.append(line)
            line_by_pair[pair] = line

    for pair, line in line_by_pair.items():
        pair_rows = rows_by_pair.get(pair, [])
        ref_id = _ref_id(line, pair_rows)
        if ref_id is None:
            highest_id += 1
            ref_id = f"M{highest_id:04d}"
        write_automatic(line, "material_ref_id", ref_id, findings, source=PMD_SHEET)
        for row in pair_rows:
            write_automatic(row, "material_ref_id", ref_id, findings, source=BOM_SHEET)

    rollups = []
    total_mass = Decimal(0)
    for line in lines:
        pair = material_pair(line.custom_material_name, line.lca_dataset_material_name)
        pair_rows = rows_by_pair.get(pair, []) if pair is not None else []
        mass = sum((_row_mass(row) for row in pair_rows), Decimal(0))
        total_mass += mass
        rollups.append((line, pair_rows, mass))

    for line, pair_rows, mass in rollups:
        write_automatic(line, "bom_row_count", len(pair_rows), findings, source=PMD_SHEET)
        write_automatic(line, "material_mass_kg", mass, findings, source=PMD_SHEET)
        write_automatic(line, "material_mass_share", _share(mass, total_mass), findings, source=PMD_SHEET)

    _fill_material_data_type(lines, rows, findings)
    _fill_common_material_name(rows, document_translator, findings)


def _fill_material_data_type(
    lines: list[ProjectMaterialDatabaseRecord],
    rows: list[Any],
    findings: list[OpenBDFValidationError],
) -> None:
    """Copy the data type of the project material database line onto its bill of materials rows."""
    type_by_ref_id: dict[str, Any] = {}
    for line in lines:
        if line.material_ref_id:
            type_by_ref_id.setdefault(line.material_ref_id, line.material_data_type)

    for row in rows:
        value = type_by_ref_id.get(row.material_ref_id) if row.material_ref_id else None
        write_automatic(row, "material_data_type", value, findings, source=BOM_SHEET, warn_missing=False)


def _fill_common_material_name(
    rows: list[Any],
    document_translator: DocumentTranslator | None,
    findings: list[OpenBDFValidationError],
) -> None:
    """Map the material name as built to the OpenBDF material classification, and never guess."""
    if document_translator is None:
        return

    missing: set[Any] = set()
    for row in rows:
        value, unmapped = mapped_value(
            Optional[OpenBDFMaterialClassification],
            row.custom_material_name,
            document_translator,
            OpenBDFMaterialClassification.__name__,
        )
        if unmapped:
            missing.add(row.custom_material_name)
        write_automatic(row, "common_material_name", value, findings, source=BOM_SHEET, warn_missing=False)

    report_missing(missing, findings, source=BOM_SHEET)


def _ref_id_number(material_ref_id: str | None) -> int:
    """Return the numeric suffix of an M%d material_ref_id, or 0."""
    if material_ref_id and material_ref_id.startswith("M") and material_ref_id[1:].isdigit():
        return int(material_ref_id[1:])
    return 0


def _ref_id(line: ProjectMaterialDatabaseRecord, rows: list[Any]) -> str | None:
    """Keep the reference id already written on the line or on one of its rows."""
    if line.material_ref_id:
        return line.material_ref_id
    for row in rows:
        if row.material_ref_id:
            return row.material_ref_id
    return None


def _first_text(records: list[Any], field_name: str) -> str | None:
    """Return the first non-blank value of a text field, without its surrounding spaces."""
    for record in records:
        value = (getattr(record, field_name) or "").strip()
        if value:
            return value
    return None


def _row_mass(row: Any) -> Decimal:
    """Return the mass a bill of materials row contributes, repeated once per floor unless stated."""
    repetitions = 1 if row.floor_repetition is None else row.floor_repetition
    return (row.material_weight_kg or Decimal(0)) * repetitions


def _share(part: Decimal, total: Decimal) -> Decimal:
    """Return the share of a total as a percentage from 0 to 100."""
    if not total:
        return Decimal(0)
    return (part / total * 100).quantize(SHARE_QUANTUM, rounding=ROUND_HALF_UP)
