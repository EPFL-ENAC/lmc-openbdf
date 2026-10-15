from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any

import pandas as pd
from pydantic import BaseModel

from openbdf.lib.converters.dataframe import bom_draft_from_dataframe, bom_from_dataframe, project_package_from_tables
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import get_field_code
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.general_info import ProjectRecordBase
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase


def value_for_annotation(annotation: Any) -> Any:
    annotation, _ = unwrap_optional(annotation)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation)).value
    if annotation is bool:
        return True
    if annotation is int:
        return 1
    if annotation is Decimal:
        return "1"
    if annotation is date:
        return "2024-01-01"
    if annotation is str:
        return "value"

    return "value"


def required_horizontal_row(model_cls: type[BaseModel], **overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {}

    for field_name, field_info in model_cls.model_fields.items():
        if field_info.is_required():
            row[get_field_code(field_name, field_info)] = value_for_annotation(field_info.annotation)

    row.update(overrides)
    return row


def project_df() -> pd.DataFrame:
    rows = [
        {
            "field_code": get_field_code(field_name, field_info),
            "value": value_for_annotation(field_info.annotation),
        }
        for field_name, field_info in ProjectRecordBase.model_fields.items()
        if field_info.is_required()
    ]
    return pd.DataFrame(rows)


def bom_df(*material_ids: str) -> pd.DataFrame:
    rows = [
        required_horizontal_row(
            BuildingBillMaterialsSlimRecordBase,
            material_id=material_id,
            custom_material_name=f"Material {material_id}",
        )
        for material_id in material_ids
    ]
    return pd.DataFrame(rows)


def wide_df(*material_ids: str) -> pd.DataFrame:
    rows = [
        required_horizontal_row(
            LCAResultsWideFullBase,
            material_id=material_id,
            gwp_total_a1_a3=str(index),
            gwp_total_total=str(index * 10),
        )
        for index, material_id in enumerate(material_ids, start=1)
    ]
    return pd.DataFrame(rows)


def tall_df(*material_ids: str) -> pd.DataFrame:
    rows = [
        required_horizontal_row(
            LCAResultsTallBase,
            material_id=material_id,
            lca_service_life=str(index * 10),
            lca_stages="A1" if index % 2 else "A2",
        )
        for index, material_id in enumerate(material_ids, start=1)
    ]
    return pd.DataFrame(rows)


def tables(
    bill_of_materials: pd.DataFrame,
    results_wide: pd.DataFrame | None = None,
    results_tall: pd.DataFrame | None = None,
    project_material_database: pd.DataFrame | None = None,
) -> OpenBDFTables:
    return OpenBDFTables(
        project=project_df(),
        bill_of_materials=bill_of_materials,
        project_material_database=(
            project_material_database if project_material_database is not None else project_material_database_df()
        ),
        results_wide=results_wide,
        results_tall=results_tall,
    )


def project_material_database_df(*material_ref_ids: str) -> pd.DataFrame:
    rows = [
        required_horizontal_row(
            ProjectMaterialDatabaseBase,
            material_ref_id=material_ref_id,
            custom_material_name=f"Material {material_ref_id}",
        )
        for material_ref_id in material_ref_ids
    ]
    return pd.DataFrame(rows)


def test_bom_from_dataframe_keeps_missing_material_reference_service_life():
    result = bom_from_dataframe(bom_df("mat-1"))

    assert len(result) == 1
    assert result[0].material_reference_service_life is None


def test_bom_from_dataframe_drop_invalid_keeps_rows_missing_material_reference_service_life():
    dataframe = bom_df("mat-1", "mat-2")

    result = bom_from_dataframe(dataframe, drop_invalid=True)

    assert [item.material_id for item in result] == ["mat-1", "mat-2"]


def test_bom_draft_from_dataframe_drop_invalid_keeps_rows_missing_material_reference_service_life():
    result = bom_draft_from_dataframe(bom_df("mat-1", "mat-2"), drop_invalid=True)

    assert [item.material_id for item in result] == ["mat-1", "mat-2"]


def test_bom_from_dataframe_drop_invalid_no_drop_when_all_valid():
    result = bom_from_dataframe(bom_df("mat-1", "mat-2"), drop_invalid=True)

    assert len(result) == 2


def test_bom_drop_invalid_blank_rows_not_counted():
    valid = bom_df("mat-1")
    blank = pd.DataFrame(index=[0])
    dataframe = pd.concat([valid, blank], ignore_index=True)

    result = bom_from_dataframe(dataframe, drop_invalid=True)

    assert [item.material_id for item in result] == ["mat-1"]


def test_project_package_from_tables_drop_invalid_drops_missing_required():
    valid = bom_df("mat-1")
    invalid = bom_df("mat-2").drop(columns=["custom_material_name"])
    dataframe = pd.concat([valid, invalid], ignore_index=True)

    project = project_package_from_tables(tables(dataframe), drop_invalid=True)

    assert [b.material_id for b in project.bill_of_materials] == ["mat-1"]


def test_bom_draft_from_dataframe_allows_missing_material_reference_service_life():
    records = bom_draft_from_dataframe(bom_df("mat-1"))

    assert len(records) == 1
    assert records[0].material_reference_service_life is None


def test_project_package_from_tables_links_wide_results_to_bom_by_material_id():
    project = project_package_from_tables(tables(bom_df("mat-1"), results_wide=wide_df("mat-1")))

    bom_record = project.bill_of_materials[0]
    assert bom_record.lca_results_full_record is not None
    assert bom_record.lca_results_full_record.material_id == "mat-1"
    assert bom_record.lca_results_full_record.building_bill_materials_slim_record is bom_record


def test_project_package_from_tables_links_multiple_tall_results_to_bom_by_material_id():
    project = project_package_from_tables(tables(bom_df("mat-1"), results_tall=tall_df("mat-1", "mat-1")))

    bom_record = project.bill_of_materials[0]
    assert [result.material_id for result in bom_record.lca_results_tall_full_records] == ["mat-1", "mat-1"]
    assert all(
        result.building_bill_materials_slim_record is bom_record for result in bom_record.lca_results_tall_full_records
    )


def test_project_package_from_tables_links_results_to_separate_bom_entries():
    project = project_package_from_tables(
        tables(
            bom_df("mat-1", "mat-2"),
            results_wide=wide_df("mat-2", "mat-1"),
            results_tall=tall_df("mat-2", "mat-1"),
        )
    )

    by_material_id = {record.material_id: record for record in project.bill_of_materials}
    assert by_material_id["mat-1"].lca_results_full_record is not None
    assert by_material_id["mat-1"].lca_results_full_record.material_id == "mat-1"
    assert by_material_id["mat-2"].lca_results_full_record is not None
    assert by_material_id["mat-2"].lca_results_full_record.material_id == "mat-2"
    assert [result.material_id for result in by_material_id["mat-1"].lca_results_tall_full_records] == ["mat-1"]
    assert [result.material_id for result in by_material_id["mat-2"].lca_results_tall_full_records] == ["mat-2"]


def test_project_package_from_tables_allows_missing_result_tables():
    project = project_package_from_tables(tables(bom_df("mat-1")))

    bom_record = project.bill_of_materials[0]
    assert bom_record.material_id == "mat-1"
    assert bom_record.lca_results_full_record is None
    assert bom_record.lca_results_tall_full_records == []


def test_project_package_from_tables_builds_project_material_database_records():
    project = project_package_from_tables(
        tables(bom_df("mat-1"), project_material_database=project_material_database_df("M0001", "M0002"))
    )

    assert [record.material_ref_id for record in project.project_material_database] == ["M0001", "M0002"]
    assert all(record.project_record is project for record in project.project_material_database)
