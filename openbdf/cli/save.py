import importlib.resources
import itertools
import re
from copy import copy
from pathlib import Path
from typing import TypeVar

import numpy as np
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Protection, Side
from openpyxl.styles.cell_style import StyleArray
from openpyxl.utils import get_column_letter
from openpyxl.writer.theme import theme_xml
from pydantic.fields import FieldInfo
from sqlmodel import SQLModel

from openbdf.lib.converters.dataframe import horizontal_to_dataframe
from openbdf.lib.converters.enums_registry import Boolean, EnumRegistry
from openbdf.lib.converters.translators import (
    ABOUT_SHEET_NAME,
    COMMON_CATEGORY_PROPERTIES,
    SHEETS_PROPERTIES_HEADERS,
)
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.human_readable import human_readable_constraints, human_readable_type
from openbdf.lib.types.xlsx import xlsx_validation_from_type
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.enums.buildings import (
    AboveBelowGround,
    BuildingClassificationCode,
    BuildingElementClassificationTier,
    BuildingFacingDirection,
    BuildingStructureType,
    BuildingTypology,
    FloorAreaInclusions,
    FoundationType,
    GFAMeasurementMethod,
    GrossFloorAreaStandard,
    SharedComponentAllocationRule,
)
from openbdf.model.enums.countries import Country
from openbdf.model.enums.element_classifications import OpenBDFBuildingElementClassification
from openbdf.model.enums.energy import (
    BuildingEnergyClassificationSystem,
    BuildingEnergyCodeSystem,
    EmissionFactorScenario,
    OnSiteRenewableAllocationApproach,
    PrimaryEnergySource,
)
from openbdf.model.enums.geography import ClimateZone, ExtendedDefaultDataBasis, FEMASeismicActivity, SoilType
from openbdf.model.enums.lca import (
    AssessmentType_EN15978,
    BiogenicCarbonAccounting,
    DataWeightingBasis,
    LCADatabase,
    LCADatabaseSystemModel,
    LCAStageOrModuleOrSubModule,
    LCATemporalApproach,
    LCIAMethodology,
    LCIModelingApproach,
    LifeCycleSystemBoundary,
    LimitValueScopeReduction,
)
from openbdf.model.enums.materials import (
    DeclaredUnit,
    MaterialDataType,
    MaterialEPDMatch,
    MaterialFlowType,
    MaterialQuantitiesSource,
    OpenBDFMaterialClassification,
    ReplacementCountMethod,
)
from openbdf.model.enums.openbdf_enum import OpenBDFEnum
from openbdf.model.enums.project import ConstructionType, ProjectPhase, ProjectPhaseCommon, ProjectUnits, RecordType
from openbdf.model.enums.requirement import Requirement
from openbdf.model.general_info import ProjectRecordBase
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBase
from openbdf.model.tables import ProjectRecord

thin_side = Side(border_style="thin", color="AAAAAA")

ATTRIBUTES_NAME_STYLE = NamedStyle(
    "AttributeName", font=Font(name="Calibri", bold=True, color="FFFFFF"), fill=PatternFill("solid", fgColor="2b5b47")
)
INFO_STYLE = NamedStyle("Info", font=Font(name="Calibri", italic=True))
FIELD_CODE_STYLE = NamedStyle(
    "FieldCode", font=Font(name="Calibri", color="FFFFFF"), fill=PatternFill("solid", fgColor="010101")
)
REQUIRED_STYLE = NamedStyle("Required", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="189d7e"))
STRONGLY_RECOMMENDED_STYLE = NamedStyle(
    "Strongly recommended", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="31658d")
)
RECOMMENDED_STYLE = NamedStyle("Recommended", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="3592e3"))
SUGGESTED_STYLE = NamedStyle("Suggested", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="9dd2f3"))
OPTIONAL_STYLE = NamedStyle("Optional", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="e9f7fe"))
AUTOMATIC_STYLE = NamedStyle("Automatic", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="bcc4c2"))
REQUIREMENT_STYLES: dict[Requirement, NamedStyle] = {
    Requirement.REQUIRED: REQUIRED_STYLE,
    Requirement.STRONGLY_RECOMMENDED: STRONGLY_RECOMMENDED_STYLE,
    Requirement.RECOMMENDED: RECOMMENDED_STYLE,
    Requirement.SUGGESTED: SUGGESTED_STYLE,
    Requirement.OPTIONAL: OPTIONAL_STYLE,
    Requirement.AUTOMATIC: AUTOMATIC_STYLE,
}
ROW_HEADER_STYLE = NamedStyle("RowHeader", font=Font(name="Calibri", bold=True), alignment=Alignment(vertical="top"))
EDITABLE_VALUE_STYLE = NamedStyle(
    "EditableValue",
    font=Font(name="Calibri"),
    fill=PatternFill("solid", fgColor="feffb3"),
    border=Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side),
    protection=Protection(locked=False),
)
DISABLED_STYLE = NamedStyle(
    "Disabled",
    font=Font(name="Calibri"),
    fill=PatternFill("solid", fgColor="d3d3d3"),
)

