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
    # Not used to build messages. Keep it in sync with the texts at the raise sites by hand.
    message_template: str = ""
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
    message_template = "Field <code> is required and was not provided"


class UnknownEnumValue(OpenBDFValidationError):
    """E002: a cell holds a value that is not a member of the field enum."""

    code = "E002"
    message_template = "Value <value> is not a valid <type>"


class TypeMismatch(OpenBDFValidationError):
    """E003: a cell cannot be read as the type of its field."""

    code = "E003"
    message_template = "Field <code> expects <type>"


class RowCountMismatch(OpenBDFValidationError):
    """E004: the bill of materials and the wide results sheet do not have the same number of rows."""

    code = "E004"
    message_template = "Bill of Materials has <n> rows, LCA Result (Wide) has <m>"


class MaterialIdMisalignment(OpenBDFValidationError):
    """E005: two rows at the same position carry different material_id values."""

    code = "E005"
    message_template = "Row <i>: material_id <id> in the inventory, <id> in the results"


class ShareOutOfRange(OpenBDFValidationError):
    """E006: a share is outside the 0 to 100 range."""

    code = "E006"
    message_template = "Field <code> must lie between 0 and 100"


class ShareSumMismatch(OpenBDFValidationError):
    """E007: the eight data type shares do not add up to 100."""

    code = "E007"
    message_template = "The eight data type shares must add up to 100"


class FloorAreaNotPositive(OpenBDFValidationError):
    """E008: a floor area is zero or negative."""

    code = "E008"
    message_template = "Floor area must be greater than zero"


class DuplicateFieldCode(OpenBDFValidationError):
    """E009: one sheet declares the same field code twice."""

    code = "E009"
    message_template = "Field code <code> is declared twice"


class ResultsWithoutIndicatorDeclaration(OpenBDFValidationError):
    """E010: an indicator carries results while lca_<indicator>_declared is false."""

    code = "E010"
    message_template = "Indicator <indicator> carries a result in <column> but is not declared for material <id>"


class ProjectMaterialDatabaseWithoutBillOfMaterialsLine(OpenBDFValidationError):
    """E011: a project material database line has no bill of materials material."""

    code = "E011"
    message_template = "Project material database line <material> has no bill of materials material"


class BillOfMaterialsWithoutProjectMaterialDatabaseLine(OpenBDFValidationError):
    """E012: a bill of materials material has no project material database line."""

    code = "E012"
    message_template = "Bill of materials material <material> has no project material database line"


class DuplicatedProjectMaterialDatabaseLine(OpenBDFValidationError):
    """E013: a bill of materials material has more than one project material database line."""

    code = "E013"
    message_template = "Bill of materials material <material> has <n> project material database lines"


class MaterialRefIdMismatch(OpenBDFValidationError):
    """E014: bill of materials rows carry a material_ref_id that differs from their database line."""

    code = "E014"
    message_template = "Bill of materials rows of material <material> carry material_ref_id <id> instead of <expected>"


class DuplicateMaterialRefId(OpenBDFValidationError):
    """E015: one material_ref_id names more than one project material database line."""

    code = "E015"
    message_template = "material_ref_id <id> is used by <n> project material database lines"


class DuplicateMaterialId(OpenBDFValidationError):
    """E016: two bill of materials rows share a material_id, so their tall results collide."""

    code = "E016"
    message_template = "material_id <id> is used by <n> bill of materials rows"


class AggregateAndSubModulesBothFilled(OpenBDFValidationError):
    """E017: an aggregate stage and its sub-modules carry values on one material."""

    code = "E017"
    message_template = "Module <m> and its sub-modules are both populated for material <id>"


class ModuleDInTotal(OpenBDFValidationError):
    """E018: an indicator total matches the sum that includes module D, not the sum of the modules A to C."""

    code = "E018"
    message_template = "Module D must not be added to the whole-life total"


