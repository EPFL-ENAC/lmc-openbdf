"""Write a computed value into a record and report what the contributor wrote there instead."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from openbdf.lib.converters.translators import DocumentTranslator
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.types.values import parse_value
from openbdf.lib.validation.errors import (
    AutomaticFieldSupplied,
    OpenBDFValidationError,
    UnmappedNationalValue,
)


def field_code(record: Any, field_name: str) -> str:
    """Return the specification field code of a field of a record."""
    field = type(record).model_fields.get(field_name)
    return get_field_code(field_name, field) if field is not None else field_name


def write_automatic(
    record: Any,
    field_name: str,
    value: Any,
    findings: list[OpenBDFValidationError],
    *,
    source: str,
    warn_missing: bool = True,
) -> None:
    """
    Write a derived value and report what the field held before.

    A field with no computed value is emptied, because an automatic cell belongs to the
    parser and never to the contributor. warn_missing is False when the caller already
    reported the unmapped value once for every row that carries it.
    """
    current = getattr(record, field_name, None)

    if value is None:
        if current is None:
            return
        if warn_missing:
            findings.append(
                UnmappedNationalValue(
                    f"Field {field_code(record, field_name)} has no computed value; "
                    "the given value was discarded and the field was left empty",
                    source=source,
                )
            )
        setattr(record, field_name, None)
        return

    if current is not None and not same_value(current, value):
        findings.append(
            AutomaticFieldSupplied(
                f"Field {field_code(record, field_name)} is derived; the given value was discarded",
                source=source,
            )
        )
    setattr(record, field_name, value)


def same_value(current: Any, value: Any) -> bool:
    """Compare a stored value with a derived one, numerically for decimals."""
    if current == value:
        return True
    if isinstance(current, Decimal) or isinstance(value, Decimal):
        try:
            return Decimal(str(current)) == Decimal(str(value))
        except (InvalidOperation, ValueError):
            return False
    return False


def mapped_value(
    annotation: Any,
    raw_value: Any,
    translator: DocumentTranslator,
    category: str,
) -> tuple[Any, bool]:
    """Return the OpenBDF value of a national value and whether that value has no mapping."""
    if raw_value is None:
        return None, False
    translated = translator.translate(category, str(raw_value))[0]
    try:
        return parse_value(annotation, translated), False
    except (TypeError, ValueError, ArithmeticError):
        return None, True


def report_missing(values: set[Any], findings: list[OpenBDFValidationError], *, source: str) -> None:
    """Warn E19 once for every distinct national value that has no mapping."""
    for value in sorted(values, key=str):
        findings.append(
            UnmappedNationalValue(f"{value!r} has no mapping; the field was left empty and not guessed", source=source)
        )