ModelT = TypeVar("ModelT", bound=SQLModel)
ModelT2 = TypeVar("ModelT2", bound=SQLModel)

# Row 9 of the horizontal sheets and column L of General Information hold the reference
# or the reference alignment of the field, depending on the sheet.
REFERENCE_LABELS = {"reference": "Reference", "reference_alignment": "Reference Alignment"}

# Canonical TypeDefinitions column order for the template export.
TEMPLATE_TYPE_DEFINITIONS: tuple[type, ...] = (
    RecordType,
    ProjectUnits,
    ConstructionType,
    Country,
    GFAMeasurementMethod,
    ProjectPhase,
    ProjectPhaseCommon,
    ClimateZone,
    FEMASeismicActivity,
    BuildingTypology,
    BuildingEnergyClassificationSystem,
    BuildingEnergyCodeSystem,
    BuildingClassificationCode,
    BuildingElementClassificationTier,
    BuildingStructureType,
    SoilType,
    FoundationType,
    PrimaryEnergySource,
    BuildingFacingDirection,
    GrossFloorAreaStandard,
    FloorAreaInclusions,
    ReplacementCountMethod,
    LCADatabase,
    LCADatabaseSystemModel,
    DataWeightingBasis,
    LCATemporalApproach,
    LCIAMethodology,
    BiogenicCarbonAccounting,
    MaterialQuantitiesSource,
    AboveBelowGround,
    OpenBDFBuildingElementClassification,
    OpenBDFMaterialClassification,
    MaterialDataType,
    MaterialEPDMatch,
    DeclaredUnit,
    MaterialFlowType,
    LCAStageOrModuleOrSubModule,
    LCIModelingApproach,
    LifeCycleSystemBoundary,
    AssessmentType_EN15978,
    OnSiteRenewableAllocationApproach,
    Boolean,
    SharedComponentAllocationRule,
    ExtendedDefaultDataBasis,
    LimitValueScopeReduction,
    EmissionFactorScenario,
)

# Registering named styles once per workbook and assigning cells by name string
# (cell.style = "EditableValue") avoids openpyxl's expensive
# Serialisable.__eq__ comparison against every registered style on each call.
ALL_NAMED_STYLES: list[NamedStyle] = [
    ATTRIBUTES_NAME_STYLE,
    INFO_STYLE,
    FIELD_CODE_STYLE,
    REQUIRED_STYLE,
    RECOMMENDED_STYLE,
    OPTIONAL_STYLE,
    STRONGLY_RECOMMENDED_STYLE,
    SUGGESTED_STYLE,
    AUTOMATIC_STYLE,
    ROW_HEADER_STYLE,
    EDITABLE_VALUE_STYLE,
    DISABLED_STYLE,
]


def register_named_styles(writer: pd.ExcelWriter) -> None:
    """Register the shared named styles on the workbook once."""
    for style in ALL_NAMED_STYLES:
        writer.book.add_named_style(style)


def requirement_of(extra: dict, is_optional: bool) -> Requirement:
    """Requirement metadata of a field, defaulting on its Python optionality."""
    return extra.get("requirements", Requirement.OPTIONAL if is_optional else Requirement.REQUIRED)


def set_theme_fonts(writer: pd.ExcelWriter) -> None:
    """Pin the theme major font to Calibri to match the minor font."""
    writer.book.loaded_theme = theme_xml.replace('<a:latin typeface="Cambria"/>', '<a:latin typeface="Calibri"/>')


def named_style_arrays(writer: pd.ExcelWriter) -> dict[str, StyleArray]:
    """Resolved style arrays for the named styles registered on the workbook.

    A copy of one of these arrays assigned to cell._style is what openpyxl
    itself stores for cell.style = name, but without the named-style lookup
    that rebuilds the style name list on every call.
    """
    return {style.name: style._style for style in writer.book._named_styles}


