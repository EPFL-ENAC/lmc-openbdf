from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel

from openbdf.lib.converters.dataframe import (
    bom_from_dataframe,
    project_package_from_tables,
)
from openbdf.lib.converters.translators import DocumentTranslator
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.fields import get_field_code
from openbdf.lib.types.values import parse_value
from openbdf.lib.validation import OpenBDFValidationError, Severity, sort_findings, validate_project
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.enums.energy import BuildingEnergyClassificationSystem
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


def bom_row(material_id: str, **overrides: Any) -> dict[str, Any]:
    return required_horizontal_row(
        BuildingBillMaterialsSlimRecordBase,
        **{"material_id": material_id, "lca_dataset_material_name": "value", **overrides},
    )


def bom_df(*material_ids: str) -> pd.DataFrame:
    rows = [
        bom_row(
            material_id,
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
            gwp_total=str(index * 10),
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
            project_material_database
            if project_material_database is not None
            else project_material_database_df(*bom_material_names(bill_of_materials))
        ),
        results_wide=results_wide,
        results_tall=results_tall,
    )


def bom_material_names(bom: pd.DataFrame) -> list[str]:
    if "custom_material_name" not in bom.columns:
        return []
    return [name for name in dict.fromkeys(bom["custom_material_name"]) if not pd.isna(name)]


def project_material_database_row(material_ref_id: str, custom_material_name: str, **overrides: Any) -> dict[str, Any]:
    return required_horizontal_row(
        ProjectMaterialDatabaseBase,
        **{
            "material_ref_id": material_ref_id,
            "custom_material_name": custom_material_name,
            "lca_dataset_material_name": "value",
            **overrides,
        },
    )


def project_material_database_df(*names: str) -> pd.DataFrame:
    rows = [project_material_database_row(f"M{index:04d}", name) for index, name in enumerate(names, start=1)]
    return pd.DataFrame(rows)


def tables_without_project_material_database(bill_of_materials: pd.DataFrame) -> OpenBDFTables:
    loaded = tables(bill_of_materials)
    loaded.project_material_database = None
    return loaded


def collected_findings(loaded: OpenBDFTables, *, draft: bool = False) -> list[OpenBDFValidationError]:
    """Run the ingest and the validation that the open command runs on the tables."""
    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(loaded, findings=findings, draft=draft)
    findings.extend(validate_project(project, loaded))
    return sort_findings(findings)


def test_project_package_from_tables_warns_about_a_missing_project_material_database():
    bom = pd.DataFrame([bom_row("MAT-1", custom_material_name="Concrete")])

    findings = collected_findings(tables_without_project_material_database(bom))

    assert [str(finding) for finding in findings] == [
        "E19: 'Concrete' has no mapping; the field was left empty and not guessed",
        "E34: Sheet is missing or empty, its lines were generated from the bill of materials",
    ]
    assert findings[1].source == "Project Material Database"
    assert findings[1].severity is Severity.WARNING


def test_project_package_from_tables_generates_lines_when_the_sheet_is_missing():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Wood", material_weight_kg="50"),
    ])

    loaded = tables_without_project_material_database(bom)
    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(loaded, findings=findings)

    assert [
        (record.custom_material_name, record.material_ref_id, record.bom_row_count)
        for record in project.project_material_database
    ] == [
        ("Concrete", "M0001", 1),
        ("Wood", "M0002", 1),
    ]
    assert {record.material_id: record.material_ref_id for record in project.bill_of_materials} == {
        "MAT-1": "M0001",
        "MAT-2": "M0002",
    }


