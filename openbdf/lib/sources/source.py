from typing import Collection, Protocol

import pandas as pd


class SheetSource(Protocol):
    """A named collection of raw tabular sheets."""

    @property
    def sheet_names(self) -> Collection[str]: ...

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Return raw sheet cells without interpreting a header row."""
        ...