class TotalSumMismatch(OpenBDFValidationError):
    """E019: <indicator>_total differs from the sum over the modules A to C by 5 per cent or more."""

    code = "E019"
    message_template = "<code> is <x>, the modules sum to <y>"


class ReferenceStudyPeriodMissing(OpenBDFValidationError):
    """E020: the boundary includes a B or C module and no reference study period is given."""

    code = "E020"
    message_template = "A reference study period is required beyond stage A"


class AutomaticFieldSupplied(OpenBDFValidationError):
    """W001: a field the tool derives carries a contributor value."""

    code = "W001"
    message_template = "Field <code> is derived; the given value was discarded"
    severity = Severity.WARNING


class MissingMass(OpenBDFValidationError):
    """W002: a bill of materials row carries no mass."""

    code = "W002"
    message_template = "Row <i> has no mass, material efficiency analysis is not possible"
    severity = Severity.WARNING


class UnmappedNationalValue(OpenBDFValidationError):
    """W003: a national value has no OpenBDF mapping, so the field keeps its value."""

    code = "W003"
    message_template = "<value> has no mapping; the field was left unchanged and not guessed"
    severity = Severity.WARNING


class DeclaredIndicatorWithoutResults(OpenBDFValidationError):
    """W004: lca_<indicator>_declared is true and the aligned result columns are empty."""

    code = "W004"
    message_template = "Indicator <indicator> is declared but carries no result in <column> for material <id>"
    severity = Severity.WARNING


class DroppedLine(OpenBDFValidationError):
    """W005: a bill of materials line that misses a required field was dropped from the project."""

    code = "W005"
    message_template = "Row <i>: line dropped: <reasons>"
    severity = Severity.WARNING


class MissingSheet(OpenBDFValidationError):
    """W006: a sheet the specification requires is missing or empty, so its content was generated."""

    code = "W006"
    message_template = "Sheet is missing or empty, its lines were generated from the bill of materials"
    severity = Severity.WARNING


class UnresolvedHeaderValue(OpenBDFValidationError):
    """W007: no column name, or several column names, carry the value of a field."""

    code = "W007"
    message_template = "Field <code> needs exactly one filled column, found <n>"
    severity = Severity.WARNING


class ReferenceStudyPeriodNotFifty(OpenBDFValidationError):
    """W008: an EU submission declares a reference study period other than 50 years."""

    code = "W008"
    message_template = "Regulation (EU) 2026/52 fixes the reference period at 50 years"
    severity = Severity.WARNING


class MissingAllocationApproach(OpenBDFValidationError):
    """W009: on-site renewable energy is reported and no allocation approach is given."""

    code = "W009"
    message_template = "State approach A, B1 or B2 for the embodied emissions of on-site generation"
    severity = Severity.WARNING


class SharedComponentsNotAllocated(OpenBDFValidationError):
    """W010: several buildings share the project and no allocation rule is given."""

    code = "W010"
    message_template = "State the rule used to allocate the emissions of shared components"
    severity = Severity.WARNING


class MinorTotalSumMismatch(OpenBDFValidationError):
    """W011: <indicator>_total differs from the sum over the modules A to C by less than 5 per cent."""

    code = "W011"
    message_template = "<code> is <x>, the modules sum to <y>"
    severity = Severity.WARNING


class DroppedLineWithData(OpenBDFValidationError):
    """W012: a dropped bill of materials line carried a mass or LCA results, which no total includes."""

    code = "W012"
    message_template = "Row <i>: the dropped line carried <data>, left out of every total"
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
            hidden = source_findings[limit:]
            codes = ", ".join(dict.fromkeys(finding.code for finding in hidden))
            lines.append(f"  ... {len(hidden)} more findings not shown, including: {codes}")
    return lines


def _with_row(finding: OpenBDFValidationError) -> str:
    """Name the row of a finding, unless its message already does."""
    if finding.row is None or finding.message.startswith("Row "):
        return str(finding)
    return f"Row {finding.row}: {finding}"
