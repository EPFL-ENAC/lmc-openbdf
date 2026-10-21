from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from openbdf.lib.converters.translators import COMMON_CATEGORY_PROPERTIES, DocumentTranslator
from openbdf.lib.sources.source import SheetSource


@dataclass(slots=True)
class OpenBDFTables:
    """The logical tables consumed by OpenBDF model conversion."""

    project: pd.DataFrame
    bill_of_materials: pd.DataFrame
    project_material_database: pd.DataFrame | None = None
    results_wide: pd.DataFrame | None = None
    results_tall: pd.DataFrame | None = None

    @classmethod
    def from_source(
        cls,
        source: SheetSource,
        document_translator: DocumentTranslator,
    ) -> OpenBDFTables | None:
        """Load and lay out the logical OpenBDF tables from a sheet source."""

        project = cls._load_table(source, document_translator, "project")
        bill_of_materials = cls._load_table(source, document_translator, "bom")
        if project is None or bill_of_materials is None:
            return None

        project_material_database = cls._load_table(source, document_translator, "material_database")

        results_wide = cls._load_table(source, document_translator, "results_wide")
        results_tall = cls._load_table(source, document_translator, "results_tall")

        return cls(
            project=project.rename(columns={project.columns[0]: "field_code", project.columns[1]: "value"}),
            bill_of_materials=bill_of_materials,
            project_material_database=project_material_database,
            results_wide=results_wide,
            results_tall=results_tall,
        )

    @staticmethod
    def _load_table(
        source: SheetSource,
        document_translator: DocumentTranslator,
        category: str,
    ) -> pd.DataFrame | None:
        translation = document_translator.get_sheet_translation(COMMON_CATEGORY_PROPERTIES[category]["name"])
        if translation is None or translation.original_name not in source.sheet_names:
            return None

        return translation.translate_df(
            source.read_sheet(translation.original_name), COMMON_CATEGORY_PROPERTIES[category]["orientation"]
        )
