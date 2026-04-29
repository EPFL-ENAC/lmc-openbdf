from pathlib import Path

import pandas as pd

from openbdf.lib.converters.attribute_translator import AttributeTranslator
from openbdf.lib.converters.dataframe import (
    bom_from_dataframe,
    load_attribute_translator_from_dataframe,
    project_from_dataframe,
    project_package_from_dataframes,
)
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.tables import BuildingBillMaterialsSlimRecord


def load_attribute_translator_from_xlsx(
    xlsx_path: str | Path,
    sheet_name: str = "Sheet1",
    attribute_name_col: str = "attribute_name",
    translated_name_col: str = "translated_name",
    header_row: int = 0,
) -> AttributeTranslator:
    """
    Load an AttributeTranslator from an Excel file containing at least two columns:
    - attribute_name_col: the original attribute name (e.g. field_code)
    - translated_name_col: the translated attribute name (e.g. human-readable name)

    The data can be in any sheet, but the column names must be consistent.
    """
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=header_row)
    return load_attribute_translator_from_dataframe(df, attribute_name_col, translated_name_col)


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
    attribute_translator_path: str | Path | None = None,
    attribute_translator_sheet: str = "Attribute Translator",
    attribute_translator_attribute_name_col: str = "attribute_name",
    attribute_translator_translated_name_col: str = "translated_name",
    attribute_translator_header_row: int = 0,
):
    info_raw_df = pd.read_excel(xlsx_path, sheet_name=info_sheet_name)
    info_picked = info_raw_df.iloc[info_start_row:, [info_header_col, info_values_col]]
    info_renamed = info_picked.rename(columns={info_picked.columns[0]: "field_code", info_picked.columns[1]: "value"})

    bom_raw_df = pd.read_excel(xlsx_path, sheet_name=bom_sheet_name, header=bom_header_row)
    bom_filtered = bom_raw_df.iloc[bom_start_row:bom_end_row, bom_start_col:bom_end_col].reset_index(drop=True)

    attribute_translator = None
    if attribute_translator_path is not None:
        attribute_translator = load_attribute_translator_from_xlsx(
            attribute_translator_path,
            sheet_name=attribute_translator_sheet,
            attribute_name_col=attribute_translator_attribute_name_col,
            translated_name_col=attribute_translator_translated_name_col,
            header_row=attribute_translator_header_row,
        )

    return project_package_from_dataframes(info_renamed, bom_filtered, attribute_translator=attribute_translator)
