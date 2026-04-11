from pathlib import Path

import pandas as pd
from lib.converters.dataframe import bom_from_dataframe, project_from_dataframe, project_package_from_dataframes
from model.tables import BuildingBillMaterialsSlimRecord


def open_openbdf_xlsx(
    xlsx_path: str | Path,
    info_sheet_name: str = "Sheet1",
    info_header_col: int = 0,
    info_values_col: int = 1,
    info_start_row: int = 0,
    bom_sheet_name: str = "Sheet1",
    bom_header_row: int = 0,
    bom_start_row: int = 0,
    bom_start_col: int = 0,
    bom_end_row: int | None = None,
    bom_end_col: int | None = None,
):
    info_raw_df = pd.read_excel(xlsx_path, sheet_name=info_sheet_name)
    info_picked = info_raw_df.iloc[info_start_row:, [info_header_col, info_values_col]]
    info_renamed = info_picked.rename(columns={info_picked.columns[0]: "field_code", info_picked.columns[1]: "value"})

    bom_raw_df = pd.read_excel(xlsx_path, sheet_name=bom_sheet_name, header=bom_header_row)
    bom_filtered = bom_raw_df.iloc[bom_start_row:bom_end_row, bom_start_col:bom_end_col].reset_index(drop=True)

    return project_package_from_dataframes(info_renamed, bom_filtered)


def open_building_bill_of_materials(
    xlsx_path: str | Path,
    sheet_name: str = "Sheet1",
    header_row: int = 0,
    start_row: int = 0,
    start_col: int = 0,
    end_row: int | None = None,
    end_col: int | None = None,
) -> list[BuildingBillMaterialsSlimRecord]:
    """Open a building bill of materials from an Excel file and return a list of BuildingBillMaterialsSlimRecord."""

    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=header_row)

    df = df.iloc[start_row:end_row, start_col:end_col].reset_index(drop=True)

    print(f"Loaded BOM dataframe with {len(df)} rows and {len(df.columns)} columns.")
    print(df.head())
    return bom_from_dataframe(df)


def open_project(
    xlsx_path: str | Path, sheet_name: str = "Sheet1", header_col: int = 0, values_col: int = 1, start_row: int = 0
):
    raw_df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    print(raw_df)

    picked = raw_df.iloc[start_row:, [header_col, values_col]]
    print(picked)

    renamed = picked.rename(columns={picked.columns[0]: "field_code", picked.columns[1]: "value"})
    print(renamed)

    return project_from_dataframe(renamed)
