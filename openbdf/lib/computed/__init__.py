"""Fill the fields the tool derives, after the tables are built and before they are validated."""

from __future__ import annotations

from openbdf.lib.converters.translators import DocumentTranslator
from openbdf.lib.validation.errors import OpenBDFValidationError
from openbdf.model.tables import ProjectRecord

from .elements import fill_bill_of_materials_elements
from .materials import fill_materials
from .project import fill_project_quantities
from .results import fill_tall_results

__all__ = ["fill_computed"]


def fill_computed(
    project: ProjectRecord,
    document_translator: DocumentTranslator | None = None,
    *,
    findings: list[OpenBDFValidationError] | None = None,
    generate_missing_lines: bool = False,
) -> list[OpenBDFValidationError]:
    """
    Fill every automatic field of a built project and return the findings, existing ones included.

    The order matters: the material reference ids pair the rows with their database line, the
    database rollups then carry the weights that the project shares divide, and a row takes
    its data type from its line.
    """
    if findings is None:
        findings = []

    fill_materials(project, findings, generate_missing_lines=generate_missing_lines)
    fill_bill_of_materials_elements(project, document_translator, findings)
    fill_tall_results(project, findings)
    fill_project_quantities(project, findings)

    return findings
