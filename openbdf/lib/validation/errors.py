from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Any

from pydantic import ValidationError

from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import field_metadata


class Severity(str, Enum):
    """Severity of a validation finding."""

    REJECT = "Reject"
    WARNING = "Warning"
    INFO = "Info"


# Severity from the most to the least important, so the reject findings show first.
SEVERITY_RANK = {Severity.REJECT: 0, Severity.WARNING: 1, Severity.INFO: 2}


class OpenBDFValidationError(ValueError):
    """Base class of the validation findings."""

    code: str = ""
    severity: Severity = Severity.REJECT

    def __init__(self, message: str, *, source: str = "", row: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        # Name of the sheet the finding comes from, used to group the terminal output.
        self.source = source
        # Excel row number of the finding, None when the finding is about a whole sheet.
        self.row = row

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


# Finding codes: E for Reject, W for Warning, I for Info, numbered per severity.
class MissingRequiredField(OpenBDFValidationError):
    """E001: a field whose requirement is required carries no value."""

    code = "E001"


class UnknownEnumValue(OpenBDFValidationError):
    """E002: a cell holds a value that is not a member of the field enum."""

    code = "E002"


class TypeMismatch(OpenBDFValidationError):
    """E003: a cell cannot be read as the type of its field."""

    code = "E003"


class RowCountMismatch(OpenBDFValidationError):
    """E004: the bill of materials and the wide results sheet do not have the same number of rows."""

    code = "E004"


class MaterialIdMisalignment(OpenBDFValidationError):
    """E005: two rows at the same position carry different material_id values."""

    code = "E005"


class ShareOutOfRange(OpenBDFValidationError):
    """E006: a share is outside the 0 to 100 range."""

    code = "E006"


class ShareSumMismatch(OpenBDFValidationError):
    """E007: the eight data type shares do not add up to 100."""

    code = "E007"


class FloorAreaNotPositive(OpenBDFValidationError):
    """E008: a floor area is zero or negative."""

    code = "E008"


class DuplicateFieldCode(OpenBDFValidationError):
    """E009: one sheet declares the same field code twice."""

    code = "E009"


class ResultsWithoutIndicatorDeclaration(OpenBDFValidationError):
    """E010: an indicator carries results while lca_<indicator>_declared is false."""

    code = "E010"


class ProjectMaterialDatabaseWithoutBillOfMaterialsLine(OpenBDFValidationError):
    """E011: a project material database line has no bill of materials material."""

    code = "E011"


class BillOfMaterialsWithoutProjectMaterialDatabaseLine(OpenBDFValidationError):
    """E012: a bill of materials material has no project material database line."""

    code = "E012"


class DuplicatedProjectMaterialDatabaseLine(OpenBDFValidationError):
    """E013: a bill of materials material has more than one project material database line."""

    code = "E013"


class MaterialRefIdMismatch(OpenBDFValidationError):
    """E014: bill of materials rows carry a material_ref_id that differs from their database line."""

    code = "E014"


class DuplicateMaterialRefId(OpenBDFValidationError):
    """E015: one material_ref_id names more than one project material database line."""

    code = "E015"


class DuplicateMaterialId(OpenBDFValidationError):
    """E016: two bill of materials rows share a material_id, so their tall results collide."""

    code = "E016"


class AutomaticFieldSupplied(OpenBDFValidationError):
    """W001: a field the tool derives carries a contributor value."""

    code = "W001"
    severity = Severity.WARNING


class MissingMass(OpenBDFValidationError):
    """W002: a bill of materials row carries no mass."""

    code = "W002"
    severity = Severity.WARNING


class UnmappedNationalValue(OpenBDFValidationError):
    """W003: a national value has no OpenBDF mapping, so the field keeps its value."""

    code = "W003"
    severity = Severity.WARNING


class DeclaredIndicatorWithoutResults(OpenBDFValidationError):
    """W004: lca_<indicator>_declared is true and the aligned result columns are empty."""

    code = "W004"
    severity = Severity.WARNING


class DroppedLine(OpenBDFValidationError):
    """W005: a bill of materials line that misses a required field was dropped from the project."""

    code = "W005"
    severity = Severity.WARNING


class MissingSheet(OpenBDFValidationError):
    """W006: a sheet the specification requires is missing or empty, so its content was generated."""

    code = "W006"
    severity = Severity.WARNING


class UnresolvedHeaderValue(OpenBDFValidationError):
    """W007: no column name, or several column names, carry the value of a field."""

    code = "W007"
    severity = Severity.WARNING


# Order of the sheets in the workbook, used to sort the findings the way the file is read.
SHEET_ORDER = (
    "General Information",
    "Bill of Materials",
    "Project Material Database",
    "LCA Result (Wide)",
    "LCA Result (Tall)",
)

FLOOR_AREA_FIELDS = frozenset({"building_useful_floor_area", "building_gross_floor_area"})


def sort_findings(findings: Sequence[OpenBDFValidationError]) -> list[OpenBDFValidationError]:
    """Order findings by sheet, then by severity, then by row, then by code."""
    order = {sheet: position for position, sheet in enumerate(SHEET_ORDER)}
    return sorted(
        findings,
        key=lambda finding: (order.get(finding.source, len(order)), finding.source, *_within_sheet_key(finding)),
    )


def _within_sheet_key(finding: OpenBDFValidationError) -> tuple[int, int, str]:
    """Order the findings of one sheet with the most severe first."""
    return SEVERITY_RANK[finding.severity], finding.row or 0, finding.code


def findings_from_validation_error(
    error: ValidationError,
    model_cls: type[Any],
    *,
    source: str,
    row: int | None = None,
    row_by_field: Mapping[str, int] | None = None,
    skip_fields: frozenset[str] = frozenset(),
) -> list[OpenBDFValidationError]:
    """
    Turn every field error of one pydantic ValidationError into a specification finding.

    row is the Excel row of the failing record. row_by_field gives the row of each field
    instead, for a vertical sheet where every field has its own row.

    Fields in skip_fields are left out: the parser already reported a finding for the
    cell, and validating the value it could not read would report the same cell twice.
    """
    findings: list[OpenBDFValidationError] = []

    for detail in error.errors():
        field_name = str(detail["loc"][0]) if detail["loc"] else ""
        if field_name in skip_fields:
            continue
        finding_row = row_by_field.get(field_name, row) if row_by_field else row
        field = model_cls.model_fields.get(field_name)
        metadata = field_metadata(field) if field is not None else {}
        code = metadata.get("field_code") or field_name
        expected = _type_name(field)
        kind = detail["type"]

        if kind == "missing":
            findings.append(
                MissingRequiredField(f"Field {code} is required and was not provided", source=source, row=finding_row)
            )
        elif kind == "enum":
            findings.append(
                UnknownEnumValue(
                    f"Value {detail.get('input')!r} is not a valid {expected}", source=source, row=finding_row
                )
            )
        elif kind in {"greater_than_equal", "less_than_equal"} and code.endswith("_share"):
            findings.append(ShareOutOfRange(f"Field {code} must lie between 0 and 100", source=source, row=finding_row))
        elif kind == "greater_than" and code in FLOOR_AREA_FIELDS:
            findings.append(
                FloorAreaNotPositive("Floor area must be greater than zero", source=source, row=finding_row)
            )
        else:
            findings.append(TypeMismatch(f"Field {code} expects {expected}", source=source, row=finding_row))

    return findings


def _type_name(field: Any) -> str:
    """Return the name of the type a field expects."""
    if field is None:
        return "a value"
    annotation, _ = unwrap_optional(field.annotation)
    return getattr(annotation, "__name__", str(annotation))


def format_findings(findings: Sequence[OpenBDFValidationError], *, limit: int = 10) -> list[str]:
    """Format findings for the terminal, capped per source sheet so a large file stays readable."""
    grouped: dict[str, list[OpenBDFValidationError]] = {}
    for finding in findings:
        grouped.setdefault(finding.source, []).append(finding)

    lines: list[str] = []
    for source, source_findings in grouped.items():
        if source:
            lines.append(f"{source}:")
        source_findings = sorted(source_findings, key=_within_sheet_key)
        lines.extend(f"  {_with_row(finding)}" for finding in source_findings[:limit])
        if len(source_findings) > limit:
            lines.append(f"  ... {len(source_findings) - limit} more findings not shown")
    return lines


def _with_row(finding: OpenBDFValidationError) -> str:
    """Name the row of a finding, unless its message already does."""
    if finding.row is None or finding.message.startswith("Row "):
        return str(finding)
    return f"Row {finding.row}: {finding}"