def get_field_extra(field: FieldInfo) -> dict:
    """Safely extracts json_schema_extra if it is a dictionary."""
    extra = field.json_schema_extra
    return extra if isinstance(extra, dict) else {}


ABOUT_WIDTH = 80
HYPERLINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|<((?:https?|mailto):[^>]+)>")
HYPERLINK_FONT = Font(name="Calibri", color="0563C1", underline="single")
ABOUT_TITLE_FONT = Font(name="Calibri", bold=True, size=14, color="2B5B47")


def about_text_rows(text: str) -> list[tuple[str, str | None]]:
    """Plain markdown text to rows wrapped at spaces before 80 characters; separator-only fragments between links are dropped."""
    text = text.replace("**", "").lstrip("#> ").strip()
    if not text.strip(", "):
        return []
    rows: list[tuple[str, str | None]] = []
    current = ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > ABOUT_WIDTH:
            rows.append((current, None))
            current = word
        else:
            current = f"{current} {word}".strip()
    return [*rows, (current, None)] if current else rows


def about_line_rows(line: str) -> list[tuple[str, str | None]]:
    """One markdown line becomes (text, url) rows; links get their own row since Excel allows one hyperlink per cell."""
    rows: list[tuple[str, str | None]] = []
    position = 0
    for match in HYPERLINK_PATTERN.finditer(line):
        rows.extend(about_text_rows(line[position : match.start()]))
        display = match.group(1) if match.group(1) is not None else match.group(3)
        rows.append((display, match.group(2) or match.group(3)))
        position = match.end()
    rows.extend(about_text_rows(line[position:]))
    return rows or [("", None)]


def about_to_xlsx(writer: pd.ExcelWriter) -> None:
    about_text = importlib.resources.files("openbdf").joinpath("about.md").read_text(encoding="utf-8")
    about_sheet = writer.book.create_sheet(ABOUT_SHEET_NAME)
    about_sheet.column_dimensions["A"].width = ABOUT_WIDTH + 5
    cell_row = 1
    for line in about_text.splitlines():
        title = line.startswith("#")
        notice = line.lstrip().startswith(">")
        for text, url in about_line_rows(line):
            cell = about_sheet.cell(row=cell_row, column=1, value=text)
            if url:
                cell.hyperlink = url
                cell.font = HYPERLINK_FONT
            elif title:
                cell.font = ABOUT_TITLE_FONT
            elif notice:
                cell.style = INFO_STYLE.name
            cell_row += 1


def save_openbdf_to_xlsx(
    xlsx_path: str | Path,
    project: ProjectRecord | None,
    info_sheet_name: str = COMMON_CATEGORY_PROPERTIES["project"]["name"],
    bom_sheet_name: str = COMMON_CATEGORY_PROPERTIES["bom"]["name"],
    project_material_database_sheet_name: str = COMMON_CATEGORY_PROPERTIES["material_database"]["name"],
    results_wide_sheet_name: str = COMMON_CATEGORY_PROPERTIES["results_wide"]["name"],
    results_tall_sheet_name: str = COMMON_CATEGORY_PROPERTIES["results_tall"]["name"],
):
    """Save a list of BuildingBillMaterialsSlimRecord to an Excel file."""

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        register_named_styles(writer)
        set_theme_fonts(writer)
        enum_registry = EnumRegistry()
        enum_registry.register(*TEMPLATE_TYPE_DEFINITIONS)

        about_to_xlsx(writer)
        info_to_xlsx(writer, project, info_sheet_name, enum_registry)
        wide_to_xlsx(
            writer,
            project.bill_of_materials if project else None,
            BuildingBillMaterialsSlimRecordBase,
            bom_sheet_name,
            enum_registry,
            reference_attribute="reference",
        )
        wide_to_xlsx(
            writer,
            project.project_material_database if project else None,
            ProjectMaterialDatabaseBase,
            project_material_database_sheet_name,
            enum_registry,
            reference_attribute="reference",
        )
        wide_to_xlsx(
            writer,
            [record.lca_results_full_record for record in project.bill_of_materials if record.lca_results_full_record]
            if project
            else None,
            LCAResultsWideFullBase,
            results_wide_sheet_name,
            enum_registry,
            reference_attribute="reference_alignment",
        )
        wide_to_xlsx(
            writer,
            [
                item
                for record in project.bill_of_materials
                if record.lca_results_tall_full_records
                for item in record.lca_results_tall_full_records
            ]
            if project
            else None,
            LCAResultsTallBase,
            results_tall_sheet_name,
            enum_registry,
            reference_attribute="reference_alignment",
        )

        enum_registry.to_xlsx(writer)


