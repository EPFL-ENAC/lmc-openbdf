from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Collection, Sequence

import pandas as pd

from openbdf.lib.sources.excel_source import DuplicateSheetNamesError
from openbdf.lib.sources.source import SheetSource


class ParquetSheetSource(SheetSource):
    """Expose one sheet per parquet file, given as paths, named after the file stem."""

    def __init__(self, files: Path | str | Sequence[Path | str]):
        if isinstance(files, (str, Path)):
            files = [files]
        self._files = [Path(file) for file in files]

        if not self._files:
            raise ValueError("At least one input workbook is required.")

        self._frames_by_sheet: dict[str, pd.DataFrame] = {}

    def __enter__(self) -> ParquetSheetSource:
        frames_by_sheet: dict[str, pd.DataFrame] = {}
        paths_by_sheet: dict[str, list[Path]] = defaultdict(list)
        for file in self._files:
            sheet_name = file.stem
            frames_by_sheet[sheet_name] = pd.read_parquet(file)
            paths_by_sheet[sheet_name].append(file)

        duplicates = {sheet_name: paths for sheet_name, paths in paths_by_sheet.items() if len(paths) > 1}
        if duplicates:
            raise DuplicateSheetNamesError(duplicates)

        self._frames_by_sheet = frames_by_sheet
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._frames_by_sheet = {}

    @property
    def sheet_names(self) -> Collection[str]:
        self._ensure_open()
        return self._frames_by_sheet.keys()

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        self._ensure_open()
        frame = self._frames_by_sheet[sheet_name]
        return pd.DataFrame([[*frame.columns], *frame.to_numpy().tolist()], dtype=object)

    def _ensure_open(self) -> None:
        if not self._frames_by_sheet:
            raise RuntimeError("ParquetSheetSource must be used as a context manager.")
