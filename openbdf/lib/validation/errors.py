from __future__ import annotations

from collections.abc import Sequence
from enum import Enum


class Severity(str, Enum):
    """Severity of a validation finding."""

    INFO = "Info"
    WARNING = "Warning"
    REJECT = "Reject"


class OpenBDFValidationError(ValueError):
    """Base class of the validation findings."""

    code: str = ""
    severity: Severity = Severity.REJECT

    def __init__(self, message: str, *, source: str = "") -> None:
        super().__init__(message)
        self.message = message
        # Name of the sheet the finding comes from, used to group the terminal output.
        self.source = source

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class DeclaredIndicatorWithoutResults(OpenBDFValidationError):
    """E25: lca_<indicator>_declared is true and the aligned result columns are empty."""

    code = "E25"
    severity = Severity.WARNING


class ResultsWithoutIndicatorDeclaration(OpenBDFValidationError):
    """E26: an indicator carries results while lca_<indicator>_declared is false."""

    code = "E26"
    severity = Severity.REJECT


class OpenBDFValidationErrors(OpenBDFValidationError):
    """Every finding of one validation run, raised when at least one finding rejects the file."""

    def __init__(self, findings: Sequence[OpenBDFValidationError]) -> None:
        self.findings = list(findings)
        super().__init__("\n".join(str(finding) for finding in self.findings))

    @property
    def errors(self) -> list[OpenBDFValidationError]:
        return [finding for finding in self.findings if finding.severity is Severity.REJECT]

    @property
    def warnings(self) -> list[OpenBDFValidationError]:
        return [finding for finding in self.findings if finding.severity is Severity.WARNING]

    @property
    def infos(self) -> list[OpenBDFValidationError]:
        return [finding for finding in self.findings if finding.severity is Severity.INFO]

    def __str__(self) -> str:
        return self.message


def format_findings(findings: Sequence[OpenBDFValidationError], *, limit: int = 50) -> list[str]:
    """Format findings for the terminal, capped per source sheet so a large file stays readable."""
    grouped: dict[str, list[OpenBDFValidationError]] = {}
    for finding in findings:
        grouped.setdefault(finding.source, []).append(finding)

    lines: list[str] = []
    for source, source_findings in grouped.items():
        if source:
            lines.append(f"{source}:")
        lines.extend(f"  {finding}" for finding in source_findings[:limit])
        if len(source_findings) > limit:
            lines.append(f"  ... {len(source_findings) - limit} more findings not shown")
    return lines
