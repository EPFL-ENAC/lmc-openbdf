import importlib.resources
import itertools
import re
from collections.abc import Callable, Collection
from copy import copy
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, TypeVar

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Protection, Side
from openpyxl.styles.cell_style import StyleArray
from openpyxl.utils import get_column_letter
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.writer.theme import theme_xml
from pydantic.fields import FieldInfo
from sqlmodel import SQLModel

from openbdf.lib.converters.dataframe import horizontal_to_dataframe
from openbdf.lib.converters.enums_registry import Boolean, EnumRegistry
from openbdf.lib.converters.translator_csv import csv_dir_rows, workbook_sheets_to_csv_dir
from openbdf.lib.converters.translators import (
    ABOUT_SHEET_NAME,
    COMMON_CATEGORY_PROPERTIES,
    FLOOR_LEVEL_CATEGORY,
    SHEETS_PROPERTIES_HEADERS,
)
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.human_readable import human_readable_constraints, human_readable_type
from openbdf.lib.types.xlsx import xlsx_validation_from_type
from openbdf.lib.validation.errors import AutomaticFieldSupplied, OpenBDFValidationError
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.enums.buildings import (
    AboveBelowGround,
    BuildingClassificationCode,
    BuildingElementClassificationTier,
    BuildingFacingDirection,
    BuildingStructureType,
    BuildingTypology,
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
from openbdf.model.enums.requirement import Requirement, requirement_of
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
REQUIRED_STYLE = NamedStyle(
    "Required", font=Font(name="Calibri", color="FFFFFF"), fill=PatternFill("solid", fgColor="189d7e")
)
STRONGLY_RECOMMENDED_STYLE = NamedStyle(
    "Strongly recommended", font=Font(name="Calibri", color="FFFFFF"), fill=PatternFill("solid", fgColor="3592e3")
)
RECOMMENDED_STYLE = NamedStyle(
    "Recommended", font=Font(name="Calibri", color="FFFFFF"), fill=PatternFill("solid", fgColor="72b7ed")
)
SUGGESTED_STYLE = NamedStyle("Suggested", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="b8e0f7"))
OPTIONAL_STYLE = NamedStyle("Optional", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="e9f7fe"))
AUTOMATIC_STYLE = NamedStyle("Automatic", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="d5e6e2"))
METADATA_STYLE = NamedStyle("Metadata", font=Font(name="Calibri"), fill=PatternFill("solid", fgColor="d5e6e2"))
FIRST_ROW_HEIGHT = 38
REQUIREMENT_STYLES: dict[Requirement, NamedStyle] = {
    Requirement.REQUIRED: REQUIRED_STYLE,
    Requirement.STRONGLY_RECOMMENDED: STRONGLY_RECOMMENDED_STYLE,
    Requirement.RECOMMENDED: RECOMMENDED_STYLE,
    Requirement.SUGGESTED: SUGGESTED_STYLE,
    Requirement.OPTIONAL: OPTIONAL_STYLE,
    Requirement.AUTOMATIC: AUTOMATIC_STYLE,
}
MARKED_REQUIREMENTS = (Requirement.REQUIRED, Requirement.STRONGLY_RECOMMENDED, Requirement.AUTOMATIC)
EDITABLE_VALUE_STYLE = NamedStyle(
    "EditableValue",
    font=Font(name="Calibri"),
    fill=PatternFill("solid", fgColor="feffb3"),
    border=Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side),
    protection=Protection(locked=False),
)
AUTOMATIC_VALUE_STYLE = NamedStyle(
    "AutomaticValue",
    font=Font(name="Calibri"),
    fill=PatternFill("solid", fgColor="d5e6e2"),
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

# The sheet builder reads this value as "no project_id given", so an imported project_id wins.
DEFAULT_PROJECT_ID = "XXXXXXX"

# The bec translator only maps the building element classification code name; its enum sheet is separate.
BEC_TRANSLATOR_FIELD_CODES: tuple[str, ...] = ("building_element_classification_code_name",)

# Integer-looking CSV fields become numbers, so Excel does not flag them as text.

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
    METADATA_STYLE,
    EDITABLE_VALUE_STYLE,
    AUTOMATIC_VALUE_STYLE,
    DISABLED_STYLE,
]


def register_named_styles(writer: pd.ExcelWriter) -> None:
    """Register the shared named styles on the workbook once."""
    for style in ALL_NAMED_STYLES:
        writer.book.add_named_style(style)


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
    project_id: str = DEFAULT_PROJECT_ID,
    findings: list[OpenBDFValidationError] | None = None,
):
    """Save a list of BuildingBillMaterialsSlimRecord to an Excel file."""

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        register_named_styles(writer)
        set_theme_fonts(writer)
        enum_registry = EnumRegistry()
        enum_registry.register(*TEMPLATE_TYPE_DEFINITIONS)

        about_to_xlsx(writer)
        info_to_xlsx(writer, project, info_sheet_name, enum_registry, project_id=project_id, findings=findings)
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
        style_first_rows(writer)


