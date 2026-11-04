from __future__ import annotations

from collections import defaultdict
from contextlib import ExitStack
from typing import TYPE_CHECKING, Collection, Protocol, Sequence, cast

import pandas as pd

if TYPE_CHECKING:
    from openbdf.lib.sources.excel_source import ExcelSheetSource, ParquetSheetSource, WorkbookInput


class SheetSource(Protocol):
    """A named collection of raw tabular sheets."""

    @property
    def sheet_names(self) -> Collection[str]: ...

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Return raw sheet cells without interpreting a header row."""
        ...


class CompositeSheetSource(SheetSource):
    """Expose the sheets of several sheet sources as a single collection."""

    def __init__(self, sources: Sequence[ExcelSheetSource | ParquetSheetSource]):
        self._sources = list(sources)
        self._stack: ExitStack | None = None
        self._sources_by_sheet: dict[str, ExcelSheetSource | ParquetSheetSource] = {}

    def __enter__(self) -> CompositeSheetSource:
        if self._stack is not None:
            raise RuntimeError("CompositeSheetSource is already open.")

        # Imported here because excel_source imports this module.
        from openbdf.lib.sources.excel_source import DuplicateSheetNamesError

        stack = ExitStack()
        try:
            sources_by_sheet: dict[str, list[ExcelSheetSource | ParquetSheetSource]] = defaultdict(list)
            for source in self._sources:
                stack.enter_context(source)
                for sheet_name in source.sheet_names:
                    sources_by_sheet[sheet_name].append(source)

            duplicates = {sheet_name: sources for sheet_name, sources in sources_by_sheet.items() if len(sources) > 1}
            if duplicates:
                raise DuplicateSheetNamesError(cast("dict[str, list[WorkbookInput]]", duplicates))

            self._sources_by_sheet = {sheet_name: sources[0] for sheet_name, sources in sources_by_sheet.items()}
            self._stack = stack
            return self
        except Exception:
            stack.close()
            raise

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._stack is not None:
            self._stack.__exit__(exc_type, exc_value, traceback)
        self._stack = None
        self._sources_by_sheet = {}

    @property
    def sheet_names(self) -> Collection[str]:
        self._ensure_open()
        return self._sources_by_sheet.keys()

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        self._ensure_open()
        return self._sources_by_sheet[sheet_name].read_sheet(sheet_name)

    def _ensure_open(self) -> None:
        if self._stack is None:
            raise RuntimeError("CompositeSheetSource must be used as a context manager.")