def test_project_package_from_tables_in_draft_mode_generates_lines_when_the_sheet_is_missing():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Wood", material_weight_kg="50"),
    ])

    loaded = tables_without_project_material_database(bom)
    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(loaded, findings=findings, draft=True)
    findings.extend(validate_project(project, loaded))

    assert [str(finding) for finding in findings] == [
        "E19: 'Concrete' has no mapping; the field was left empty and not guessed",
        "E19: 'Wood' has no mapping; the field was left empty and not guessed",
        "E34: Sheet is missing or empty, its lines were generated from the bill of materials",
    ]

    assert [
        (record.custom_material_name, record.material_ref_id, record.bom_row_count)
        for record in project.project_material_database
    ] == [
        ("Concrete", "M0001", 1),
        ("Wood", "M0002", 1),
    ]
    assert {record.material_id: record.material_ref_id for record in project.bill_of_materials} == {
        "MAT-1": "M0001",
        "MAT-2": "M0002",
    }


def test_bom_from_dataframe_keeps_missing_material_reference_service_life():
    result = bom_from_dataframe(bom_df("mat-1"))

    assert len(result) == 1
    assert result[0].material_reference_service_life is None


def test_bom_from_dataframe_drop_invalid_keeps_rows_missing_material_reference_service_life():
    result = bom_from_dataframe(bom_df("mat-1", "mat-2"), drop_invalid=True)

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


def test_bom_ignores_an_unnamed_sheet_column():
    # A styled but empty sheet column has a NaN header. It must not match the blank
    # source cells of the translator, which all used to map to one field code.
    dataframe = bom_df("MAT-1").drop(columns=["material_id"])
    dataframe[float("nan")] = None
    translator = DocumentTranslator.from_csv_dir(
        Path(__file__).parents[1] / "translators" / "translator_at", 0, 1, 5, 6, 0
    )
    findings: list[OpenBDFValidationError] = []

    result = bom_from_dataframe(dataframe, translator, findings=findings)

    assert [str(finding) for finding in findings] == []
    assert [item.material_id for item in result] == ["MAT-1"]


def test_project_package_from_tables_drop_invalid_drops_missing_required():
    valid = bom_df("mat-1")
    invalid = bom_df("mat-2").drop(columns=["custom_material_name"])
    dataframe = pd.concat([valid, invalid], ignore_index=True)

    project = project_package_from_tables(tables(dataframe), drop_invalid=True)

    assert [b.material_id for b in project.bill_of_materials] == ["mat-1"]


def test_dropped_line_is_reported_as_a_warning():
    valid = bom_df("mat-1")
    invalid = bom_df("mat-2").drop(columns=["custom_material_name"])
    dataframe = pd.concat([valid, invalid], ignore_index=True)
    findings: list[OpenBDFValidationError] = []

    bom_from_dataframe(dataframe, findings=findings, drop_invalid=True)

    assert [str(finding) for finding in findings] == [
        "E33: Row 2: line dropped (material_id 'mat-2'): Field custom_material_name is required and was not provided"
    ]
    assert findings[0].severity is Severity.WARNING
    assert findings[0].source == "Bill of Materials"
    assert findings[0].row == 2


def test_a_line_dropped_without_a_material_id_names_no_material():
    invalid = pd.DataFrame([{"material_id": None, "custom_material_name": "Concrete"}])
    findings: list[OpenBDFValidationError] = []

    bom_from_dataframe(invalid, findings=findings, drop_invalid=True)

    assert [str(finding) for finding in findings] == [
        "E33: Row 1: line dropped: Field material_id is required and was not provided"
    ]


def test_bom_from_dataframe_allows_missing_material_reference_service_life():
    records = bom_from_dataframe(bom_df("mat-1"))

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
        tables(bom_df("mat-1"), project_material_database=project_material_database_df("Material mat-1"))
    )

    assert [record.material_ref_id for record in project.project_material_database] == ["M0001"]
    assert all(record.project_record is project for record in project.project_material_database)


def test_project_package_from_tables_validates_consistent_project_material_database():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_ref_id="M0001", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Concrete", material_ref_id="M0001"),
        bom_row("MAT-3", custom_material_name="Wood", material_ref_id="M0002", material_weight_kg="50"),
    ])
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Concrete"),
        project_material_database_row("M0002", "Wood"),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pmd))

    assert [record.custom_material_name for record in project.project_material_database] == ["Concrete", "Wood"]


