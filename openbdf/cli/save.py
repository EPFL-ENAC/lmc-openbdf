from pathlib import Path
from typing import TypeVar

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from pydantic.fields import FieldInfo
from sqlmodel import SQLModel

from openbdf.lib.converters.dataframe import wide_to_dataframe
from openbdf.lib.converters.enums_registry import EnumRegistry
from openbdf.lib.converters.translators import COMMON_CATEGORY_NAMES, SHEETS_PROPERTIES_HEADERS
from openbdf.lib.types.annotations import unwrap_optional
from openbdf.lib.types.human_readable import human_readable_constraints, human_readable_type
from openbdf.lib.types.xlsx import xlsx_validation_from_type
from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.enums.openbdf_enum import OpenBDFEnum
from openbdf.model.general_info import ProjectRecordBase
from openbdf.model.lca_results_full import LCAResultsFullBase
from openbdf.model.tables import ProjectRecord

thin_side = Side(border_style="thin", color="AAAAAA")

ATTRIBUTES_NAME_STYLE = NamedStyle(
    "AttributeName", font=Font(bold=True, color="FFFFFF"), fill=PatternFill("solid", fgColor="2b5b47")
)
INFO_STYLE = NamedStyle("Info", font=Font(italic=True))
FIELD_CODE_STYLE = NamedStyle("FieldCode", font=Font(color="FFFFFF"), fill=PatternFill("solid", fgColor="010101"))
REQUIRED_STYLE = NamedStyle("Required", fill=PatternFill("solid", fgColor="a3d3bd"))
RECOMMENDED_STYLE = NamedStyle("Recommended", fill=PatternFill("solid", fgColor="a9d2f6"))
OPTIONAL_STYLE = NamedStyle("Optional", fill=PatternFill("solid", fgColor="d8e6e2"))
ROW_HEADER_STYLE = NamedStyle("RowHeader", font=Font(bold=True), alignment=Alignment(vertical="top"))
EDITABLE_VALUE_STYLE = NamedStyle(
    "EditableValue",
    fill=PatternFill("solid", fgColor="feffb3"),
    border=Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side),
    protection=Protection(locked=False),
)
DISABLED_STYLE = NamedStyle(
    "Disabled",
    fill=PatternFill("solid", fgColor="d3d3d3"),
)

ModelT = TypeVar("ModelT", bound=SQLModel)
ModelT2 = TypeVar("ModelT2", bound=SQLModel)


def get_field_extra(field: FieldInfo) -> dict:
    """Safely extracts json_schema_extra if it is a dictionary."""
    extra = field.json_schema_extra
    return extra if isinstance(extra, dict) else {}