def _style_first_row(sheet: Worksheet, header_style: str | None = None) -> None:
    """Make the header row taller, align its text bottom left and optionally restyle it."""
    sheet.row_dimensions[1].height = FIRST_ROW_HEIGHT
    for cell in sheet[1]:
        cell.alignment = Alignment(horizontal="left", vertical="bottom")
        if header_style is not None:
            cell.style = header_style


def style_first_rows(writer: pd.ExcelWriter, header_style: str | None = None) -> None:
    """Make the header row of every sheet taller, align its text bottom left and optionally restyle it."""
    for sheet in writer.book.worksheets:
        _style_first_row(sheet, header_style if sheet.title != ABOUT_SHEET_NAME else None)


def _info_value(
    project: ProjectRecord | None,
    field_code: str,
    project_id: str,
    findings: list[OpenBDFValidationError] | None,
    sheet_name: str,
) -> Any:
    """Return the Value cell of a General Information field and report a replaced project_id."""
    if field_code != "project_id":
        value = getattr(project, field_code) if project else ""
        return value.display_name if isinstance(value, OpenBDFEnum) else value

    imported = getattr(project, "project_id", None) if project else None
    if project_id == DEFAULT_PROJECT_ID:
        return imported or DEFAULT_PROJECT_ID

    if findings is not None and imported is not None and imported != project_id:
        findings.append(
            AutomaticFieldSupplied(
                "Field project_id was in the original data; the given project_id replaced it",
                source=sheet_name,
            )
        )
    return project_id