def info_to_xlsx(writer: pd.ExcelWriter, project: ProjectRecord | None, sheet_name: str, enum_registry: EnumRegistry):
    info_sheet = writer.book.create_sheet(sheet_name)
    info_sheet.protection.sheet = True  # Lock the sheet to prevent accidental edits

    project_record_fields = ProjectRecordBase.model_fields  # Base is on purpose to avoid DB-only fields like ID, etc...

    for cell_row, field_code in enumerate(project_record_fields, start=2):  # xlsx are 1-indexed (ewww)
        metadata = project_record_fields.get(field_code)
        if not metadata:
            continue

        extra = get_field_extra(metadata)
        data_type, is_optional = unwrap_optional(metadata.annotation)
        requirements = requirement_of(extra, is_optional)

        header_cells = []

        g = info_sheet.cell(row=cell_row, column=1, value=extra.get("group", field_code))
        header_cells.append(g)

        sg = info_sheet.cell(row=cell_row, column=2, value=extra.get("sub_group", field_code))
        header_cells.append(sg)

        an = info_sheet.cell(row=cell_row, column=3, value=extra.get("attribute_name", field_code))
        header_cells.append(an)

        fc = info_sheet.cell(row=cell_row, column=4, value=extra.get("field_code", field_code))
        header_cells.append(fc)

        desc = info_sheet.cell(
            row=cell_row,
            column=5,
            value=metadata.description if metadata and metadata.description else field_code,
        )
        header_cells.append(desc)

        dt = info_sheet.cell(row=cell_row, column=6, value=human_readable_type(data_type))
        dt.style = INFO_STYLE.name

        constraints = extra.get("constraint")
        c = info_sheet.cell(row=cell_row, column=7, value=constraints)
        if constraints:
            c.style = INFO_STYLE.name
        else:
            c.style = DISABLED_STYLE.name

        units = extra.get("units", "")
        u = info_sheet.cell(row=cell_row, column=8, value=units)
        if units:
            u.style = INFO_STYLE.name
        else:
            u.style = DISABLED_STYLE.name

        r = info_sheet.cell(row=cell_row, column=9, value=requirements.display_name)
        r.style = REQUIREMENT_STYLES[requirements].name

        reference = extra.get("reference")
        ref = info_sheet.cell(row=cell_row, column=11, value=reference or "")
        ref.style = INFO_STYLE.name if reference else DISABLED_STYLE.name

        v = info_sheet.cell(row=cell_row, column=10, value=getattr(project, field_code) if project else "")
        v.style = EDITABLE_VALUE_STYLE.name

        dv = xlsx_validation_from_type(data_type, is_optional, metadata, enum_registry)  # type: ignore[arg-type]
        if dv:
            dv.add(v)
            info_sheet.add_data_validation(dv)

        if requirements is Requirement.REQUIRED:
            for c in header_cells:
                c.style = REQUIRED_STYLE.name

    a = info_sheet.cell(row=1, column=1, value="Group")
    a.style = ATTRIBUTES_NAME_STYLE.name
    d = info_sheet.cell(row=1, column=2, value="Sub-group")
    d.style = ATTRIBUTES_NAME_STYLE.name
    dt = info_sheet.cell(row=1, column=3, value="Attribute Name")
    dt.style = ATTRIBUTES_NAME_STYLE.name
    c = info_sheet.cell(row=1, column=4, value="Field Code")
    c.style = ATTRIBUTES_NAME_STYLE.name
    u = info_sheet.cell(row=1, column=5, value="Description")
    u.style = ATTRIBUTES_NAME_STYLE.name
    r = info_sheet.cell(row=1, column=6, value="Datatype")
    r.style = ATTRIBUTES_NAME_STYLE.name
    ui = info_sheet.cell(row=1, column=7, value="Constraint")
    ui.style = ATTRIBUTES_NAME_STYLE.name
    fc = info_sheet.cell(row=1, column=8, value="Units")
    fc.style = ATTRIBUTES_NAME_STYLE.name
    fc = info_sheet.cell(row=1, column=9, value="Requirements")
    fc.style = ATTRIBUTES_NAME_STYLE.name
    fc = info_sheet.cell(row=1, column=10, value="Value")
    fc.style = ATTRIBUTES_NAME_STYLE.name
    fc = info_sheet.cell(row=1, column=11, value="Reference")
    fc.style = ATTRIBUTES_NAME_STYLE.name

    info_sheet.column_dimensions["A"].width = 10
    info_sheet.column_dimensions["B"].width = 20
    info_sheet.column_dimensions["C"].width = 30
    info_sheet.column_dimensions["D"].width = 30
    info_sheet.column_dimensions["E"].width = 40
    info_sheet.column_dimensions["F"].width = 30
    info_sheet.column_dimensions["G"].width = 25
    info_sheet.column_dimensions["H"].width = 15
    info_sheet.column_dimensions["I"].width = 25
    info_sheet.column_dimensions["J"].width = 25
    info_sheet.column_dimensions["K"].width = 40