def save_openbdf_to_xlsx(
    xlsx_path: str | Path,
    project: ProjectRecord | None,
    info_sheet_name: str = "General Info",
    bom_sheet_name: str = "Building Bill of Materials",
    results_sheet_name: str = "LCA Results",
):
    """Save a list of BuildingBillMaterialsSlimRecord to an Excel file."""

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        enum_registry = EnumRegistry()

        info_to_xlsx(writer, project, info_sheet_name, enum_registry)
        wide_to_xlsx(
            writer,
            project.bill_of_materials if project else None,
            BuildingBillMaterialsSlimRecordBase,
            bom_sheet_name,
            enum_registry,
        )
        wide_to_xlsx(
            writer,
            [record.lca_results_full_record for record in project.bill_of_materials if record.lca_results_full_record]
            if project
            else None,
            LCAResultsFullBase,
            results_sheet_name,
            enum_registry,
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
        requirements = extra.get("requirements", "Optional" if is_optional else "Required")

        header_cells = []

        g = info_sheet.cell(row=cell_row, column=1, value=extra.get("group", field_code))
        header_cells.append(g)

        sg = info_sheet.cell(row=cell_row, column=2, value=extra.get("sub_group", field_code))
        header_cells.append(sg)

        an = info_sheet.cell(row=cell_row, column=3, value=extra.get("attribute_name", field_code))
        header_cells.append(an)

        fc = info_sheet.cell(row=cell_row, column=4, value=field_code)
        header_cells.append(fc)

        desc = info_sheet.cell(
            row=cell_row,
            column=5,
            value=metadata.description if metadata and metadata.description else field_code,
        )
        header_cells.append(desc)

        dt = info_sheet.cell(row=cell_row, column=6, value=human_readable_type(data_type))
        dt.style = INFO_STYLE

        constraints = human_readable_constraints(metadata)
        c = info_sheet.cell(row=cell_row, column=7, value=constraints)
        if constraints:
            c.style = INFO_STYLE
        else:
            c.style = DISABLED_STYLE

        units = extra.get("units", "")
        u = info_sheet.cell(row=cell_row, column=8, value=units)
        if units:
            u.style = INFO_STYLE
        else:
            u.style = DISABLED_STYLE

        r = info_sheet.cell(row=cell_row, column=9, value=requirements)
        if requirements == "Required":
            r.style = REQUIRED_STYLE
        elif requirements == "Recommended":
            r.style = RECOMMENDED_STYLE
        else:
            r.style = OPTIONAL_STYLE

        v = info_sheet.cell(row=cell_row, column=10, value=getattr(project, field_code) if project else "")
        v.style = EDITABLE_VALUE_STYLE

        dv = xlsx_validation_from_type(data_type, is_optional, metadata, enum_registry)  # type: ignore[arg-type]
        if dv:
            dv.add(v)
            info_sheet.add_data_validation(dv)

        if requirements == "Required":
            for c in header_cells:
                c.style = REQUIRED_STYLE

    a = info_sheet.cell(row=1, column=1, value="Group")
    a.style = ATTRIBUTES_NAME_STYLE
    d = info_sheet.cell(row=1, column=2, value="Sub-group")
    d.style = ATTRIBUTES_NAME_STYLE
    dt = info_sheet.cell(row=1, column=3, value="Attribute Name")
    dt.style = ATTRIBUTES_NAME_STYLE
    c = info_sheet.cell(row=1, column=4, value="Field Code")
    c.style = ATTRIBUTES_NAME_STYLE
    u = info_sheet.cell(row=1, column=5, value="Description")
    u.style = ATTRIBUTES_NAME_STYLE
    r = info_sheet.cell(row=1, column=6, value="Datatype")
    r.style = ATTRIBUTES_NAME_STYLE
    ui = info_sheet.cell(row=1, column=7, value="Constraint")
    ui.style = ATTRIBUTES_NAME_STYLE
    fc = info_sheet.cell(row=1, column=8, value="Units")
    fc.style = ATTRIBUTES_NAME_STYLE
    fc = info_sheet.cell(row=1, column=9, value="Requirements")
    fc.style = ATTRIBUTES_NAME_STYLE
    fc = info_sheet.cell(row=1, column=10, value="Value")
    fc.style = ATTRIBUTES_NAME_STYLE

    info_sheet.column_dimensions["A"].width = 10
    info_sheet.column_dimensions["B"].width = 20
    info_sheet.column_dimensions["C"].width = 30
    info_sheet.column_dimensions["D"].width = 30
    info_sheet.column_dimensions["E"].width = 40
    info_sheet.column_dimensions["F"].width = 30
    info_sheet.column_dimensions["G"].width = 25
    info_sheet.column_dimensions["H"].width = 15
    info_sheet.column_dimensions["I"].width = 15
    info_sheet.column_dimensions["J"].width = 25


def wide_to_xlsx(
    writer: pd.ExcelWriter,
    records: list[ModelT] | None,
    model_cls: type[ModelT2],
    sheet_name: str,
    enum_registry: EnumRegistry,
    min_rows: int = 100,
):
    if records is None:
        records = []

    df = wide_to_dataframe(records, model_cls)  # type: ignore[misc]
    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startcol=1, startrow=8)

    sheet = writer.sheets[sheet_name]
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
        requirements = extra.get("requirements", "Optional" if is_optional else "Required")

        attribute_name = extra.get("attribute_name", field_code)
        an = sheet.cell(row=1, column=cell_column, value=attribute_name)
        an.style = ATTRIBUTES_NAME_STYLE

        desc = sheet.cell(
            row=2,
            column=cell_column,
            value=metadata.description if metadata and metadata.description else field_code,
        )
        if not is_optional:
            desc.style = REQUIRED_STYLE
        desc.alignment = Alignment(wrap_text=True, vertical="top")

        sheet.cell(row=3, column=cell_column, value=human_readable_type(data_type))

        constraints = human_readable_constraints(metadata)
        c = sheet.cell(row=4, column=cell_column, value=constraints)
        if constraints:
            c.style = INFO_STYLE
        else:
            c.style = DISABLED_STYLE

        unit = extra.get("units", "")
        u = sheet.cell(row=5, column=cell_column, value=unit)
        if unit:
            u.style = INFO_STYLE
        else:
            u.style = DISABLED_STYLE

        r = sheet.cell(row=6, column=cell_column, value=requirements)
        if requirements == "Required":
            r.style = REQUIRED_STYLE
        elif requirements == "Recommended":
            r.style = RECOMMENDED_STYLE
        else:
            r.style = OPTIONAL_STYLE

        fc = sheet.cell(row=8, column=cell_column, value=field_code)
        fc.style = FIELD_CODE_STYLE

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
    a.style = ROW_HEADER_STYLE
    d = sheet.cell(row=2, column=1, value="Description")
    d.style = ROW_HEADER_STYLE
    dt = sheet.cell(row=3, column=1, value="Data Type")
    dt.style = ROW_HEADER_STYLE
    c = sheet.cell(row=4, column=1, value="Constraint")
    c.style = ROW_HEADER_STYLE
    u = sheet.cell(row=5, column=1, value="Units")
    u.style = ROW_HEADER_STYLE
    r = sheet.cell(row=6, column=1, value="Requirements")
    r.style = ROW_HEADER_STYLE
    ui = sheet.cell(row=7, column=1, value="User Instructions")
    ui.style = ROW_HEADER_STYLE
    fc = sheet.cell(row=8, column=1, value="Field Code")
    fc.style = ROW_HEADER_STYLE

    last_col = len(df.columns) + 1
    start_data_row = 9
    end_data_row = start_data_row + max(len(df) - 1, min_rows)
    for row_idx in range(start_data_row, end_data_row + 1):
        sheet.cell(row=row_idx, column=1).style = DISABLED_STYLE
        for col_idx in range(2, last_col + 1):
            sheet.cell(row=row_idx, column=col_idx).style = EDITABLE_VALUE_STYLE

    sheet.row_dimensions[2].height = 15
    sheet.column_dimensions["A"].width = 20


