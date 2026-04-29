import pandas as pd


# TODO : best idea would to make this a global translator, you give the cli a translator file, with a sheet for the attributes names, and one sheet per enum
class AttributeTranslator:
    _translation_dict: dict[str, str] = {}

    def __init__(self, translation_dict: dict[str, str]):
        self._translation_dict = translation_dict

    @staticmethod
    def from_dataframe(df: pd.DataFrame, attribute_name_col: str, translated_name_col: str) -> "AttributeTranslator":
        translation_dict = dict(zip(df[attribute_name_col], df[translated_name_col]))
        return AttributeTranslator(translation_dict)

    def translate(self, attribute_name: str) -> str:
        return self._translation_dict.get(attribute_name, attribute_name)
