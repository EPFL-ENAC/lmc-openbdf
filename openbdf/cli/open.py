from pathlib import Path

import pandas as pd

from openbdf.lib.converters.attribute_translator import COMMON_CATEGORY_NAMES, DocumentTranslator
from openbdf.lib.converters.dataframe import (
    project_draft_package_from_dataframes,
    project_package_from_dataframes,
)


def open_openbdf_xlsx(
    xlsx_path: str | Path,
    attribute_translator_path: str | Path | None = None,
    attribute_translator_attribute_name_col: int = 0,
    attribute_translator_translated_name_col: int = 1,
    attribute_translator_header_row: int = 0,
    draft: bool = False,
):
    xlsx_file = pd.ExcelFile(xlsx_path)

    if attribute_translator_path is not None:
        document_translator = DocumentTranslator.from_xlsx(
            xlsx_path=attribute_translator_path,
            attribute_name_col=attribute_translator_attribute_name_col,
            translated_name_col=attribute_translator_translated_name_col,
            header_row=attribute_translator_header_row,
        )
    else:
        document_translator = DocumentTranslator()

    info_df = document_translator.get_translated_xlsx_sheet(xlsx_file, COMMON_CATEGORY_NAMES["project"])
    if info_df is None:
        return None

    info_df.rename(columns={info_df.columns[0]: "field_code", info_df.columns[1]: "value"}, inplace=True)

    bom_df = document_translator.get_translated_xlsx_sheet(xlsx_file, COMMON_CATEGORY_NAMES["bom"])
    if bom_df is None:
        return None
    bom_df = bom_df.reset_index(drop=True)

    if draft:
        return project_draft_package_from_dataframes(info_df, bom_df, document_translator=document_translator)

    return project_package_from_dataframes(info_df, bom_df, document_translator=document_translator)
