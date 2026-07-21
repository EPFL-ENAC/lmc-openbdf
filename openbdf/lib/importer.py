from __future__ import annotations

from collections import defaultdict
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Collection, Protocol, Sequence

import pandas as pd

from openbdf.lib.converters.translators import COMMON_CATEGORY_NAMES, DocumentTranslator


class SheetSource(Protocol):
    """A named collection of tabular sheets."""

    @property
    def sheet_names(self) -> Collection[str]: ...

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Return raw sheet cells without interpreting a header row."""
        ...


@dataclass(slots=True)
class OpenBDFTables:
    """The logical tables consumed by OpenBDF model conversion."""

    project: pd.DataFrame
    bill_of_materials: pd.DataFrame
    results_wide: pd.DataFrame | None = None
    results_tall: pd.DataFrame | None = None


class DuplicateSheetNamesError(ValueError):
    """Raised when multiple input files contain the same sheet name."""

    def __init__(self, duplicates: dict[str, list[Path]]):
        self.duplicates = duplicates
        details = "; ".join(
            f"{sheet_name!r}: {', '.join(str(path) for path in paths)}"
            for sheet_name, paths in sorted(duplicates.items())
        )
        super().__init__(f"Duplicate sheet names found across input files: {details}")


class ExcelSheetSource:
    """Expose sheets from one or more Excel files through ``SheetSource``."""

    def __init__(self, paths: str | Path | Sequence[str | Path]):
        if isinstance(paths, (str, Path)):
            self._paths = [Path(paths)]
        else:
            self._paths = [Path(path) for path in paths]

        if not self._paths:
            raise ValueError("At least one input workbook is required.")

        self._stack: ExitStack | None = None
        self._workbooks_by_sheet: dict[str, pd.ExcelFile] = {}

    def __enter__(self) -> ExcelSheetSource:
        if self._stack is not None:
            raise RuntimeError("ExcelSheetSource is already open.")

        stack = ExitStack()
        try:
            workbooks = [(path, stack.enter_context(pd.ExcelFile(path))) for path in self._paths]

            sources_by_sheet: dict[str, list[tuple[Path, pd.ExcelFile]]] = defaultdict(list)
            for path, workbook in workbooks:
                for sheet_name in workbook.sheet_names:
                    sources_by_sheet[sheet_name].append((path, workbook))

            duplicates = {
                sheet_name: [path for path, _ in sources]
                for sheet_name, sources in sources_by_sheet.items()
                if len(sources) > 1
            }
            if duplicates:
                raise DuplicateSheetNamesError(duplicates)

            self._workbooks_by_sheet = {sheet_name: sources[0][1] for sheet_name, sources in sources_by_sheet.items()}
            self._stack = stack
            return self
        except Exception:
            stack.close()
            raise

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._stack is not None:
            self._stack.__exit__(exc_type, exc_value, traceback)
        self._stack = None
        self._workbooks_by_sheet = {}

    @property
    def sheet_names(self) -> Collection[str]:
        self._ensure_open()
        return self._workbooks_by_sheet.keys()

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        self._ensure_open()
        return self._workbooks_by_sheet[sheet_name].parse(sheet_name, header=None)

    def _ensure_open(self) -> None:
        if self._stack is None:
            raise RuntimeError("ExcelSheetSource must be used as a context manager.")


def load_openbdf_tables(
    source: SheetSource,
    document_translator: DocumentTranslator,
) -> OpenBDFTables | None:
    """Load and lay out the logical OpenBDF tables from a sheet source."""

    project = _load_table(source, document_translator, COMMON_CATEGORY_NAMES["project"])
    bill_of_materials = _load_table(source, document_translator, COMMON_CATEGORY_NAMES["bom"])
    if project is None or bill_of_materials is None:
        return None

    results_wide = _load_table(source, document_translator, COMMON_CATEGORY_NAMES["results_wide"])
    results_tall = _load_table(source, document_translator, COMMON_CATEGORY_NAMES["results_tall"])

    return OpenBDFTables(
        project=project.rename(columns={project.columns[0]: "field_code", project.columns[1]: "value"}).reset_index(
            drop=True
        ),
        bill_of_materials=bill_of_materials.reset_index(drop=True),
        results_wide=results_wide.reset_index(drop=True) if results_wide is not None else None,
        results_tall=results_tall.reset_index(drop=True) if results_tall is not None else None,
    )


def _load_table(
    source: SheetSource,
    document_translator: DocumentTranslator,
    translated_sheet_name: str,
) -> pd.DataFrame | None:
    translation = document_translator.get_sheet_translation(translated_sheet_name)
    if translation is None or translation.original_name not in source.sheet_names:
        return None

    return translation.translate_df(source.read_sheet(translation.original_name))