def info_to_xlsx(
    writer: pd.ExcelWriter,
    project: ProjectRecord | None,
    sheet_name: str,
    enum_registry: EnumRegistry,
    project_id: str = DEFAULT_PROJECT_ID,
    findings: list[OpenBDFValidationError] | None = None,
):
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
        c.style = METADATA_STYLE.name

        units = extra.get("units", "")
        u = info_sheet.cell(row=cell_row, column=8, value=units)
        u.style = METADATA_STYLE.name

        r = info_sheet.cell(row=cell_row, column=9, value=requirements.display_name)
        r.style = REQUIREMENT_STYLES[requirements].name

        reference = extra.get("reference")
        ref = info_sheet.cell(row=cell_row, column=11, value=reference or "")
        ref.style = METADATA_STYLE.name

        v = info_sheet.cell(
            row=cell_row, column=10, value=_info_value(project, field_code, project_id, findings, sheet_name)
        )
        v.style = AUTOMATIC_VALUE_STYLE.name if requirements is Requirement.AUTOMATIC else EDITABLE_VALUE_STYLE.name

        dv = xlsx_validation_from_type(data_type, is_optional, metadata, enum_registry)  # type: ignore[arg-type]
        if dv:
            dv.add(v)
            info_sheet.add_data_validation(dv)

        if requirements in MARKED_REQUIREMENTS:
            for c in header_cells:
                c.style = REQUIREMENT_STYLES[requirements].name

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
    automatic_array = style_arrays[AUTOMATIC_VALUE_STYLE.name]
    disabled_array = style_arrays[DISABLED_STYLE.name]
    automatic_columns: set[int] = set()
    enum_columns: dict[int, type[OpenBDFEnum]] = {}

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
        if requirements in MARKED_REQUIREMENTS:
            desc.style = REQUIREMENT_STYLES[requirements].name
        desc.alignment = Alignment(wrap_text=True, vertical="top")

        sheet.cell(row=4, column=cell_column, value=human_readable_type(data_type))

        constraints = extra.get("constraint") or human_readable_constraints(metadata)
        c = sheet.cell(row=5, column=cell_column, value=constraints)
        c.style = METADATA_STYLE.name

        unit = extra.get("units", "")
        u = sheet.cell(row=6, column=cell_column, value=unit)
        u.style = METADATA_STYLE.name

        r = sheet.cell(row=7, column=cell_column, value=requirements.display_name)
        r.style = REQUIREMENT_STYLES[requirements].name
        if requirements is Requirement.AUTOMATIC:
            automatic_columns.add(cell_column)
        if isinstance(data_type, type) and issubclass(data_type, OpenBDFEnum):
            enum_columns[cell_column] = data_type

        reference = extra.get(reference_attribute)
        ref = sheet.cell(row=8, column=cell_column, value=reference or "")
        ref.style = (
            REQUIREMENT_STYLES[requirements].name if requirements in MARKED_REQUIREMENTS else METADATA_STYLE.name
        )

        dv = xlsx_validation_from_type(data_type, is_optional, metadata, enum_registry)  # type: ignore[arg-type]
        if dv:
            dv.add(
                f"{column_letter}9:{column_letter}1048576"
            )  # Apply validation to the whole column starting from the first data row
            sheet.add_data_validation(dv)

        sheet.column_dimensions[column_letter].width = max(
            15, len(attribute_name) + 5
        )  # Set column width based on header length

    for row_idx, label in enumerate(
        ["Attribute", "Field Code", "Description", "Data Type", "Constraint", "Units", "Requirements", ""], start=1
    ):
        header = sheet.cell(row=row_idx, column=1, value=label or REFERENCE_LABELS[reference_attribute])
        header.style = ATTRIBUTES_NAME_STYLE.name

    last_col = len(df.columns) + 1
    start_data_row = 9
    end_data_row = start_data_row + max(len(df) - 1, min_rows)

    rows = df.itertuples(index=False, name=None)
    for row_idx in range(start_data_row, end_data_row + 1):
        sheet.cell(row=row_idx, column=1)._style = copy(disabled_array)
        row_values = next(rows, None)
        for col_idx in range(2, last_col + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            cell._style = copy(automatic_array if col_idx in automatic_columns else editable_array)
            if row_values is not None:
                value = row_values[col_idx - 2]
                if isinstance(value, np.generic):
                    value = value.item()
                if value is None or value != value:  # None and NaN are written as empty strings
                    value = ""
                if col_idx in enum_columns:
                    member = enum_columns[col_idx].find_value(value)
                    if member is not None:
                        value = member.display_name
                cell.value = value

    sheet.row_dimensions[2].height = 15
    sheet.column_dimensions["A"].width = 20


def save_translator(xlsx_path: str | Path | BinaryIO):
    """Save a template Excel file for the attribute translator."""
    _save_skeleton(translator_skeleton(), xlsx_path)


def translator_skeleton(sheet_set: str = "full") -> BytesIO:
    """Build a styled translator workbook without translated values and return its memory buffer."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        register_named_styles(writer)
        set_theme_fonts(writer)
        about_to_xlsx(writer)
        _translator_sheet_set(writer, sheet_set)
        style_first_rows(writer, ATTRIBUTES_NAME_STYLE.name)
    buffer.seek(0)
    return buffer


def save_bec_translator(xlsx_path: str | Path | BinaryIO):
    """Save a template Excel file for the building element classification translator."""
    _save_skeleton(translator_skeleton("bec"), xlsx_path)


def save_bmc_translator(xlsx_path: str | Path | BinaryIO):
    """Save a template Excel file for the material classification translator."""
    _save_skeleton(translator_skeleton("bmc"), xlsx_path)


def _save_skeleton(skeleton: BytesIO, xlsx_path: str | Path | BinaryIO) -> None:
    """Write a skeleton buffer to a path or to a binary stream."""
    data = skeleton.getvalue()
    if isinstance(xlsx_path, (str, Path)):
        Path(xlsx_path).write_bytes(data)
    else:
        xlsx_path.seek(0)
        xlsx_path.truncate()
        xlsx_path.write(data)


def _translator_sheet_set(writer: pd.ExcelWriter, sheet_set: str) -> None:
    """Add the sheets of a translator template set, in template order, after the About sheet."""
    if sheet_set == "bec":
        make_translator_openbdf_pydantic(
            writer,
            COMMON_CATEGORY_PROPERTIES["project"]["name"],
            _fields_of(ProjectRecordBase.model_fields, BEC_TRANSLATOR_FIELD_CODES),
        )
        make_translator_openbdfenum(
            writer, OpenBDFBuildingElementClassification.__name__, OpenBDFBuildingElementClassification
        )
        return

    if sheet_set == "bmc":
        make_translator_openbdfenum(writer, OpenBDFMaterialClassification.__name__, OpenBDFMaterialClassification)
        return

    if sheet_set != "full":
        raise ValueError(f"Unknown translator template set: {sheet_set!r}")

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
    make_translator_floor_level(writer, FLOOR_LEVEL_CATEGORY)


def _fields_of(model: dict[str, FieldInfo], field_codes: Collection[str]) -> dict[str, FieldInfo]:
    """The metadata of the given field codes, in model order."""
    return {field_code: field for field_code, field in model.items() if field_code in field_codes}


def csv_dir_from_build(build: Callable[[BytesIO], None], directory: Path) -> list[Path]:
    """Run a workbook builder into memory and write one CSV file per sheet of its workbook."""
    buffer = BytesIO()
    build(buffer)
    buffer.seek(0)
    return workbook_sheets_to_csv_dir(load_workbook(buffer), directory, exclude=(ABOUT_SHEET_NAME,))


def workbook_from_csv_dir(directory: Path) -> BytesIO:
    """Build a translator workbook from a directory of sheet CSV files; the About sheet comes from about.md."""
    workbook = load_workbook(translator_skeleton())
    rows_by_sheet = {
        sheet_name: rows for sheet_name, rows in csv_dir_rows(directory).items() if sheet_name != ABOUT_SHEET_NAME
    }

    sheets: list[Worksheet] = []
    for sheet_name, rows in rows_by_sheet.items():
        width = max((len(row) for row in rows), default=0)
        if sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            row_styles = [sheet.cell(row=2, column=column).style for column in range(1, width + 1)]
            if sheet.max_row > 1:
                sheet.delete_rows(2, sheet.max_row - 1)
        else:
            sheet = workbook.create_sheet(sheet_name)
            row_styles = None
            _style_first_row(sheet, ATTRIBUTES_NAME_STYLE.name)
        _write_csv_header(sheet, rows[0] if rows else [])
        _write_csv_rows(sheet, rows[1:], row_styles)
        sheets.append(sheet)

    for sheet_name in [sheet.title for sheet in workbook.worksheets if sheet.title not in rows_by_sheet]:
        if sheet_name != ABOUT_SHEET_NAME:
            workbook.remove(workbook[sheet_name])

    workbook._sheets = [workbook[ABOUT_SHEET_NAME], *sheets]

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer


def _write_csv_header(sheet: Worksheet, header: list[str]) -> None:
    """Write the header row of a sheet, clear the header cells the template has in excess, set a column width."""
    for column in range(len(header) + 1, sheet.max_column + 1):
        sheet.cell(row=1, column=column).value = None
    for column, value in enumerate(header, start=1):
        sheet.cell(row=1, column=column).value = value or None
        sheet.column_dimensions[get_column_letter(column)].width = max(15, len(value) + 5)


def _write_csv_rows(sheet: Worksheet, rows: list[list[str]], row_styles: list[str] | None) -> None:
    """Write CSV rows from row 2, repeating the style of row 2 on every written cell."""
    for row_index, row in enumerate(rows, start=2):
        for column_index, value in enumerate(row, start=1):
            style = (
                row_styles[column_index - 1]
                if row_styles is not None and column_index <= len(row_styles)
                else EDITABLE_VALUE_STYLE.name
            )
            cell = sheet.cell(row=row_index, column=column_index)
            cell.value = value or None
            cell.style = style


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

    # The contributor fills everything but the OpenBDF side of the mapping.
    for cell_row in range(2, len(models) + 2):
        for column in range(1, 11):
            if column != 2:
                info_sheet.cell(row=cell_row, column=column).style = EDITABLE_VALUE_STYLE.name

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

        code_cell = info_sheet.cell(row=cell_row, column=1, value="")
        code_cell.style = EDITABLE_VALUE_STYLE.name

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


def make_translator_floor_level(writer: pd.ExcelWriter, sheet_name: str):
    """The floor level sheet maps a storey label to an OpenBDF floor number."""
    if sheet_name in writer.book.sheetnames:
        return

    info_sheet = writer.book.create_sheet(sheet_name)

    info_sheet.cell(row=1, column=1, value="Value in your format")
    info_sheet.cell(row=1, column=2, value="OpenBDF floor level")
    info_sheet.cell(row=1, column=3, value="Leave the floor level empty to take the number carried by the label")

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 80


EXCEL_SHEET_TITLE_MAX_LENGTH = 31


def _sheet_title(workbook: Workbook, sheet_name: str) -> str | None:
    """The title of a new sheet, cut to the Excel limit, or None when the workbook holds that title already.

    Sheets are keyed by the cut title, so two enums that share their first 31 characters collapse into one sheet.
    """
    title = sheet_name[:EXCEL_SHEET_TITLE_MAX_LENGTH]
    return None if title in workbook.sheetnames else title


def make_translator_openbdfenum(writer: pd.ExcelWriter, sheet_name: str, enum: type[OpenBDFEnum]):
    title = _sheet_title(writer.book, sheet_name)
    if title is None:
        return

    info_sheet = writer.book.create_sheet(title)

    info_sheet.cell(row=1, column=1, value="Value in your format")
    info_sheet.cell(row=1, column=2, value="OpenBDF enum value")
    info_sheet.cell(row=1, column=3, value="OpenBDF value display name")
    info_sheet.cell(row=1, column=4, value="OpenBDF value description (if any)")
    info_sheet.cell(row=1, column=5, value="OpenBDF value parent category (if applicable)")

    for cell_row, item in enumerate(enum, start=2):  # xlsx are 1-indexed (ewww)
        display_name = getattr(item, "display_name", None)
        description = getattr(item, "description", None)
        parent_category = getattr(item, "parent_category", None)

        value_cell = info_sheet.cell(row=cell_row, column=1, value="")
        value_cell.style = EDITABLE_VALUE_STYLE.name

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