def wide_to_xlsx(
    writer: pd.ExcelWriter,
    records: list[ModelT] | None,
    model_cls: type[ModelT2],
    sheet_name: str,
    enum_registry: EnumRegistry,
    reference_attribute: str,
    min_rows: int = 100,
):
    if records is None:
        records = []

    df = horizontal_to_dataframe(records, model_cls)  # type: ignore[misc]
    style_arrays = named_style_arrays(writer)
    editable_array = style_arrays[EDITABLE_VALUE_STYLE.name]
    disabled_array = style_arrays[DISABLED_STYLE.name]

    sheet = writer.book.create_sheet(sheet_name)
    # sheet.protection.sheet = True  # Lock the sheet to prevent accidental edits
    fields = model_cls.model_fields

    # headers
    for cell_column, field_code in enumerate(df.columns.tolist(), start=2):  # xlsx are 1-indexed (ewww)
        column_letter = get_column_letter(cell_column)

        metadata = fields.get(field_code)
        if not metadata:
            continue

        extra = get_field_extra(metadata)
        data_type, is_optional = unwrap_optional(metadata.annotation)
        requirements = requirement_of(extra, is_optional)

        attribute_name = extra.get("attribute_name", field_code)
        an = sheet.cell(row=1, column=cell_column, value=attribute_name)
        an.style = ATTRIBUTES_NAME_STYLE.name

        fc = sheet.cell(row=2, column=cell_column, value=field_code)
        fc.style = FIELD_CODE_STYLE.name

        desc = sheet.cell(
            row=3,
            column=cell_column,
            value=metadata.description if metadata and metadata.description else field_code,
        )
        if not is_optional:
            desc.style = REQUIRED_STYLE.name
        desc.alignment = Alignment(wrap_text=True, vertical="top")

        sheet.cell(row=4, column=cell_column, value=human_readable_type(data_type))

        constraints = extra.get("constraint") or human_readable_constraints(metadata)
        c = sheet.cell(row=5, column=cell_column, value=constraints)
        if constraints:
            c.style = INFO_STYLE.name
        else:
            c.style = DISABLED_STYLE.name

        unit = extra.get("units", "")
        u = sheet.cell(row=6, column=cell_column, value=unit)
        if unit:
            u.style = INFO_STYLE.name
        else:
            u.style = DISABLED_STYLE.name

        r = sheet.cell(row=7, column=cell_column, value=requirements.display_name)
        r.style = REQUIREMENT_STYLES[requirements].name

        reference = extra.get(reference_attribute)
        ref = sheet.cell(row=8, column=cell_column, value=reference or "")
        ref.style = INFO_STYLE.name if reference else DISABLED_STYLE.name

        dv = xlsx_validation_from_type(data_type, is_optional, metadata, enum_registry)  # type: ignore[arg-type]
        if dv:
            dv.add(
                f"{column_letter}9:{column_letter}1048576"
            )  # Apply validation to the whole column starting from the first data row
            sheet.add_data_validation(dv)

        sheet.column_dimensions[column_letter].width = max(
            15, len(attribute_name) + 5
        )  # Set column width based on header length

    a = sheet.cell(row=1, column=1, value="Attribute")
    a.style = ROW_HEADER_STYLE.name
    d = sheet.cell(row=2, column=1, value="Field Code")
    d.style = ROW_HEADER_STYLE.name
    dt = sheet.cell(row=3, column=1, value="Description")
    dt.style = ROW_HEADER_STYLE.name
    c = sheet.cell(row=4, column=1, value="Data Type")
    c.style = ROW_HEADER_STYLE.name
    u = sheet.cell(row=5, column=1, value="Constraint")
    u.style = ROW_HEADER_STYLE.name
    r = sheet.cell(row=6, column=1, value="Units")
    r.style = ROW_HEADER_STYLE.name
    cr = sheet.cell(row=7, column=1, value="Requirements")
    cr.style = ROW_HEADER_STYLE.name
    rf = sheet.cell(row=8, column=1, value=REFERENCE_LABELS[reference_attribute])
    rf.style = ROW_HEADER_STYLE.name

    last_col = len(df.columns) + 1
    start_data_row = 9
    end_data_row = start_data_row + max(len(df) - 1, min_rows)

    rows = df.itertuples(index=False, name=None)
    for row_idx in range(start_data_row, end_data_row + 1):
        sheet.cell(row=row_idx, column=1)._style = copy(disabled_array)
        row_values = next(rows, None)
        for col_idx in range(2, last_col + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            cell._style = copy(editable_array)
            if row_values is not None:
                value = row_values[col_idx - 2]
                if isinstance(value, np.generic):
                    value = value.item()
                if value is None or value != value:  # None and NaN are written as empty strings
                    value = ""
                cell.value = value

    sheet.row_dimensions[2].height = 15
    sheet.column_dimensions["A"].width = 20


def save_translator(
    xlsx_path: str | Path,
):
    """Save a template Excel file for the attribute translator."""
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        register_named_styles(writer)
        set_theme_fonts(writer)
        about_to_xlsx(writer)
        make_translations_library_template_xlsx(writer, "Translations Library")
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_PROPERTIES["project"]["name"], ProjectRecordBase.model_fields
        )
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_PROPERTIES["bom"]["name"], BuildingBillMaterialsSlimRecordBase.model_fields
        )
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_PROPERTIES["material_database"]["name"], ProjectMaterialDatabaseBase.model_fields
        )
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_PROPERTIES["results_wide"]["name"], LCAResultsWideFullBase.model_fields
        )
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_PROPERTIES["results_tall"]["name"], LCAResultsTallBase.model_fields
        )
        export_all_enums_in_model_to_translator(writer, ProjectRecordBase.model_fields)
        export_all_enums_in_model_to_translator(writer, BuildingBillMaterialsSlimRecordBase.model_fields)
        export_all_enums_in_model_to_translator(writer, ProjectMaterialDatabaseBase.model_fields)


