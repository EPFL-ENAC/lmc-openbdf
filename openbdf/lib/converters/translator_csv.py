import csv
import re
from collections import defaultdict
from collections.abc import Collection
from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

# Sheet CSV files are named after a zero padded index that gives the sheet order, then the exact sheet name.
SHEET_FILE_PATTERN = re.compile(r"^(?P<index>\d+)-(?P<name>.+)\.csv$")


def sheet_csv_path(index: int, sheet_name: str) -> str:
    """The file name of a sheet, ordered by its 3-digit prefix."""
    return f"{index:03d}-{sheet_name}.csv"


def csv_dir_sheets(directory: Path) -> list[tuple[str, Path]]:
    """The sheet name and path of every sheet CSV of a directory, in sheet order."""
    if not directory.is_dir():
        raise FileNotFoundError(f"Not a directory of sheet CSV files: {directory}")

    sheets: list[tuple[int, str, Path]] = []
    invalid: list[Path] = []
    for path in sorted(directory.glob("*.csv")):
        if not path.is_file():
            continue
        match = SHEET_FILE_PATTERN.fullmatch(path.name)
        if match is None:
            invalid.append(path)
        else:
            sheets.append((int(match.group("index")), match.group("name"), path))

    if invalid:
        raise ValueError(f"CSV file names must look like {sheet_csv_path(1, 'Sheet name')}: {_file_names(invalid)}")

    paths_by_name: dict[str, list[Path]] = defaultdict(list)
    for _, sheet_name, path in sheets:
        paths_by_name[sheet_name].append(path)

    duplicated = [path for paths in paths_by_name.values() if len(paths) > 1 for path in paths]
    if duplicated:
        raise ValueError(f"Several CSV files map to the same sheet name: {_file_names(duplicated)}")

    return [(sheet_name, path) for _, sheet_name, path in sorted(sheets, key=lambda sheet: (sheet[0], sheet[1]))]


def _file_names(paths: list[Path]) -> str:
    """The file names of the given paths, comma separated and sorted."""
    return ", ".join(sorted(path.name for path in paths))


def workbook_sheets_to_csv_dir(workbook: Workbook, directory: Path, exclude: Collection[str] = ()) -> list[Path]:
    """Write every worksheet except the excluded ones as a numbered CSV file and return the written paths."""
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for sheet in workbook.worksheets:
        if sheet.title in exclude:
            continue
        path = directory / sheet_csv_path(len(written) + 1, sheet.title)
        with path.open("w", encoding="utf-8", newline="") as stream:
            csv.writer(stream, lineterminator="\n").writerows(_worksheet_rows(sheet))
        written.append(path)
    return written


def _worksheet_rows(sheet: Worksheet) -> list[list[str]]:
    """The used range of a worksheet as CSV fields, without trailing empty rows and columns."""
    last_row, last_column = _used_range(sheet)
    if last_row == 0 or last_column == 0:
        return []
    rows = sheet.iter_rows(min_row=1, max_row=last_row, max_col=last_column)
    return [[_csv_field(cell.value) for cell in row] for row in rows]


def _used_range(sheet: Worksheet) -> tuple[int, int]:
    """The last row and column of a worksheet that hold a value."""
    last_row = 0
    last_column = 0
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value is None or cell.value == "":
                continue
            last_row = max(last_row, cell.row)
            last_column = max(last_column, cell.column)
    return last_row, last_column


def _csv_field(value: Any) -> str:
    """A cell value as a CSV field: an empty field for an empty cell and plain digits for an integer."""
    if value is None:
        return ""
    if isinstance(value, int) and not isinstance(value, bool):
        return str(int(value))
    return str(value)


def csv_dir_rows(directory: Path) -> dict[str, list[list[str]]]:
    """The rows of every sheet CSV of a directory, keyed by sheet name in sheet order."""
    rows: dict[str, list[list[str]]] = {}
    for sheet_name, path in csv_dir_sheets(Path(directory)):
        with path.open(encoding="utf-8", newline="") as stream:
            rows[sheet_name] = list(csv.reader(stream))
    return rows
