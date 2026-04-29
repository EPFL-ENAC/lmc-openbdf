from enum import Enum
from typing import Any

import typer
from pydantic import BaseModel, Field

from ..lib.types import get_display_type, unwrap_optional

# --- Data Models ---


class EnumValue(BaseModel):
    value: str
    display_name: str | None = None
    description: str | None = None


class FieldAnalysis(BaseModel):
    field_name: str
    is_optional: bool
    data_type: str
    attribute_name: str | None = None
    group_info: str | None = None
    description: str | None = None
    requirements: str | None = None
    constraint: str | None = None
    units: str | None = None
    enum_values: list[EnumValue] = Field(default_factory=list)


class ModelAnalysis(BaseModel):
    model_name: str
    fields: list[FieldAnalysis]


# --- Logic / Extraction ---


def analyze_model(model_name: str, field_names: list[str] | None = None) -> ModelAnalysis:
    """Extracts metadata from the SQLModel and returns a structured object."""
    from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
    from openbdf.model.enums.openbdf_enum import OpenBDFEnum
    from openbdf.model.general_info import ProjectRecordBase  # Import inside to avoid circular deps
    from openbdf.model.tables import BuildingBillMaterialsSlimRecord, ProjectRecord

    registry = {
        "ProjectRecordBase": ProjectRecordBase,
        "ProjectRecord": ProjectRecord,
        "BuildingBillMaterialsSlimRecordBase": BuildingBillMaterialsSlimRecordBase,
        "BuildingBillMaterialsSlimRecord": BuildingBillMaterialsSlimRecord,
    }
    model_class = registry.get(model_name)

    if not model_class:
        raise ValueError(f"Model '{model_name}' not found.")

    if field_names is None:
        field_names = list(model_class.model_fields.keys())

    analysis = ModelAnalysis(model_name=model_name, fields=[])

    for f_name in field_names:
        field_info = model_class.model_fields.get(f_name)
        if not field_info:
            continue

        raw_type = field_info.annotation
        data_type, is_optional = unwrap_optional(raw_type)
        display_type = get_display_type(data_type)
        extra = field_info.json_schema_extra
        metadata: dict[str, Any] = {}
        if isinstance(extra, dict):
            metadata = extra

        # Extract Enum values
        enums = []
        if isinstance(data_type, type) and issubclass(data_type, Enum):
            for item in data_type:
                display_name = getattr(item, "display_name", None)
                description = getattr(item, "description", None)

                enums.append(
                    EnumValue(
                        value=str(item.value),
                        display_name=str(display_name) if display_name else None,
                        description=str(description) if description else None,
                    )
                )

        field_data = FieldAnalysis(
            field_name=f_name,
            is_optional=is_optional,
            data_type=display_type,
            attribute_name=metadata.get("attribute_name"),
            group_info=f"{metadata.get('group')} > {metadata.get('sub_group')}" if metadata.get("group") else None,
            description=metadata.get("description") or field_info.description,
            requirements=metadata.get("requirements"),
            constraint=metadata.get("constraint"),
            units=metadata.get("units"),
            enum_values=enums,
        )
        analysis.fields.append(field_data)

    return analysis


# --- Formatter: Console ---


def print_to_console(analysis: ModelAnalysis):
    """Prints the analysis using Typer styling."""
    typer.secho(f"\nMODEL: {analysis.model_name}", fg=typer.colors.MAGENTA, bold=True, underline=True)

    for field in analysis.fields:
        opt_str = "(Optional)" if field.is_optional else ""
        typer.secho(f"\n--- Field: {field.field_name} {opt_str} ---", fg=typer.colors.CYAN, bold=True)

        info = {
            "Attribute Name": field.attribute_name,
            "Group": field.group_info,
            "Description": field.description,
            "Requirements": field.requirements,
            "Constraint": field.constraint,
            "Units": field.units,
            "Data Type": field.data_type,
        }

        for label, value in info.items():
            if value and value != "none":
                typer.echo(f"{typer.style(label + ':', fg=typer.colors.YELLOW)} {value}")

        if field.enum_values:
            typer.secho("\nPossible Values:", fg=typer.colors.GREEN, underline=True)
            for ev in field.enum_values:
                if ev.display_name:
                    desc = f" - {ev.description}" if ev.description else ""
                    typer.echo(f"  • {typer.style(ev.value, bold=True)} ({ev.display_name}){desc}")
                else:
                    typer.echo(f"  • {ev.value}")


# --- Formatter: Markdown ---


def generate_markdown(analysis: ModelAnalysis) -> str:
    """Returns a string formatted in Markdown."""
    lines = [f"# Model Analysis: {analysis.model_name}", ""]

    for field in analysis.fields:
        opt_suffix = " *(Optional)*" if field.is_optional else ""
        lines.append(f"## Field: `{field.field_name}`{opt_suffix}")

        if field.description:
            lines.append(f"**Description:** {field.description}")

        lines.append("\n| Property | Value |")
        lines.append("| :--- | :--- |")
        lines.append(f"| Data Type | `{field.data_type}` |")

        if field.attribute_name:
            lines.append(f"| Attribute | {field.attribute_name} |")
        if field.group_info:
            lines.append(f"| Group | {field.group_info} |")
        if field.requirements:
            lines.append(f"| Requirements | {field.requirements} |")
        if field.constraint:
            lines.append(f"| Constraint | {field.constraint} |")
        if field.units:
            lines.append(f"| Units | {field.units} |")

        if field.enum_values:
            lines.append("\n### Possible Values")
            for ev in field.enum_values:
                display = f" ({ev.display_name})" if ev.display_name else ""
                desc = f" - {ev.description}" if ev.description else ""
                lines.append(f"- **`{ev.value}`**{display}{desc}")

        lines.append("\n---")

    return "\n".join(lines)
