from math import nan

import pandas as pd
import pytest

from openbdf.lib.converters.dataframe import bom_draft_from_dataframe
from openbdf.lib.converters.translators import DocumentTranslator, PreprocessRule
from openbdf.model.enums.buildings import AboveBelowGround


@pytest.mark.parametrize(
    "value, expected",
    [
        (2, 2),
        (-2, -2),
        (0, 0),
        ("2", 2),
        ("+2", 2),
        (2.0, 2.0),
        ("6. Geschoss", 6),
        ("Obergeschoß 10", 10),
        ("OG 2 - 2e verdieping", 2),
    ],
)
def test_int_preprocess_rule_accepts_integer_values(value, expected):
    result = PreprocessRule.fromString("@INT").execute(value)

    assert result.valid is True
    assert result.value == expected


@pytest.mark.parametrize("value", ["EG", 2.5, True, None, nan])
def test_int_preprocess_rule_rejects_non_integer_values(value):
    result = PreprocessRule.fromString("@INT").execute(value)

    assert result.valid is False
    assert result.value is value


@pytest.mark.parametrize("code", ["", "   ", "@FLOAT", "@INT>0", "INT"])
def test_preprocess_rule_rejects_unsupported_syntax(code):
    with pytest.raises(ValueError, match="Unsupported preprocess rule syntax"):
        PreprocessRule.fromString(code)


@pytest.mark.parametrize(
    "value, expected_floor_level, expected_above_below_ground",
    [
        ("-1", "-1", AboveBelowGround.BELOW),
        ("0", "0", AboveBelowGround.ABOVE),
        ("1", "1", AboveBelowGround.ABOVE),
        ("2", "2", AboveBelowGround.ABOVE),
        ("3", "3", AboveBelowGround.ABOVE),
        ("4", "4", AboveBelowGround.ABOVE),
        ("5", "5", AboveBelowGround.ABOVE),
        ("6. Geschoss", "6", AboveBelowGround.ABOVE),
        ("DG", None, AboveBelowGround.ABOVE),
        ("DG - Dak", None, AboveBelowGround.ABOVE),
        ("EG", None, AboveBelowGround.ABOVE),
        ("EG - Begane grond", None, AboveBelowGround.ABOVE),
        ("Erdgeschoß", None, AboveBelowGround.ABOVE),
        ("Favoriten", None, AboveBelowGround.BELOW),
        ("Obergeschoß 1", "1", AboveBelowGround.ABOVE),
        ("Obergeschoß 10", "10", AboveBelowGround.ABOVE),
        ("Obergeschoß 2", "2", AboveBelowGround.ABOVE),
        ("Obergeschoß 3", "3", AboveBelowGround.ABOVE),
        ("Obergeschoß 4", "4", AboveBelowGround.ABOVE),
        ("Obergeschoß 5", "5", AboveBelowGround.ABOVE),
        ("Obergeschoß 6", "6", AboveBelowGround.ABOVE),
        ("Obergeschoß 7", "7", AboveBelowGround.ABOVE),
        ("Obergeschoß 8", "8", AboveBelowGround.ABOVE),
        ("Obergeschoß 9", "9", AboveBelowGround.ABOVE),
        ("OG", None, AboveBelowGround.ABOVE),
        ("OG 1 - 1e verdieping", "1", AboveBelowGround.ABOVE),
        ("OG 2 - 2e verdieping", "2", AboveBelowGround.ABOVE),
        ("OG 3 - 3e verdieping", "3", AboveBelowGround.ABOVE),
        ("RDOK Dach", None, AboveBelowGround.ABOVE),
        ("UG", None, AboveBelowGround.BELOW),
        ("UG - Kelder", None, AboveBelowGround.BELOW),
        ("Untergeschoß", None, AboveBelowGround.BELOW),
    ],
)
def test_parse_floor(value: str, expected_floor_level: str | None, expected_above_below_ground: AboveBelowGround):
    above_below_ground_rules = [
        ("@INT>=0", AboveBelowGround.ABOVE),
        ("@REGEX^DG.*", AboveBelowGround.ABOVE),
        ("@REGEX^EG.*", AboveBelowGround.ABOVE),
        ("Erdgeschoß", AboveBelowGround.ABOVE),
        ("@REGEX^Obergeschoß \\d+", AboveBelowGround.ABOVE),
        ("@REGEX^OG.*", AboveBelowGround.ABOVE),
        ("@REGEX^\\d+\\. Geschoss", AboveBelowGround.ABOVE),
        ("RDOK Dach", AboveBelowGround.ABOVE),
        ("@INT<0", AboveBelowGround.BELOW),
        ("Favoriten", AboveBelowGround.BELOW),
        ("@REGEX^UG.*", AboveBelowGround.BELOW),
        ("@REGEX^Untergeschoß", AboveBelowGround.BELOW),
    ]

    bom_sheet = pd.DataFrame({
        "source": ["floor", "floor"],
        "target": ["custom_floor_level", "common_above_below_ground"],
        "preprocess": ["@INT", ""],
    })
    enum_sheet = pd.DataFrame({
        "source": [rule[0] for rule in above_below_ground_rules],
        "target": [str(rule[1]) for rule in above_below_ground_rules],
    })

    translator = DocumentTranslator.from_dataframes(
        {"Bill of Materials": bom_sheet, "AboveBelowGround": enum_sheet},
        attribute_name_col=0,
        translated_name_col=1,
        preprocess_rule_col=2,
    )

    records = bom_draft_from_dataframe(
        pd.DataFrame({"floor": [value]}),
        document_translator=translator,
    )

    record = records[0]
    assert record.custom_floor_level == expected_floor_level
    assert record.common_above_below_ground == expected_above_below_ground