def test_project_package_from_tables_reports_missing_project_material_database_lines():
    pmd = project_material_database_df("Material mat-1")

    findings = collected_findings(tables(bom_df("mat-1", "mat-2"), project_material_database=pmd))

    assert [str(finding) for finding in findings] == [
        "E19: 'Material mat-1' has no mapping; the field was left empty and not guessed",
        "E19: 'Material mat-2' has no mapping; the field was left empty and not guessed",
        "E28: Bill of materials material 'Material mat-2' with EPD dataset 'value' "
        "has no project material database line",
    ]
    assert findings[0].source == "Bill of Materials"


def test_project_package_from_tables_reports_orphan_project_material_database_lines():
    pmd = project_material_database_df("Material mat-1", "Orphan material")

    findings = collected_findings(tables(bom_df("mat-1"), project_material_database=pmd))

    assert [str(finding) for finding in findings] == [
        "E19: 'Material mat-1' has no mapping; the field was left empty and not guessed",
        "E27: Project material database line 'Orphan material' with EPD dataset 'value' "
        "has no bill of materials material",
    ]


def test_project_package_from_tables_reports_duplicate_project_material_database_lines():
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Material mat-1"),
        project_material_database_row("M0002", "Material mat-1"),
    ])

    findings = collected_findings(tables(bom_df("mat-1"), project_material_database=pmd))

    assert [str(finding) for finding in findings] == [
        "E19: 'Material mat-1' has no mapping; the field was left empty and not guessed",
        "E29: Bill of materials material 'Material mat-1' with EPD dataset 'value' "
        "has 2 project material database lines",
    ]


def test_project_package_from_tables_aligns_a_contradicting_material_ref_id_and_warns():
    bom = pd.DataFrame([bom_row("MAT-1", custom_material_name="Concrete", material_ref_id="M0002")])
    pmd = project_material_database_df("Concrete")

    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(tables(bom, project_material_database=pmd), findings=findings)
    findings.extend(validate_project(project, tables(bom, project_material_database=pmd)))

    assert [str(finding) for finding in sort_findings(findings)] == [
        "E04: Field material_ref_id is derived; the given value was discarded",
        "E19: 'Concrete' has no mapping; the field was left empty and not guessed",
    ]
    assert [record.material_ref_id for record in project.bill_of_materials] == ["M0001"]


def test_project_package_from_tables_reports_duplicate_project_material_database_ids():
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Material mat-1"),
        project_material_database_row("M0001", "Material mat-2"),
    ])

    findings = collected_findings(tables(bom_df("mat-1", "mat-2"), project_material_database=pmd))

    assert [str(finding) for finding in findings] == [
        "E19: 'Material mat-1' has no mapping; the field was left empty and not guessed",
        "E19: 'Material mat-2' has no mapping; the field was left empty and not guessed",
        "E31: material_ref_id 'M0001' is used by 2 project material database lines",
    ]


def test_project_package_from_tables_allows_empty_material_ref_ids_under_a_grouped_name():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete"),
        bom_row("MAT-2", custom_material_name="Concrete", material_ref_id="M0001"),
    ])
    pmd = project_material_database_df("Concrete")

    project = project_package_from_tables(tables(bom, project_material_database=pmd))

    assert [record.custom_material_name for record in project.project_material_database] == ["Concrete"]


def test_project_package_from_tables_in_draft_mode_adds_missing_project_material_database_lines():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_ref_id="M0001"),
        bom_row("MAT-2", custom_material_name="Wood", material_ref_id="M0003"),
        bom_row("MAT-3", custom_material_name="Glass"),
    ])
    pmd = pd.DataFrame([project_material_database_row("M0001", "Concrete")])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    lines = project.project_material_database
    assert [(record.custom_material_name, record.material_ref_id) for record in lines] == [
        ("Concrete", "M0001"),
        ("Wood", "M0004"),
        ("Glass", "M0005"),
    ]
    assert all(isinstance(record, ProjectMaterialDatabaseBase) for record in lines)


