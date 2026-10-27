import operator
import re
from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from pathlib import Path
from typing import Any, Callable, Literal, TypedDict

import pandas as pd
from pydantic import BaseModel

from openbdf.lib.converters.translator_csv import csv_dir_sheets

ABOUT_SHEET_NAME = "About"


@dataclass(frozen=True)
class PreprocessResult:
    value: Any
    valid: bool


@dataclass(frozen=True)
class PreprocessRule:
    predicate: Callable[[Any], PreprocessResult]

    @staticmethod
    def fromString(code: str) -> "PreprocessRule":
        if code.strip() != "@INT":
            raise ValueError(f"Unsupported preprocess rule syntax: {code!r}")

        def int_filter_predicate(value: Any) -> PreprocessResult:
            valid = False
            if isinstance(value, bool):
                valid = False
            elif isinstance(value, Integral):
                valid = True
            elif isinstance(value, Real):
                numeric_value = float(value)
                valid = isfinite(numeric_value) and numeric_value.is_integer()
            elif isinstance(value, str):
                # Warning: if there is a floating point number, the decimal part will be ignored
                match = re.search(r"[+-]?\d+", value.strip())
                if match:
                    value = int(match.group(0))
                    valid = True

            return PreprocessResult(value=value, valid=valid)

        return PreprocessRule(predicate=int_filter_predicate)

    def execute(self, value: Any) -> PreprocessResult:
        return self.predicate(value)


@dataclass(frozen=True)
class TranslationRule:
    predicate: Callable[[str], bool]
    # A rule with no output keeps the value unchanged, so the field is derived from the label itself.
    output: str | None

    @staticmethod
    def fromString(code: str, output: str | None) -> "TranslationRule":
        if code.startswith("@REGEX"):
            pattern_text = code.removeprefix("@REGEX")
            if not pattern_text:
                raise ValueError(f"Empty regex rule: {code!r}")

            pattern = re.compile(pattern_text)

            def predicate(value: str) -> bool:
                return bool(pattern.fullmatch(value))

            return TranslationRule(predicate=predicate, output=output)

        bare_kind = re.fullmatch(r"@(?P<kind>INT|FLOAT)", code.strip())
        if bare_kind:
            kind = bare_kind.group("kind")

            def any_number(value: str) -> bool:
                if kind == "INT":
                    return bool(re.fullmatch(r"[+-]?\d+", value))
                try:
                    float(value)
                except ValueError:
                    return False
                return True

            return TranslationRule(predicate=any_number, output=output)

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


def _is_missing(value: Any) -> bool:
    """Return True for missing/blank default-value cells."""
    if value is None:
        return True
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


class CategoryTranslator:
    _translation_dict: dict[str, list[str]]
    _preprocess_rules: dict[str, PreprocessRule]
    _rules: list[TranslationRule]
    _default_values: dict[str, str]

    def __init__(
        self,
        translation_dict: dict[str, list[str]],
        preprocess_rules: dict[str, PreprocessRule] | None = None,
        rules: list[TranslationRule] | None = None,
        default_values: dict[str, str] | None = None,
    ):
        self._translation_dict = translation_dict
        self._preprocess_rules = preprocess_rules or {}
        self._rules = rules or []
        self._default_values = default_values or {}

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame,
        attribute_name_col: int,
        translated_name_col: int,
        default_value_col: int | None = None,
        preprocess_rule_col: int | None = None,
    ) -> "CategoryTranslator":
        translation_dict: dict[str, list[str]] = {}
        preprocess_rules: dict[str, PreprocessRule] = {}
        rules: list[TranslationRule] = []
        default_values: dict[str, str] = {}

        has_default_col = default_value_col is not None and df.shape[1] > default_value_col
        has_preprocess_rule_col = preprocess_rule_col is not None and df.shape[1] > preprocess_rule_col

        for idx, (raw_key, output) in enumerate(zip(df.iloc[:, attribute_name_col], df.iloc[:, translated_name_col])):
            # A blank source cell declares no local code. Reading it as str would key every
            # blank row under "nan", so an unnamed sheet column would match all of them.
            has_source = not _is_missing(raw_key)
            raw_key = str(raw_key)
            output = None if _is_missing(output) else str(output)

            if has_source and raw_key.startswith("@"):
                rules.append(TranslationRule.fromString(raw_key, output))
            elif has_source and output is not None:
                translation_dict.setdefault(raw_key, []).append(output)

            if output is None:
                continue

            if has_default_col:
                default_value = df.iloc[idx, default_value_col]
                if not _is_missing(default_value):
                    default_values[output] = str(default_value)

            if has_preprocess_rule_col:
                preprocess_rule = df.iloc[idx, preprocess_rule_col]
                if isinstance(preprocess_rule, str) and preprocess_rule.strip():
                    # Rules are keyed by translated names, rather than source names.
                    preprocess_rules[output] = PreprocessRule.fromString(preprocess_rule)

        return CategoryTranslator(translation_dict, preprocess_rules, rules, default_values)

    def translate(self, attribute_name: str) -> list[str]:
        if attribute_name is None:
            return [attribute_name]

        if isinstance(attribute_name, str) and attribute_name in self._translation_dict:
            return self._translation_dict[attribute_name]  # Return all translated names

        for rule in self._rules:
            if isinstance(attribute_name, str) and rule.predicate(attribute_name):
                return [attribute_name] if rule.output is None else [rule.output]

        return [attribute_name]

    def get_default(self, attribute_name: str) -> str | None:
        """Return the default value for a translated attribute name, if any."""
        return self._default_values.get(attribute_name)

    def source_keys(self) -> list[str]:
        """Return the literal source values this translator knows, in file order."""
        return list(self._translation_dict)

    def get_preprocess_rule(self, field_name: str) -> PreprocessRule | None:
        """Return the preprocess rule for a translated field name, if any."""
        return self._preprocess_rules.get(field_name)