def test_blank_preprocess_cells_mean_no_rule():
    dataframe = pd.DataFrame({
        "source": ["first", "second"],
        "target": ["first_target", "second_target"],
        "preprocess": ["", None],
    })

    translator = DocumentTranslator.from_dataframes(
        {"Category": dataframe},
        attribute_name_col=0,
        translated_name_col=1,
        preprocess_rule_col=2,
    )

    assert translator.get_preprocess_rule("Category", "first_target") is None
    assert translator.get_preprocess_rule("Category", "second_target") is None


def test_loading_and_applying_int_preprocess_rule_is_silent(capsys):
    dataframe = pd.DataFrame({
        "source": ["floor"],
        "target": ["floor_level"],
        "preprocess": ["@INT"],
    })

    translator = DocumentTranslator.from_dataframes(
        {"Category": dataframe},
        attribute_name_col=0,
        translated_name_col=1,
        preprocess_rule_col=2,
    )
    rule = translator.get_preprocess_rule("Category", "floor_level")

    assert rule is not None
    assert rule.execute("2").valid is True
    assert capsys.readouterr().out == ""


def test_document_translator_reads_int_rule_from_xlsx(tmp_path, capsys):
    workbook_path = tmp_path / "translator.xlsx"
    dataframe = pd.DataFrame({
        "source": ["floor", "name"],
        "target": ["floor_level", "material_name_custom"],
        "attribute": ["Floor level", "Material name"],
        "datatype": ["integer", "string"],
        "requirements": ["Recommended", "Recommended"],
        "default": [None, None],
        "preprocess": ["@INT", ""],
    })
    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        dataframe.to_excel(writer, sheet_name="Category", index=False)

    translator = DocumentTranslator.from_xlsx(
        workbook_path,
        attribute_name_col=0,
        translated_name_col=1,
        default_value_col=5,
        preprocess_rule_col=6,
    )

    int_rule = translator.get_preprocess_rule("Category", "floor_level")
    assert int_rule is not None
    assert int_rule.execute(-2).valid is True
    assert translator.get_preprocess_rule("Category", "material_name_custom") is None
    assert capsys.readouterr().out == ""
