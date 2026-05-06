from pathlib import Path

import pandas as pd


# TODO : best idea would to make this a global translator, you give the cli a translator file, with a sheet for the attributes names, and one sheet per enum
class CategoryTranslator:
    _translation_dict: dict[str, str]

    def __init__(self, translation_dict: dict[str, str]):
        self._translation_dict = translation_dict

    @staticmethod
    def from_dataframe(df: pd.DataFrame, attribute_name_col: int, translated_name_col: int) -> "CategoryTranslator":
        translation_dict = dict(zip(df.iloc[:, attribute_name_col], df.iloc[:, translated_name_col]))
        return CategoryTranslator(translation_dict)

    def translate(self, attribute_name: str) -> str:
        return self._translation_dict.get(attribute_name, attribute_name)


class DocumentTranslator:
    _translators: dict[str, CategoryTranslator]

    def __init__(self, translators: dict[str, CategoryTranslator]):
        self._translators = translators

    @staticmethod
    def from_dataframes(
        dfs: dict[str, pd.DataFrame], attribute_name_col: int, translated_name_col: int
    ) -> "DocumentTranslator":
        translators = {
            category_name: CategoryTranslator.from_dataframe(df, attribute_name_col, translated_name_col)
            for category_name, df in dfs.items()
        }
        return DocumentTranslator(translators)

    @staticmethod
    def from_xlsx(
        xlsx_path: str | Path, attribute_name_col: int, translated_name_col: int, header_row: int = 0
    ) -> "DocumentTranslator":
        xlsx = pd.ExcelFile(xlsx_path)
        dfs = {sheet_name: xlsx.parse(sheet_name, header=header_row) for sheet_name in xlsx.sheet_names}
        return DocumentTranslator.from_dataframes(dfs, attribute_name_col, translated_name_col)

    def translate(self, category_name: str, attribute_name: str) -> str:
        translator = self._translators.get(category_name)
        if translator is None:
            return attribute_name
        return translator.translate(attribute_name)


COMMON_CATEGORY_NAMES = {
    "project": "General Info",
    "bom": "Bill of Materials",
}