def save_translator(
    xlsx_path: str | Path,
):
    """Save a template Excel file for the attribute translator."""
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        make_translations_library_template_xlsx(writer, "Translations Library")
        make_translator_openbdf_pydantic(writer, COMMON_CATEGORY_NAMES["project"], ProjectRecordBase.model_fields)
        make_translator_openbdf_pydantic(
            writer, COMMON_CATEGORY_NAMES["bom"], BuildingBillMaterialsSlimRecordBase.model_fields
        )
        export_all_enums_in_model_to_translator(writer, ProjectRecordBase.model_fields)
        export_all_enums_in_model_to_translator(writer, BuildingBillMaterialsSlimRecordBase.model_fields)


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

    models = [
        {
            "name": COMMON_CATEGORY_NAMES["project"],
            "orientation": "vertical",
            "header_row": 0,
        },
        {
            "name": COMMON_CATEGORY_NAMES["bom"],
            "orientation": "horizontal",
            "header_row": 0,
        },
    ]

    for cell_row, model in enumerate(models, start=2):  # xlsx are 1-indexed (ewww)
        info_sheet.cell(row=cell_row, column=2, value=model["name"])
        info_sheet.cell(row=cell_row, column=3, value=model["orientation"])
        info_sheet.cell(row=cell_row, column=4, value=model["header_row"])

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

    for cell_row, field_code in enumerate(model, start=2):  # xlsx are 1-indexed (ewww)
        metadata = model.get(field_code)
        if not metadata:
            continue

        extra = get_field_extra(metadata)
        data_type, is_optional = unwrap_optional(metadata.annotation)
        requirements = extra.get("requirements", "Optional" if is_optional else "Required")

        fc = info_sheet.cell(row=cell_row, column=2, value=field_code)
        fc.style = FIELD_CODE_STYLE

        an = info_sheet.cell(row=cell_row, column=3, value=extra.get("attribute_name", field_code))
        an.style = ATTRIBUTES_NAME_STYLE

        r = info_sheet.cell(row=cell_row, column=4, value=human_readable_type(data_type))
        r.style = INFO_STYLE

        req = info_sheet.cell(row=cell_row, column=5, value=requirements)
        if requirements == "Required":
            req.style = REQUIRED_STYLE
        elif requirements == "Recommended":
            req.style = RECOMMENDED_STYLE
        else:
            req.style = OPTIONAL_STYLE

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 20
    info_sheet.column_dimensions["D"].width = 40
    info_sheet.column_dimensions["E"].width = 40


def export_all_enums_in_model_to_translator(writer: pd.ExcelWriter, model: dict[str, FieldInfo]):
    for field in model.values():
        annotation = field.annotation
        data_type, _ = unwrap_optional(annotation)
        if isinstance(data_type, type) and issubclass(data_type, OpenBDFEnum):
            make_translator_openbdfenum(writer, data_type.__name__, data_type)


def make_translator_openbdfenum(writer: pd.ExcelWriter, sheet_name: str, enum: type[OpenBDFEnum]):
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
        fc.style = FIELD_CODE_STYLE

        an = info_sheet.cell(row=cell_row, column=3, value=str(display_name) if display_name else str(item.value))
        an.style = ATTRIBUTES_NAME_STYLE

        d = info_sheet.cell(row=cell_row, column=4, value=str(description) if description else "")

        pc = info_sheet.cell(row=cell_row, column=5, value=str(parent_category[0]) if parent_category else "")

    info_sheet.column_dimensions["A"].width = 30
    info_sheet.column_dimensions["B"].width = 30
    info_sheet.column_dimensions["C"].width = 40
    info_sheet.column_dimensions["D"].width = 140
    info_sheet.column_dimensions["E"].width = 40