def test_project_package_from_tables_in_draft_mode_generates_lines_from_an_empty_project_material_database():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Wood", material_weight_kg="50"),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert [(record.custom_material_name, record.material_ref_id) for record in lines] == [
        ("Concrete", "M0001"),
        ("Wood", "M0002"),
    ]
    assert lines[0].material_mass_kg == Decimal("100")
    assert lines[1].material_mass_kg == Decimal("50")
    assert all(isinstance(record, ProjectMaterialDatabaseBase) for record in lines)
    refs = {record.material_id: record.material_ref_id for record in project.bill_of_materials}
    assert refs == {"MAT-1": "M0001", "MAT-2": "M0002"}


def test_project_package_from_tables_in_draft_mode_keeps_existing_project_material_database_lines():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_ref_id="M0001", material_weight_kg="123"),
        bom_row("MAT-2", custom_material_name="Wood"),
    ])
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Concrete", material_mass_kg="999", material_mass_share="0.5"),
        {"material_ref_id": "…", "custom_material_name": "…"},
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    lines = project.project_material_database
    assert [record.custom_material_name for record in lines] == ["Concrete", "…", "Wood"]
    concrete, placeholder, wood = lines
    assert concrete.material_ref_id == "M0001"
    assert concrete.bom_row_count == 1
    assert concrete.material_mass_kg == Decimal("123")
    assert concrete.material_mass_share == Decimal("100.0000")
    assert placeholder.material_ref_id == "…"
    assert placeholder.bom_row_count == 0
    assert placeholder.material_mass_kg == Decimal("0")
    assert placeholder.material_mass_share == Decimal("0")
    assert wood.material_ref_id == "M0002"


def test_project_package_from_tables_in_draft_mode_back_fills_material_ref_ids():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_ref_id="M0001"),
        bom_row("MAT-2", custom_material_name="Concrete", material_ref_id="M0002"),
        bom_row("MAT-3", custom_material_name="Wood", material_ref_id="M0099"),
        bom_row("MAT-4", custom_material_name=None, material_ref_id="M0098"),
    ])
    pmd = pd.DataFrame([project_material_database_row("M0001", "Concrete")])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    refs = {record.material_id: record.material_ref_id for record in project.bill_of_materials}
    assert refs["MAT-1"] == "M0001"
    assert refs["MAT-2"] == "M0001"
    assert refs["MAT-3"] == "M0100"
    assert refs["MAT-4"] == "M0098"


def test_project_package_from_tables_in_draft_mode_generates_line_values_from_the_bom():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_weight_kg="100"),
        bom_row(
            "MAT-2",
            custom_material_name="Wood",
            material_weight_kg="100",
            floor_repetition=2,
            lca_dataset_material_name="Wood EPD",
        ),
        bom_row(
            "MAT-3",
            custom_material_name="Wood",
            material_weight_kg="50",
            lca_dataset_material_name="Wood EPD",
            lca_database_name="OKOBAUDAT",
        ),
    ])
    pmd = pd.DataFrame([project_material_database_row("M0001", "Concrete", material_mass_kg="999")])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    concrete = project.project_material_database[0]
    wood = project.project_material_database[1]
    assert wood.material_ref_id == "M0002"
    assert wood.bom_row_count == 2
    assert wood.material_mass_kg == Decimal("250")
    assert wood.material_mass_share == Decimal("71.4286")
    assert wood.lca_dataset_material_name == "Wood EPD"
    assert wood.lca_database_name == "OKOBAUDAT"
    assert concrete.material_mass_kg == Decimal("100")


