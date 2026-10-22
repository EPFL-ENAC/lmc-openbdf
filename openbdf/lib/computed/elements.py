"""Derive the harmonised storey and element classification fields of every bill of materials row."""

from __future__ import annotations

from typing import Any, Optional

from openbdf.lib.converters.translators import (
    COMMON_CATEGORY_PROPERTIES,
    FLOOR_LEVEL_CATEGORY,
    DocumentTranslator,
    PreprocessRule,
)
from openbdf.lib.validation.errors import OpenBDFValidationError
from openbdf.model.enums.buildings import AboveBelowGround
from openbdf.model.enums.element_classifications import OpenBDFBuildingElementClassification
from openbdf.model.tables import ProjectRecord

from .write import mapped_value, report_missing, write_automatic

BOM_SHEET = COMMON_CATEGORY_PROPERTIES["bom"]["name"]
ABOVE_BELOW_CATEGORY = AboveBelowGround.__name__

# The @INT rule is the parser's own way to take the number out of a label such as 'OG 2'.
INT_RULE = PreprocessRule.fromString("@INT")


def fill_bill_of_materials_elements(
    project: ProjectRecord,
    document_translator: DocumentTranslator | None,
    findings: list[OpenBDFValidationError],
) -> None:
    """Fill common_floor_level, common_above_below_ground and bec_openbdf, and never guess."""
    if document_translator is None:
        return

    missing_floor: set[Any] = set()
    missing_bec: set[Any] = set()

    for row in project.bill_of_materials:
        level, floor_unmapped = _floor_level(row.custom_floor_level, document_translator)
        if floor_unmapped:
            missing_floor.add(row.custom_floor_level)

        position, _ = mapped_value(
            Optional[AboveBelowGround],
            row.custom_floor_level,
            document_translator,
            ABOVE_BELOW_CATEGORY,
        )
        if level is not None and position is not None and level != 0:
            level = -abs(level) if position is AboveBelowGround.BELOW else abs(level)

        write_automatic(row, "common_floor_level", level, findings, source=BOM_SHEET, warn_missing=False)
        write_automatic(
            row,
            "common_above_below_ground",
            position if position is not None else _position(level),
            findings,
            source=BOM_SHEET,
            warn_missing=False,
        )

        bec, bec_unmapped = mapped_value(
            Optional[OpenBDFBuildingElementClassification],
            row.bec_custom,
            document_translator,
            OpenBDFBuildingElementClassification.__name__,
        )
        if bec_unmapped:
            missing_bec.add(row.bec_custom)
        write_automatic(row, "bec_openbdf", bec, findings, source=BOM_SHEET, warn_missing=False)

    report_missing(missing_floor | missing_bec, findings, source=BOM_SHEET)


def _floor_level(label: str | None, translator: DocumentTranslator) -> tuple[int | None, bool]:
    """Return the OpenBDF floor number of a storey label and whether that label has no mapping."""
    if label is None:
        return None, False

    translated = translator.translate(FLOOR_LEVEL_CATEGORY, label)[0]
    try:
        return int(float(str(translated))), False
    except (TypeError, ValueError):
        pass

    if translated != label:
        # The sheet matched the label and left the number out, so the label states no number.
        return None, False

    parsed = INT_RULE.execute(label)
    if parsed.valid:
        return int(parsed.value), False
    return None, True


def _position(level: int | None) -> AboveBelowGround | None:
    """Return the above/below position of a floor number. Ground level is above the natural ground."""
    if level is None:
        return None
    return AboveBelowGround.BELOW if level < 0 else AboveBelowGround.ABOVE
