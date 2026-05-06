from pathlib import Path

import pandas as pd

from openbdf.lib.converters.attribute_translator import DocumentTranslator
from openbdf.lib.converters.dataframe import (
    project_package_from_dataframes,
)


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
    attribute_translator_attribute_name_col: int = 0,
    attribute_translator_translated_name_col: int = 1,
    attribute_translator_header_row: int = 0,
):
    info_raw_df = pd.read_excel(xlsx_path, sheet_name=info_sheet_name)
    info_picked = info_raw_df.iloc[info_start_row:, [info_header_col, info_values_col]]
    info_renamed = info_picked.rename(columns={info_picked.columns[0]: "field_code", info_picked.columns[1]: "value"})

    bom_raw_df = pd.read_excel(xlsx_path, sheet_name=bom_sheet_name, header=bom_header_row)
    bom_filtered = bom_raw_df.iloc[bom_start_row:bom_end_row, bom_start_col:bom_end_col].reset_index(drop=True)

    document_translator = None
    if attribute_translator_path is not None:
        document_translator = DocumentTranslator.from_xlsx(
            xlsx_path=attribute_translator_path,
            attribute_name_col=attribute_translator_attribute_name_col,
            translated_name_col=attribute_translator_translated_name_col,
            header_row=attribute_translator_header_row,
        )

    return project_package_from_dataframes(info_renamed, bom_filtered, document_translator=document_translator)
