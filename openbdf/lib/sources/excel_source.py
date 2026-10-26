from __future__ import annotations

from collections import defaultdict
from contextlib import ExitStack
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Collection, Sequence

import pandas as pd

from openbdf.lib.sources.source import SheetSource

WorkbookInput = str | Path | BinaryIO


def workbook_label(workbook: WorkbookInput, position: int) -> str:
    """Return a readable name for a workbook given as a path or as a binary file object."""

    if isinstance(workbook, (str, Path)):
        return str(workbook)
    name = getattr(workbook, "name", None)
    return name if isinstance(name, str) else f"<workbook {position}>"


def format_duplicates(duplicates: dict[str, list[WorkbookInput]]) -> str:
    lines = []
    for sheet_name, workbooks in sorted(duplicates.items()):
        labels = [workbook_label(workbook, position) for position, workbook in enumerate(workbooks)]
        lines.append(f"{sheet_name!r}: {', '.join(labels)}")
    return "; ".join(lines)


class DuplicateSheetNamesError(ValueError):
    """Raised when multiple input files contain the same sheet name."""

    def __init__(self, duplicates: dict[str, list[WorkbookInput]]):
        self.duplicates = duplicates
        super().__init__(f"Duplicate sheet names found across input files: {format_duplicates(duplicates)}")


class ExcelSheetSource(SheetSource):
    """Expose sheets from one or more Excel workbooks, given as paths or binary file objects."""

    def __init__(self, workbooks: WorkbookInput | bytes | Sequence[WorkbookInput | bytes]):
        if isinstance(workbooks, (str, Path, bytes, bytearray)) or hasattr(workbooks, "read"):
            workbooks = [workbooks]
        self._workbooks = [
            BytesIO(workbook) if isinstance(workbook, (bytes, bytearray)) else workbook for workbook in workbooks
        ]

        if not self._workbooks:
            raise ValueError("At least one input workbook is required.")

        self._stack: ExitStack | None = None
        self._workbooks_by_sheet: dict[str, pd.ExcelFile] = {}

    def __enter__(self) -> ExcelSheetSource:
        if self._stack is not None:
            raise RuntimeError("ExcelSheetSource is already open.")

        stack = ExitStack()
        try:
            readers = [
                (workbook, stack.enter_context(pd.ExcelFile(workbook, engine="calamine")))
                for workbook in self._workbooks
            ]

            sources_by_sheet: dict[str, list[tuple[WorkbookInput, pd.ExcelFile]]] = defaultdict(list)
            for workbook, reader in readers:
                for sheet_name in reader.sheet_names:
                    sources_by_sheet[sheet_name].append((workbook, reader))

            duplicates = {
                sheet_name: [workbook for workbook, _ in sources]
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
