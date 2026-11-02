from __future__ import annotations

from collections.abc import Sequence

from openbdf.lib.validation.errors import SEVERITY_RANK, OpenBDFValidationError


def codes_table() -> list[str]:
    """Build the lines of the finding-code table, the rejects first."""
    classes = sorted(
        OpenBDFValidationError.__subclasses__(),
        key=lambda cls: (SEVERITY_RANK[cls.severity], cls.code),
    )
    rows = [(f"{cls.code}  {cls.__name__}", _raised_when(cls), cls.severity.value) for cls in classes]
    headers = ["**Error**", "**Raised when**", "**Severity**"]
    widths = [max(len(header), *(len(row[column]) for row in rows)) for column, header in enumerate(headers)]

    return [
        _row(headers, widths),
        _row(["-" * width for width in widths], widths),
        *(_row(row, widths) for row in rows),
    ]


def _row(cells: Sequence[str], widths: Sequence[int]) -> str:
    return "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)) + " |"


def _raised_when(cls: type[OpenBDFValidationError]) -> str:
    """Turn the class docstring "E001: a field ..." into a table description."""
    description = (cls.__doc__ or "").split(": ", 1)[-1].rstrip(".")
    first, _, rest = description.partition(" ")
    if "_" in first or "<" in first:
        return description
    return first.capitalize() + " " + rest if rest else first.capitalize()