def make_translations_library_template_xlsx(writer: pd.ExcelWriter, sheet_name: str):
    info_sheet = writer.book.create_sheet(sheet_name)
    info_sheet.cell(row=1, column=1, value=SHEETS_PROPERTIES_HEADERS["original_name"])
    info_sheet.cell(row=1, column=2, value=SHEETS_PROPERTIES_HEADERS["translated_name"])
    info_sheet.cell(row=1, column=3, value=SHEETS_PROPERTIES_HEADERS["orientation"])
    info_sheet.cell(row=1, column=4, value=SHEETS_PROPERTIES_HEADERS["header_row"])
    info_sheet.cell(row=1, column=5, value=SHEETS_PROPERTIES_HEADERS["header_col"])
    info_sheet.cell(row=1, column=6, value=SHEETS_PROPERTIES_HEADERS["values_col"])
    info_sheet.cell(row=1, column=7, value=SHEETS_PROPERTIES_HEADERS["start_row"])
    info_sheet.cell(row=1, column=8, value=SHEETS_PROPERTIES_HEADERS["start_col"])
    info_sheet.cell(row=1, column=9, value=SHEETS_PROPERTIES_HEADERS["end_row"])
    info_sheet.cell(row=1, column=10, value=SHEETS_PROPERTIES_HEADERS["end_col"])

    models = COMMON_CATEGORY_PROPERTIES.values()

    for cell_row, model in enumerate(models, start=2):  # xlsx are 1-indexed (ewww)
        info_sheet.cell(row=cell_row, column=2, value=model["name"])
        info_sheet.cell(row=cell_row, column=3, value=model["orientation"])
        info_sheet.cell(row=cell_row, column=4, value=0)

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 30
    info_sheet.column_dimensions["D"].width = 30
    info_sheet.column_dimensions["E"].width = 40
    info_sheet.column_dimensions["F"].width = 40
    info_sheet.column_dimensions["G"].width = 30
    info_sheet.column_dimensions["H"].width = 30
    info_sheet.column_dimensions["I"].width = 30
    info_sheet.column_dimensions["J"].width = 30