def test_project_package_from_tables_in_draft_mode_ignores_rows_without_a_material_name():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Concrete", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name=None, material_ref_id="M0099", material_weight_kg="500"),
    ])
    pmd = pd.DataFrame([{"material_ref_id": "…", "custom_material_name": "…"}])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    lines = project.project_material_database
    assert [record.custom_material_name for record in lines] == ["…", "Concrete"]
    concrete = lines[1]
    assert concrete.material_ref_id == "M0100"
    assert concrete.bom_row_count == 1
    assert concrete.material_mass_kg == Decimal("100")
    assert concrete.material_mass_share == Decimal("100.0000")
    refs = {record.material_id: record.material_ref_id for record in project.bill_of_materials}
    assert refs["MAT-1"] == "M0100"
    assert refs["MAT-2"] == "M0099"


def test_project_package_from_tables_in_draft_mode_splits_one_material_name_by_epd_dataset():
    bom = pd.DataFrame([
        bom_row(
            "MAT-1",
            custom_material_name="Kies",
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            material_weight_kg="300",
        ),
        bom_row(
            "MAT-2",
            custom_material_name="Kies",
            lca_dataset_material_name="Kies (Korngröße 0/16)",
            material_weight_kg="100",
        ),
        bom_row(
            "MAT-3",
            custom_material_name="Kies",
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            material_weight_kg="200",
        ),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert [(line.lca_dataset_material_name, line.material_ref_id) for line in lines] == [
        ("Kies (Korngröße 2/32)", "M0001"),
        ("Kies (Korngröße 0/16)", "M0002"),
    ]
    coarse, fine = lines
    assert coarse.bom_row_count == 2
    assert coarse.material_mass_kg == Decimal("500")
    assert fine.bom_row_count == 1
    assert fine.material_mass_kg == Decimal("100")
    assert coarse.material_mass_share == Decimal("83.3333")
    assert fine.material_mass_share == Decimal("16.6667")
    assert coarse.material_mass_share + fine.material_mass_share == Decimal("100.0000")
    refs = [record.material_ref_id for record in project.bill_of_materials]
    assert refs == ["M0001", "M0002", "M0001"]


def test_project_package_from_tables_in_draft_mode_treats_blank_epd_datasets_as_one_material():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", lca_dataset_material_name=None, material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Kies", lca_dataset_material_name="", material_weight_kg="100"),
        bom_row("MAT-3", custom_material_name="Kies", lca_dataset_material_name="   ", material_weight_kg="100"),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert len(lines) == 1
    line = lines[0]
    assert line.material_ref_id == "M0001"
    assert line.lca_dataset_material_name is None
    assert line.bom_row_count == 3
    assert line.material_mass_kg == Decimal("300")
    assert line.material_mass_share == Decimal("100.0000")
    assert [record.material_ref_id for record in project.bill_of_materials] == ["M0001", "M0001", "M0001"]


def test_project_package_from_tables_in_draft_mode_matches_material_pairs_ignoring_case_and_spaces():
    bom = pd.DataFrame([
        bom_row(
            "MAT-1",
            custom_material_name="Kies",
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            material_weight_kg="100",
        ),
        bom_row(
            "MAT-2",
            custom_material_name="  KIES ",
            lca_dataset_material_name="  kies (KORngröße 2/32) ",
            material_weight_kg="200",
        ),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert len(lines) == 1
    line = lines[0]
    assert line.custom_material_name == "Kies"
    assert line.lca_dataset_material_name == "Kies (Korngröße 2/32)"
    assert line.bom_row_count == 2
    assert line.material_mass_kg == Decimal("300")
    assert [record.material_ref_id for record in project.bill_of_materials] == ["M0001", "M0001"]


def test_project_package_from_tables_in_draft_mode_recomputes_automatic_fields_of_a_matched_line():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", material_ref_id="M0001", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Kies", material_ref_id="M0001", material_weight_kg="200"),
    ])
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Kies", bom_row_count=99, material_mass_kg="1", material_mass_share="1"),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    lines = project.project_material_database
    assert len(lines) == 1
    line = lines[0]
    assert line.material_ref_id == "M0001"
    assert line.bom_row_count == 2
    assert line.material_mass_kg == Decimal("300")
    assert line.material_mass_share == Decimal("100.0000")


