import operator
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

import pandas as pd
from pydantic import BaseModel


@dataclass(frozen=True)
class TranslationRule:
    predicate: Callable[[str], bool]
    output: str

    @staticmethod
    def fromString(code: str, output: str) -> "TranslationRule":
        if code.startswith("@REGEX"):
            pattern_text = code.removeprefix("@REGEX")
            if not pattern_text:
                raise ValueError(f"Empty regex rule: {code!r}")

            pattern = re.compile(pattern_text)

            def predicate(value: str) -> bool:
                return bool(pattern.fullmatch(value))

            return TranslationRule(predicate=predicate, output=output)

        match = re.fullmatch(
            r"@(?P<kind>INT|FLOAT)(?P<op>>=|<=|==|!=|>|<)(?P<value>.+)",
            code,
        )
        if not match:
            raise ValueError(f"Unsupported rule syntax: {code!r}")

        kind = match.group("kind")
        op_symbol = match.group("op")
        raw_threshold = match.group("value").strip()

        ops = {
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne,
        }
        op = ops[op_symbol]

        if kind == "INT":
            int_threshold = int(raw_threshold)

            def predicate(value: str) -> bool:
                if not re.fullmatch(r"[+-]?\d+", value):
                    return False
                return op(int(value), int_threshold)

            return TranslationRule(predicate=predicate, output=output)

        if kind == "FLOAT":
            float_threshold = float(raw_threshold)

            def predicate(value: str) -> bool:
                try:
                    parsed = float(value)
                except ValueError:
                    return False
                return op(parsed, float_threshold)

            return TranslationRule(predicate=predicate, output=output)

        raise ValueError(f"Unsupported rule kind: {kind!r}")


class CategoryTranslator:
    _translation_dict: dict[str, str]
    _rules: list[TranslationRule]

    def __init__(
        self,
        translation_dict: dict[str, str],
        rules: list[TranslationRule] | None = None,
    ):
        self._translation_dict = translation_dict
        self._rules = rules or []

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame,
        attribute_name_col: int,
        translated_name_col: int,
    ) -> "CategoryTranslator":
        translation_dict: dict[str, str] = {}
        rules: list[TranslationRule] = []

        for raw_key, output in zip(df.iloc[:, attribute_name_col], df.iloc[:, translated_name_col]):
            raw_key = str(raw_key)
            output = str(output)

            if raw_key.startswith("@"):
                rules.append(TranslationRule.fromString(raw_key, output))
            else:
                translation_dict[raw_key] = output

        return CategoryTranslator(translation_dict, rules)

    def translate(self, attribute_name: str) -> str:
        if attribute_name is None:
            return attribute_name

        if isinstance(attribute_name, str) and attribute_name in self._translation_dict:
            return self._translation_dict[attribute_name]

        for rule in self._rules:
            if rule.predicate(attribute_name):
                return rule.output

        return attribute_name


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

    def model_post_init(self, __context: dict) -> None:
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
            header_start_row = self.header_row or 0
            header_start_col = self.start_col or 0
            header_end_col = self.end_col

            header = df.iloc[header_start_row, header_start_col:header_end_col]

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
            if not isinstance(row[SHEETS_PROPERTIES_HEADERS["original_name"]], str) or not isinstance(
                row[SHEETS_PROPERTIES_HEADERS["translated_name"]], str
            ):
                continue

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

        df = xlsx.parse(translation.original_name, header=None)

        return translation.translate_df(df)

    @staticmethod
    def default_openbdf_translator() -> "DocumentTranslator":
        return DocumentTranslator(
            library=TranslationsLibrary([
                SheetTranslation(
                    original_name=COMMON_CATEGORY_NAMES["project"],
                    translated_name=COMMON_CATEGORY_NAMES["project"],
                    orientation="vertical",
                    header_row=0,
                    header_col=3,
                    values_col=9,
                ),
                SheetTranslation(
                    original_name=COMMON_CATEGORY_NAMES["bom"],
                    translated_name=COMMON_CATEGORY_NAMES["bom"],
                    orientation="horizontal",
                    header_row=7,
                    start_row=8,
                    start_col=1,
                ),
                SheetTranslation(
                    original_name=COMMON_CATEGORY_NAMES["results_wide"],
                    translated_name=COMMON_CATEGORY_NAMES["results_wide"],
                    orientation="horizontal",
                    header_row=6,
                    start_row=7,
                    start_col=1,
                ),
            ])
        )


COMMON_CATEGORY_NAMES = {
    "project": "General Information",
    "bom": "Bill of Materials",
    "results_wide": "LCA Result (Wide)",
    "results_tall": "LCA Result (Tall)",
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
