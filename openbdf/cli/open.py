from pathlib import Path

import pandas as pd

from openbdf.lib.converters.dataframe import (
    project_draft_package_from_dataframes,
    project_package_from_dataframes,
)
from openbdf.lib.converters.translators import COMMON_CATEGORY_NAMES, DocumentTranslator


def open_openbdf_xlsx(
    xlsx_path: str | Path,
    translator_path: str | Path | None = None,
    translator_attribute_name_col: int = 0,
    translator_translated_name_col: int = 1,
    translator_header_row: int = 0,
    draft: bool = False,
):
    xlsx_file = pd.ExcelFile(xlsx_path)
    print(xlsx_file.sheet_names)

    if translator_path:
        document_translator = DocumentTranslator.from_xlsx(
            xlsx_path=translator_path,
            attribute_name_col=translator_attribute_name_col,
            translated_name_col=translator_translated_name_col,
            header_row=translator_header_row,
        )
    else:
        document_translator = DocumentTranslator.default_openbdf_translator()

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

    results_tall_df = document_translator.get_translated_xlsx_sheet(xlsx_file, COMMON_CATEGORY_NAMES["results_tall"])
    if results_tall_df is not None:
        results_tall_df = results_tall_df.reset_index(drop=True)
    results_wide_df = document_translator.get_translated_xlsx_sheet(xlsx_file, COMMON_CATEGORY_NAMES["results_wide"])
    if results_wide_df is not None:
        results_wide_df = results_wide_df.reset_index(drop=True)

    return project_package_from_dataframes(
        info_df,
        bom_df,
        results_tall_df=results_tall_df,
        results_wide_df=results_wide_df,
        document_translator=document_translator,
    )
