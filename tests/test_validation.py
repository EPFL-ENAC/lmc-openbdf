from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from types import SimpleNamespace
from typing import Any

import pandas as pd

from openbdf.lib.converters.dataframe import bom_from_dataframe, project_from_dataframe
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.validation import (
    check_duplicate_material_ids,
    check_missing_mass,
    check_result_row_alignment,
)
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.general_info import ProjectRecordBase


def value_for_annotation(annotation: Any) -> Any:
    annotation, _ = unwrap_optional(annotation)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation)).value
    if annotation is bool:
        return True
    if annotation is int:
        return "1"
    if annotation is Decimal:
        return "1"
    if annotation is date:
        return "2024-01-01"
    if annotation is str:
        return "value"

    return "value"


def required_rows(model_cls: type[Any]) -> list[dict[str, Any]]:
    return [
        {"field_code": get_field_code(field_name, field_info), "value": value_for_annotation(field_info.annotation)}
        for field_name, field_info in model_cls.model_fields.items()
        if field_info.is_required()
    ]


def project_frame(**overrides: Any) -> pd.DataFrame:
    """Build the General Information frame of a valid project, with some values replaced."""
    rows = [row for row in required_rows(ProjectRecordBase) if row["field_code"] not in overrides]
    rows.extend({"field_code": field_code, "value": value} for field_code, value in overrides.items())
    return pd.DataFrame(rows)


def bom_frame(**overrides: Any) -> pd.DataFrame:
    """Build one Bill of Materials row that passes every check, with some values replaced."""
    row = {item["field_code"]: item["value"] for item in required_rows(BuildingBillMaterialsSlimRecordBase)}
    return pd.DataFrame([row | overrides])


def test_a_missing_required_value_is_a_missing_required_field_finding():
    dataframe = bom_frame()
    dataframe.loc[0, "material_id"] = None

    findings: list[Any] = []
    bom_from_dataframe(dataframe, findings=findings)

    assert [str(finding) for finding in findings] == ["E01: Field material_id is required and was not provided"]
    assert findings[0].row == 1


def test_a_dropped_line_is_reported_with_its_excel_row():
    dataframe = pd.concat([bom_frame(), bom_frame()], ignore_index=True)
    dataframe.loc[0, "material_id"] = None
    findings: list[Any] = []

    bom_from_dataframe(dataframe, findings=findings, drop_invalid=True)

    assert [str(finding) for finding in findings] == [
        "E33: Row 1: line dropped: Field material_id is required and was not provided"
    ]
    assert findings[0].row == 1


def test_a_value_outside_its_enum_is_an_unknown_enum_value_finding():
    findings: list[Any] = []

    bom_from_dataframe(bom_frame(material_data_type="bogus"), findings=findings)

    assert [str(finding) for finding in findings] == ["E02: Value 'bogus' is not a valid MaterialDataType"]


def test_a_value_of_the_wrong_type_is_a_type_mismatch_finding():
    findings: list[Any] = []

    bom_from_dataframe(bom_frame(material_reference_service_life="not a number"), findings=findings)

    assert [str(finding) for finding in findings] == ["E03: Field material_reference_service_life expects Decimal"]


def test_a_share_above_one_is_a_share_out_of_range_finding():
    dataframe = project_frame(lca_data_generic_share="2")
    findings: list[Any] = []

    project_from_dataframe(dataframe, findings=findings)

    assert [str(finding) for finding in findings] == ["E13: Field lca_data_generic_share must lie between 0 and 1"]
    # The overridden value is the last row of the sheet, so the finding names that row.
    assert findings[0].row == len(dataframe)


def test_a_floor_area_of_zero_is_a_floor_area_not_positive_finding():
    findings: list[Any] = []

    project_from_dataframe(project_frame(building_gross_floor_area="0"), findings=findings)

    assert [str(finding) for finding in findings] == ["E17: Floor area must be greater than zero"]


def test_a_field_code_declared_twice_is_a_duplicate_field_code_finding():
    dataframe = project_frame()
    duplicate = dataframe[dataframe["field_code"] == "record_type"]
    dataframe = pd.concat([dataframe, duplicate], ignore_index=True)

    findings: list[Any] = []
    project_from_dataframe(dataframe, findings=findings)

    assert [str(finding) for finding in findings] == ["E20: Field code record_type is declared twice"]
    assert findings[0].row == len(dataframe)


def test_a_different_number_of_inventory_and_result_rows_is_a_row_count_mismatch_finding():
    bill_of_materials = pd.DataFrame({"material_id": ["MAT-1"]})
    results_wide = pd.DataFrame({"material_id": ["MAT-1", "MAT-2"]})

    findings = check_result_row_alignment(bill_of_materials, results_wide)

    assert [str(finding) for finding in findings] == ["E05: Bill of Materials has 1 rows, LCA Result (Wide) has 2"]


def test_two_rows_with_different_material_ids_are_a_misalignment_finding():
    bill_of_materials = pd.DataFrame({"material_id": ["MAT-1", "MAT-2"]}, index=[9, 10])
    results_wide = pd.DataFrame({"material_id": ["MAT-1", "MAT-3"]}, index=[9, 10])

    findings = check_result_row_alignment(bill_of_materials, results_wide)

    assert [str(finding) for finding in findings] == [
        "E06: Row 11: material_id MAT-2 in the inventory, MAT-3 in the results"
    ]
    assert findings[0].row == 11


def test_a_row_without_a_mass_warns_and_a_blank_row_is_ignored():
    bill_of_materials = pd.DataFrame(
        {"material_id": ["MAT-1", None], "material_weight_kg": [None, None]},
        index=[9, 10],
    )

    findings = check_missing_mass(bill_of_materials)

    assert [str(finding) for finding in findings] == [
        "E16: Row 10 has no mass, material efficiency analysis is not possible"
    ]


def test_a_dropped_row_is_not_reported_as_missing_a_mass():
    bill_of_materials = pd.DataFrame(
        {"material_id": ["MAT-1", "MAT-2"], "material_weight_kg": [None, None]},
        index=[9, 10],
    )

    findings = check_missing_mass(bill_of_materials, frozenset({11}))

    assert [str(finding) for finding in findings] == [
        "E16: Row 10 has no mass, material efficiency analysis is not possible"
    ]


def test_two_rows_with_one_material_id_are_a_duplicate_material_id_finding():
    project = SimpleNamespace(
        bill_of_materials=[
            SimpleNamespace(material_id="MAT-1"),
            SimpleNamespace(material_id="MAT-1"),
        ]
    )

    findings = check_duplicate_material_ids(project)

    assert [str(finding) for finding in findings] == ["E32: material_id 'MAT-1' is used by 2 bill of materials rows"]
