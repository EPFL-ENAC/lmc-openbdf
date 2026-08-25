from math import nan

import pandas as pd
import pytest

from openbdf.lib.converters.translators import DocumentTranslator, PreprocessRule


@pytest.mark.parametrize("value", [2, -2, 0, "2", "+2", 2.0])
def test_int_preprocess_rule_accepts_integer_values(value):
    result = PreprocessRule.fromString("@INT").execute(value)

    assert result.valid is True
    assert result.value is value


@pytest.mark.parametrize("value", ["EG", "2.5", 2.5, True, None, nan])
def test_int_preprocess_rule_rejects_non_integer_values(value):
    result = PreprocessRule.fromString("@INT").execute(value)

    assert result.valid is False
    assert result.value is value


@pytest.mark.parametrize("code", ["", "   ", "@FLOAT", "@INT>0", "INT"])
def test_preprocess_rule_rejects_unsupported_syntax(code):
    with pytest.raises(ValueError, match="Unsupported preprocess rule syntax"):
        PreprocessRule.fromString(code)


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
