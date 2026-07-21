from __future__ import annotations

from collections import defaultdict
from contextlib import ExitStack
from pathlib import Path
from typing import Collection, Sequence

import pandas as pd

from openbdf.lib.sources.source import SheetSource


class DuplicateSheetNamesError(ValueError):
    """Raised when multiple input files contain the same sheet name."""

    def __init__(self, duplicates: dict[str, list[Path]]):
        self.duplicates = duplicates
        details = "; ".join(
            f"{sheet_name!r}: {', '.join(str(path) for path in paths)}"
            for sheet_name, paths in sorted(duplicates.items())
        )
        super().__init__(f"Duplicate sheet names found across input files: {details}")


class ExcelSheetSource(SheetSource):
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
