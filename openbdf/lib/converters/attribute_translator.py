from pathlib import Path
from typing import Literal

import pandas as pd
from pydantic import BaseModel


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


class GeneralInfoSheetTranslator(BaseModel):
    header_row: int = 0
    values_col: int = 1
    start_row: int = 0

    @staticmethod
    def from_dict(config: dict[str, int]) -> "GeneralInfoSheetTranslator":
        return GeneralInfoSheetTranslator(
            header_row=config.get("info_header_row", 0),
            values_col=config.get("info_values_col", 1),
            start_row=config.get("info_start_row", 0),
        )


class BillOfMaterialsSheetTranslator(BaseModel):
    header_row: int = 0
    start_row: int = 0
    start_col: int = 0
    end_row: int | None = None
    end_col: int | None = None

    @staticmethod
    def from_dict(config: dict[str, int]) -> "BillOfMaterialsSheetTranslator":
        return BillOfMaterialsSheetTranslator(
            header_row=config.get("bom_header_row", 0),
            start_row=config.get("bom_start_row", 0),
            start_col=config.get("bom_start_col", 0),
            end_row=config.get("bom_end_row"),
            end_col=config.get("bom_end_col"),
        )


class SheetTranslation(BaseModel):
    original_name: str
    translated_name: str
    orientation: Literal["horizontal", "vertical"]
    header_row: int = 0

    # attributes for vertical sheets
    header_col: int | None = None
    values_col: int | None = None

    # attributes for horizontal sheets
    start_row: int | None = None
    start_col: int | None = None
    end_row: int | None = None
    end_col: int | None = None

    def __post_init__(self):
        if self.orientation == "vertical":
            if self.header_col is None or self.values_col is None:
                raise ValueError("For vertical sheets, header_col and values_col must be provided.")
        elif self.orientation == "horizontal":
            if self.start_row is None or self.start_col is None:
                raise ValueError("For horizontal sheets, start_row and start_col must be provided.")
        else:
            raise ValueError("Orientation must be either 'horizontal' or 'vertical'.")

    def translate_df(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.orientation == "vertical":
            return df.iloc[self.header_row :, [self.header_col, self.values_col]]
        elif self.orientation == "horizontal":
            header = df.iloc[self.header_row or 0, (self.start_col or 0) : self.end_col]  # DEBUG
            values = df.iloc[(self.start_row or 1) : self.end_row, (self.start_col or 0) : self.end_col]
            return pd.DataFrame(values.values, columns=header.values)
        else:
            raise ValueError("Orientation must be either 'horizontal' or 'vertical'.")


class TranslationsLibrary:
    _sheets_translations: list[SheetTranslation]
    _original_name_to_index: dict[str, int]
    _translated_to_original_index: dict[str, int]

    def __init__(self, sheets_types_translations: list[SheetTranslation]):
        self._sheets_translations = sheets_types_translations
        self._original_name_to_index = {
            translation.original_name: index for index, translation in enumerate(sheets_types_translations)
        }
        self._translated_to_original_index = {
            translation.translated_name: index for index, translation in enumerate(sheets_types_translations)
        }

    def get_translation(self, original_name: str) -> SheetTranslation | None:
        index = self._original_name_to_index.get(original_name)
        if index is not None:
            return self._sheets_translations[index]
        return None

    def get_translation_by_translated_name(self, translated_name: str) -> SheetTranslation | None:
        index = self._translated_to_original_index.get(translated_name)
        if index is not None:
            return self._sheets_translations[index]
        return None

    @staticmethod
    def from_dataframe(df: pd.DataFrame) -> "TranslationsLibrary":
        translations = []

        clean_df = df.astype(object).replace({pd.NA: None})

        for _, row in clean_df.iterrows():
            translations.append(
                SheetTranslation(
                    original_name=row[SHEETS_PROPERTIES_HEADERS["original_name"]],
                    translated_name=row[SHEETS_PROPERTIES_HEADERS["translated_name"]],
                    orientation=row[SHEETS_PROPERTIES_HEADERS["orientation"]].lower(),
                    header_row=row[SHEETS_PROPERTIES_HEADERS["header_row"]],
                    header_col=row[SHEETS_PROPERTIES_HEADERS["header_col"]],
                    values_col=row[SHEETS_PROPERTIES_HEADERS["values_col"]],
                    start_row=row[SHEETS_PROPERTIES_HEADERS["start_row"]],
                    start_col=row[SHEETS_PROPERTIES_HEADERS["start_col"]],
                    end_row=row[SHEETS_PROPERTIES_HEADERS["end_row"]],
                    end_col=row[SHEETS_PROPERTIES_HEADERS["end_col"]],
                )
            )

        return TranslationsLibrary(translations)


class DocumentTranslator:
    _translators: dict[str, CategoryTranslator]
    _library: TranslationsLibrary

    general_info_sheet_translator: GeneralInfoSheetTranslator
    bill_of_materials_sheet_translator: BillOfMaterialsSheetTranslator

    def __init__(
        self, library: TranslationsLibrary | None = None, translators: dict[str, CategoryTranslator] | None = None
    ):
        self._translators = translators or {}
        self._library = library or TranslationsLibrary([])

    @staticmethod
    def from_dataframes(
        dfs: dict[str, pd.DataFrame],
        attribute_name_col: int,
        translated_name_col: int,
        translation_library_df: pd.DataFrame | None = None,
    ) -> "DocumentTranslator":
        translators = {
            category_name: CategoryTranslator.from_dataframe(df, attribute_name_col, translated_name_col)
            for category_name, df in dfs.items()
        }

        return DocumentTranslator(
            TranslationsLibrary.from_dataframe(translation_library_df)
            if translation_library_df is not None
            else TranslationsLibrary([]),
            translators,
        )

    @staticmethod
    def from_xlsx(
        xlsx_path: str | Path, attribute_name_col: int, translated_name_col: int, header_row: int = 0
    ) -> "DocumentTranslator":
        xlsx = pd.ExcelFile(xlsx_path)

        true_sheets = [sheet for sheet in xlsx.sheet_names if sheet != "Translations Library"]

        library = (
            xlsx.parse("Translations Library", header=header_row)
            if "Translations Library" in xlsx.sheet_names
            else None
        )
        dfs = {sheet_name: xlsx.parse(sheet_name, header=header_row) for sheet_name in true_sheets}

        return DocumentTranslator.from_dataframes(
            dfs, attribute_name_col, translated_name_col, translation_library_df=library
        )

    def translate(self, category_name: str, attribute_name: str) -> str:
        translator = self._translators.get(category_name)
        if translator is None:
            return attribute_name
        return translator.translate(attribute_name)

    def get_translated_xlsx_sheet(self, xlsx: pd.ExcelFile, translated_sheet_name: str) -> pd.DataFrame | None:
        translation = self._library.get_translation_by_translated_name(translated_sheet_name)
        if translation is None:
            return None

        if translation.original_name not in xlsx.sheet_names:
            return None

        df = xlsx.parse(translation.original_name)

        return translation.translate_df(df)


COMMON_CATEGORY_NAMES = {
    "project": "General Information",
    "bom": "Bill of Materials",
}

SHEETS_PROPERTIES_HEADERS = {
    "original_name": "Sheet name in your format",
    "translated_name": "Translated name to OpenBDF",
    "orientation": "Orientation (horizontal/vertical)",
    "header_row": "Header row",
    "header_col": "Header column (for vertical sheets)",
    "values_col": "Values column (for vertical sheets)",
    "start_row": "Start row (for horizontal sheets)",
    "start_col": "Start column (for horizontal sheets)",
    "end_row": "End row (for horizontal sheets, optional)",
    "end_col": "End column (for horizontal sheets, optional)",
}