def test_project_package_from_tables_in_draft_mode_keeps_an_unmatched_line_and_generates_one_for_the_bom_pair():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", lca_dataset_material_name=None, material_weight_kg="100"),
    ])
    pmd = pd.DataFrame([
        project_material_database_row(
            "M0001",
            "Kies",
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            bom_row_count=7,
            material_mass_kg="7",
            material_mass_share="0.7",
        ),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pmd), draft=True)

    lines = project.project_material_database
    assert [(line.custom_material_name, line.material_ref_id) for line in lines] == [
        ("Kies", "M0001"),
        ("Kies", "M0002"),
    ]
    parsed, generated = lines
    assert parsed.lca_dataset_material_name == "Kies (Korngröße 2/32)"
    assert parsed.bom_row_count == 0
    assert parsed.material_mass_kg == Decimal("0")
    assert parsed.material_mass_share == Decimal("0")
    assert generated.lca_dataset_material_name is None
    assert generated.bom_row_count == 1
    assert generated.material_mass_kg == Decimal("100")
    assert generated.material_mass_share == Decimal("100.0000")
    assert [record.material_ref_id for record in project.bill_of_materials] == ["M0002"]


def test_project_package_from_tables_in_draft_mode_ignores_rows_with_a_dataset_but_no_material_name():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", material_weight_kg="100"),
        bom_row(
            "MAT-2",
            custom_material_name=None,
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            material_weight_kg="500",
        ),
        bom_row(
            "MAT-3",
            custom_material_name="   ",
            lca_dataset_material_name="Kies (Korngröße 2/32)",
            material_weight_kg="500",
        ),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert [(line.custom_material_name, line.material_ref_id, line.bom_row_count) for line in lines] == [
        ("Kies", "M0001", 1)
    ]
    assert lines[0].material_mass_kg == Decimal("100")
    assert lines[0].material_mass_share == Decimal("100.0000")
    refs = {record.material_id: record.material_ref_id for record in project.bill_of_materials}
    assert refs == {"MAT-1": "M0001", "MAT-2": None, "MAT-3": None}


def test_project_package_from_tables_reports_a_dataset_mismatch_as_missing_and_orphan():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", lca_dataset_material_name="Kies (Korngröße 0/16)"),
    ])
    pmd = pd.DataFrame([
        project_material_database_row("M0001", "Kies", lca_dataset_material_name="Kies (Korngröße 2/32)"),
    ])

    findings = collected_findings(tables(bom, project_material_database=pmd))

    assert [str(finding) for finding in findings] == [
        "E19: 'Kies' has no mapping; the field was left empty and not guessed",
        "E28: Bill of materials material 'Kies' with EPD dataset 'Kies (Korngröße 0/16)' "
        "has no project material database line",
        "E27: Project material database line 'Kies' with EPD dataset 'Kies (Korngröße 2/32)' "
        "has no bill of materials material",
    ]


def test_project_package_from_tables_in_draft_mode_counts_a_missing_floor_repetition_once_and_a_zero_never():
    bom = pd.DataFrame([
        bom_row("MAT-1", custom_material_name="Kies", material_weight_kg="100"),
        bom_row("MAT-2", custom_material_name="Kies", material_weight_kg="100", floor_repetition=None),
        bom_row("MAT-3", custom_material_name="Kies", material_weight_kg="100", floor_repetition=0),
    ])

    project = project_package_from_tables(tables(bom, project_material_database=pd.DataFrame()), draft=True)

    lines = project.project_material_database
    assert len(lines) == 1
    assert lines[0].bom_row_count == 3
    assert lines[0].material_mass_kg == Decimal("200")
    assert lines[0].material_mass_share == Decimal("100.0000")


def test_parse_value_tries_an_enum_before_the_blank_aliases():
    assert parse_value(BuildingEnergyClassificationSystem | None, "None") is BuildingEnergyClassificationSystem.NONE
    assert parse_value(str | None, "None") is None
