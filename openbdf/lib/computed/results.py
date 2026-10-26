"""Derive the stage, module and sub-module of every tall result row from its full module code."""

from __future__ import annotations

from openbdf.lib.converters.lca_results import derive_lca_stage_chain
from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES
from openbdf.lib.validation.errors import OpenBDFValidationError
from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule
from openbdf.model.tables import ProjectRecord

from .write import write_automatic

TALL_SHEET = COMMON_CATEGORY_PROPERTIES["results_tall"]["name"]


def fill_tall_results(project: ProjectRecord, findings: list[OpenBDFValidationError]) -> None:
    """Write lca_stage, lca_module and lca_submodule from lca_stage_module_submodule."""
    for row in getattr(project, "bill_of_materials", None) or []:
        for tall in row.lca_results_tall_full_records:
            stage, module, submodule = _chain(tall.lca_stage_module_submodule)
            write_automatic(tall, "lca_stage", stage, findings, source=TALL_SHEET)
            write_automatic(tall, "lca_module", module, findings, source=TALL_SHEET)
            write_automatic(tall, "lca_submodule", submodule, findings, source=TALL_SHEET)


def _chain(
    code: LCAStageOrModuleOrSubModule | None,
) -> tuple[LCAStageOrModuleOrSubModule | None, LCAStageOrModuleOrSubModule | None, LCAStageOrModuleOrSubModule | None]:
    """Return the stage, module and sub-module of a life cycle module code."""
    if not isinstance(code, LCAStageOrModuleOrSubModule):
        return None, None, None
    return derive_lca_stage_chain(code)