SheetOrientation = Literal["horizontal", "vertical"]


class SheetTranslation(BaseModel):
    original_name: str
    translated_name: str
    orientation: SheetOrientation
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

    def translate_df(self, df: pd.DataFrame, df_orientation: SheetOrientation | None = None) -> pd.DataFrame:
        if self.orientation == "vertical":
            translated_df = df.iloc[self.header_row :, [self.header_col, self.values_col]]
        elif self.orientation == "horizontal":
            header_start_row = self.header_row or 0
            header_start_col = self.start_col or 0
            header_end_col = self.end_col

            header = df.iloc[header_start_row, header_start_col:header_end_col]
            values = df.iloc[(self.start_row or 1) : self.end_row, (self.start_col or 0) : self.end_col]

            # The index stays the sheet row, so a finding can name the row the user sees.
            translated_df = pd.DataFrame(values.values, columns=header.values, index=values.index)
        else:
            raise ValueError("Orientation must be either 'horizontal' or 'vertical'.")

        if df_orientation is not None and df_orientation != self.orientation:
            translated_df = translated_df.transpose().reset_index(drop=False)

        return translated_df


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

        clean_df = df.astype(object).where(pd.notna(df), None)

        for row in clean_df.to_dict("records"):
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
        default_value_col: int | None = None,
        preprocess_rule_col: int | None = None,
        translation_library_df: pd.DataFrame | None = None,
    ) -> "DocumentTranslator":
        translators = {
            category_name: CategoryTranslator.from_dataframe(
                df,
                attribute_name_col,
                translated_name_col,
                default_value_col=default_value_col,
                preprocess_rule_col=preprocess_rule_col,
            )
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
        xlsx_path: str | Path,
        attribute_name_col: int,
        translated_name_col: int,
        default_value_col: int | None = None,
        preprocess_rule_col: int | None = None,
        header_row: int = 0,
    ) -> "DocumentTranslator":
        with pd.ExcelFile(xlsx_path) as xlsx:
            true_sheets = [
                sheet for sheet in xlsx.sheet_names if sheet not in ("Translations Library", ABOUT_SHEET_NAME)
            ]

            library = (
                xlsx.parse("Translations Library", header=header_row)
                if "Translations Library" in xlsx.sheet_names
                else None
            )
            dfs = {sheet_name: xlsx.parse(sheet_name, header=header_row) for sheet_name in true_sheets}

        return DocumentTranslator.from_dataframes(
            dfs,
            attribute_name_col,
            translated_name_col,
            default_value_col=default_value_col,
            preprocess_rule_col=preprocess_rule_col,
            translation_library_df=library,
        )

    @staticmethod
    def from_csv_dir(
        directory: str | Path,
        attribute_name_col: int,
        translated_name_col: int,
        default_value_col: int | None = None,
        preprocess_rule_col: int | None = None,
        header_row: int = 0,
    ) -> "DocumentTranslator":
        """Load a translator from a directory that holds one CSV file per sheet."""
        sheets = csv_dir_sheets(Path(directory))
        true_sheets = [
            (sheet_name, path)
            for sheet_name, path in sheets
            if sheet_name not in ("Translations Library", ABOUT_SHEET_NAME)
        ]
        library_path = next((path for sheet_name, path in sheets if sheet_name == "Translations Library"), None)

        dfs = {sheet_name: pd.read_csv(path, dtype=str, header=header_row) for sheet_name, path in true_sheets}
        library = pd.read_csv(library_path, dtype=str, header=header_row) if library_path is not None else None

        return DocumentTranslator.from_dataframes(
            dfs,
            attribute_name_col,
            translated_name_col,
            default_value_col=default_value_col,
            preprocess_rule_col=preprocess_rule_col,
            translation_library_df=library,
        )

    def __add__(self, other: "DocumentTranslator") -> "DocumentTranslator":
        """Merge this translator with another into a single translator.

        Category translators are merged by category name with a last-wins
        policy (a category present in ``other`` replaces the one from this
        translator). Sheet translations are concatenated."""
        translators = {**self._translators, **other._translators}
        library = TranslationsLibrary(self._library._sheets_translations + other._library._sheets_translations)
        return DocumentTranslator(library=library, translators=translators)

    def translate(self, category_name: str, attribute_name: str) -> list[str]:
        translator = self._translators.get(category_name, self._translators.get(category_name[:31], None))
        if translator is None:
            return [attribute_name]
        return translator.translate(attribute_name)

    def get_default(self, category_name: str, attribute_name: str) -> str | None:
        translator = self._translators.get(category_name, self._translators.get(category_name[:31], None))
        if translator is None:
            return None
        return translator.get_default(attribute_name)

    def source_keys(self, category_name: str) -> list[str]:
        """Return the source values of a category, so a caller can look for them as column names."""
        translator = self._translators.get(category_name, self._translators.get(category_name[:31], None))
        if translator is None:
            return []
        return translator.source_keys()

    def get_preprocess_rule(self, category_name: str, attribute_name: str) -> PreprocessRule | None:
        translator = self._translators.get(category_name, self._translators.get(category_name[:31], None))
        if translator is None:
            return None
        return translator.get_preprocess_rule(attribute_name)

    def get_sheet_translation(self, translated_sheet_name: str) -> SheetTranslation | None:
        return self._library.get_translation_by_translated_name(translated_sheet_name)

    @staticmethod
    def default_openbdf_translator() -> "DocumentTranslator":
        return DocumentTranslator(
            library=TranslationsLibrary([
                SheetTranslation(
                    original_name=COMMON_CATEGORY_PROPERTIES["project"]["name"],
                    translated_name=COMMON_CATEGORY_PROPERTIES["project"]["name"],
                    orientation=COMMON_CATEGORY_PROPERTIES["project"]["orientation"],
                    header_row=0,
                    header_col=3,
                    values_col=9,
                ),
                # Generated template layout (wide_to_xlsx): field codes in
                # xlsx row 2, metadata rows 3-8, data from xlsx row 9.
                SheetTranslation(
                    original_name=COMMON_CATEGORY_PROPERTIES["bom"]["name"],
                    translated_name=COMMON_CATEGORY_PROPERTIES["bom"]["name"],
                    orientation=COMMON_CATEGORY_PROPERTIES["bom"]["orientation"],
                    header_row=1,
                    start_row=8,
                    start_col=1,
                ),
                # Project Material Database: field codes in xlsx row 2, metadata rows
                # 3-8, data from xlsx row 9.
                SheetTranslation(
                    original_name=COMMON_CATEGORY_PROPERTIES["material_database"]["name"],
                    translated_name=COMMON_CATEGORY_PROPERTIES["material_database"]["name"],
                    orientation=COMMON_CATEGORY_PROPERTIES["material_database"]["orientation"],
                    header_row=1,
                    start_row=8,
                    start_col=1,
                ),
                SheetTranslation(
                    original_name=COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
                    translated_name=COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
                    orientation=COMMON_CATEGORY_PROPERTIES["results_wide"]["orientation"],
                    header_row=1,
                    start_row=8,
                    start_col=1,
                ),
            ])
        )


class CategoryProperties(TypedDict):
    name: str
    orientation: SheetOrientation


COMMON_CATEGORY_PROPERTIES: dict[str, CategoryProperties] = {
    "project": {"name": "General Information", "orientation": "vertical"},
    "bom": {"name": "Bill of Materials", "orientation": "horizontal"},
    "material_database": {"name": "Project Material Database", "orientation": "horizontal"},
    "results_wide": {"name": "LCA Result (Wide)", "orientation": "horizontal"},
    "results_tall": {"name": "LCA Result (Tall)", "orientation": "horizontal"},
}

# Category that maps a national storey label to an OpenBDF floor number. It carries no
# enum, so the blank translator template generates it separately.
FLOOR_LEVEL_CATEGORY = "FloorLevel"

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