def make_translator_openbdf_pydantic(writer: pd.ExcelWriter, sheet_name: str, model: dict[str, FieldInfo]):
    info_sheet = writer.book.create_sheet(sheet_name)
    info_sheet.cell(row=1, column=1, value="Field code in your format")
    info_sheet.cell(row=1, column=2, value="OpenBDF field code")
    info_sheet.cell(row=1, column=3, value="OpenBDF attribute name")
    info_sheet.cell(row=1, column=4, value="Datatype")
    info_sheet.cell(row=1, column=5, value="Requirements")
    dv = info_sheet.cell(row=1, column=6, value="Default value")
    dv.style = ATTRIBUTES_NAME_STYLE.name
    preprocess = info_sheet.cell(row=1, column=7, value="Preprocess rule")
    preprocess.style = ATTRIBUTES_NAME_STYLE.name

    for cell_row, field_code in enumerate(model, start=2):  # xlsx are 1-indexed (ewww)
        metadata = model.get(field_code)
        if not metadata:
            continue

        extra = get_field_extra(metadata)
        data_type, is_optional = unwrap_optional(metadata.annotation)
        requirements = requirement_of(extra, is_optional)

        fc = info_sheet.cell(row=cell_row, column=2, value=field_code)
        fc.style = FIELD_CODE_STYLE.name

        an = info_sheet.cell(row=cell_row, column=3, value=extra.get("attribute_name", field_code))
        an.style = ATTRIBUTES_NAME_STYLE.name

        r = info_sheet.cell(row=cell_row, column=4, value=human_readable_type(data_type))
        r.style = INFO_STYLE.name

        req = info_sheet.cell(row=cell_row, column=5, value=requirements.display_name)
        req.style = REQUIREMENT_STYLES[requirements].name

        default_cell = info_sheet.cell(row=cell_row, column=6, value="")
        default_cell.style = EDITABLE_VALUE_STYLE.name
        preprocess_cell = info_sheet.cell(row=cell_row, column=7, value="")
        preprocess_cell.style = EDITABLE_VALUE_STYLE.name

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 20
    info_sheet.column_dimensions["D"].width = 40
    info_sheet.column_dimensions["E"].width = 40
    info_sheet.column_dimensions["F"].width = 30
    info_sheet.column_dimensions["G"].width = 30


def export_all_enums_in_model_to_translator(writer: pd.ExcelWriter, model: dict[str, FieldInfo]):
    for field in model.values():
        annotation = field.annotation
        data_type, _ = unwrap_optional(annotation)
        if isinstance(data_type, type) and issubclass(data_type, OpenBDFEnum):
            make_translator_openbdfenum(writer, data_type.__name__, data_type)


def make_translator_openbdfenum(writer: pd.ExcelWriter, sheet_name: str, enum: type[OpenBDFEnum]):
    if sheet_name in writer.book.sheetnames:
        return

    info_sheet = writer.book.create_sheet(sheet_name)

    info_sheet.cell(row=1, column=1, value="Value in your format")
    info_sheet.cell(row=1, column=2, value="OpenBDF enum value")
    info_sheet.cell(row=1, column=3, value="OpenBDF value display name")
    info_sheet.cell(row=1, column=4, value="OpenBDF value description (if any)")
    info_sheet.cell(row=1, column=5, value="OpenBDF value parent category (if applicable)")

    for cell_row, item in enumerate(enum, start=2):  # xlsx are 1-indexed (ewww)
        display_name = getattr(item, "display_name", None)
        description = getattr(item, "description", None)
        parent_category = getattr(item, "parent_category", None)

        fc = info_sheet.cell(row=cell_row, column=2, value=str(item.value))
        fc.style = FIELD_CODE_STYLE.name

        an = info_sheet.cell(row=cell_row, column=3, value=str(display_name) if display_name else str(item.value))
        an.style = ATTRIBUTES_NAME_STYLE.name

        d = info_sheet.cell(row=cell_row, column=4, value=str(description) if description else "")

        pc = info_sheet.cell(row=cell_row, column=5, value=str(parent_category[0]) if parent_category else "")

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 40
    info_sheet.column_dimensions["D"].width = 140
    info_sheet.column_dimensions["E"].width = 40
