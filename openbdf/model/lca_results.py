from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from openbdf.model.enums.lca import LCAStageOrModule


@dataclass(frozen=True)
class LCAResultIndicator:
    """
    Definition of one LCA impact indicator.

    The generator uses this data to build the indicator fields of the tall and
    wide LCA result models.
    """

    code: str
    attribute_name: str
    units: str
    requirements: str
    required_in_wide: bool = False


# Every LCA stage or module present in the wide model, as (enum, suffix) pairs.
# The suffix becomes the field name suffix, the enum value becomes the display label.
STAGES: tuple[tuple[LCAStageOrModule, str], ...] = (
    (LCAStageOrModule.A1_A3, "a1_a3"),
    (LCAStageOrModule.A1, "a1"),
    (LCAStageOrModule.A2, "a2"),
    (LCAStageOrModule.A3, "a3"),
    (LCAStageOrModule.A4, "a4"),
    (LCAStageOrModule.A5, "a5"),
    (LCAStageOrModule.B1, "b1"),
    (LCAStageOrModule.B2, "b2"),
    (LCAStageOrModule.B3, "b3"),
    (LCAStageOrModule.B4, "b4"),
    (LCAStageOrModule.B5, "b5"),
    (LCAStageOrModule.B6, "b6"),
    (LCAStageOrModule.C1, "c1"),
    (LCAStageOrModule.C2, "c2"),
    (LCAStageOrModule.C3, "c3"),
    (LCAStageOrModule.C4, "c4"),
    (LCAStageOrModule.D, "d"),
    (LCAStageOrModule.D1, "d1"),
    (LCAStageOrModule.D2, "d2"),
)

# Every LCA impact indicator present in the tall and wide models.
# `gwp_total` is special: its wide total field keeps the bare code name (`gwp_total`) instead of `gwp_total_total`,
# its `a1_a3` stage field and its total field are required, and its total attribute removes the trailing ` - Total` suffix.
INDICATORS: tuple[LCAResultIndicator, ...] = (
    LCAResultIndicator(
        code="gwp_total",
        attribute_name="Global Warming Potential - Total",
        units="kg CO₂ eq",
        requirements="Recommended",
        required_in_wide=True,
    ),
    LCAResultIndicator(
        code="gwp_f",
        attribute_name="Global Warming Potential - Fossil",
        units="kg CO₂ eq",
        requirements="Recommended",
    ),
    LCAResultIndicator(
        code="gwp_b",
        attribute_name="Global Warming Potential - Biogenic",
        units="kg CO₂ eq",
        requirements="Recommended",
    ),
    LCAResultIndicator(
        code="gwp_luc",
        attribute_name="Global Warming Potential - Land Use and Land Use Change",
        units="kg CO₂ eq",
        requirements="Recommended",
    ),
    LCAResultIndicator(
        code="odp",
        attribute_name="Ozone Depletion Potential",
        units="kg R11 eq / kg CFC-11 eq.",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="ap",
        attribute_name="Acidification Potential",
        units="kg SO₂ eq.",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="ep",
        attribute_name="Eutrophication Potential",
        units="kg N eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="ep_af",
        attribute_name="Eutrophication Potential - Aquatic Freshwater",
        units="kg PO4 eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="ep_am",
        attribute_name="Eutrophication Potential - Aquatic Marine",
        units="kg N eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="ep_t",
        attribute_name="Eutrophication Potential - Terrestrial",
        units="mol Ne eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="pocp",
        attribute_name="Photochemical Ozone Creation Potential",
        units="kg C2H4 eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="sfp",
        attribute_name="Smog Forming Potential",
        units="kg O3 eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="pofp",
        attribute_name="Photochemical Ozone Formation Potential",
        units="kg NMVOC eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="adpmm",
        attribute_name="Abiotic Depletion Potential (Minerals and Metals)",
        units="kg Sb eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="adpf",
        attribute_name="Abiotic Depletion Potential (Fossil Fuels)",
        units="MJ",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="wdp",
        attribute_name="Water Depletion Potential",
        units="m3 world eq",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="pere",
        attribute_name="Primary Energy Renewable (Energy resources)",
        units="MJ",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="penre",
        attribute_name="Primary Energy Non-Renewable (Energy resources)",
        units="MJ",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="pert",
        attribute_name="Primary Energy Renewable Total",
        units="MJ",
        requirements="Optional",
    ),
    LCAResultIndicator(
        code="penrt",
        attribute_name="Primary Energy Non-Renewable Total",
        units="MJ",
        requirements="Optional",
    ),
)


# ---------------------------------------------------------------------------
# Code generation for the tall and wide LCA result model classes.
# ---------------------------------------------------------------------------

_HEADER = (
    "# This file is generated by scripts/generate_lca_results_classes.py.\n"
    "# Do not edit by hand. Regenerate with: make generate-lca-results-classes.\n\n"
)

_TRAILING_TOTAL_SUFFIX = " - Total"


def _q(value: str) -> str:
    """Wrap a string in double quotes for source emission."""
    return '"' + value.replace('"', '\\"') + '"'


def _total_code(code: str) -> str:
    """Field code of the wide total field for an indicator."""
    if code.endswith("_total"):
        return code
    return f"{code}_total"


def _total_attribute_name(attribute_name: str) -> str:
    """Attribute name of the wide total field for an indicator."""
    base = attribute_name
    if base.endswith(_TRAILING_TOTAL_SUFFIX):
        base = base[: -len(_TRAILING_TOTAL_SUFFIX)]
    return f"Total {base}"


def _render_field(
    *,
    name: str,
    type_: str,
    default: str | None,
    requirements: str | None,
    attribute_name: str,
    field_code: str,
    description: str,
    units: str | None,
    max_length: int | None = None,
) -> str:
    lines: list[str] = [f"    {name}: {type_} = Field("]
    if max_length is not None:
        lines.append(f"        max_length={max_length},")
    if default is not None:
        lines.append(f"        default={default},")
    lines.append(f"        description={_q(description)},")
    lines.append("        schema_extra=openbdf_field_metadata(")
    lines.append(f"            attribute_name={_q(attribute_name)},")
    lines.append(f"            field_code={_q(field_code)},")
    lines.append(f"            description={_q(description)},")
    if units is not None:
        lines.append(f"            units={_q(units)},")
    if requirements is not None:
        lines.append(f"            requirements={_q(requirements)},")
    lines.append("        ),")
    lines.append("    )")
    return "\n".join(lines)


def _material_id_field() -> str:
    return _render_field(
        name="material_id",
        type_="str",
        default=None,
        requirements="Required",
        attribute_name="Material ID",
        field_code="material_id",
        description=(
            "The unique identifier for the material within the project context, referencing the Bill of Materials."
        ),
        units=None,
        max_length=200,
    )


def _lca_service_life_field() -> str:
    return _render_field(
        name="lca_service_life",
        type_="Decimal",
        default=None,
        requirements=None,
        attribute_name="Service life",
        field_code="lca_service_life",
        description="Declared reference service life.",
        units="years",
    )


def _lca_stage_or_module_field() -> str:
    return _render_field(
        name="lca_stage_or_module",
        type_="LCAStageOrModule",
        default=None,
        requirements="Required",
        attribute_name="LCA stage or module",
        field_code="lca_stage_or_module",
        description="Life cycle assessment stage or module for this result row.",
        units=None,
    )


def _tall_indicator_field(indicator: LCAResultIndicator) -> str:
    return _render_field(
        name=indicator.code,
        type_="Optional[Decimal]",
        default="None",
        requirements=indicator.requirements,
        attribute_name=indicator.attribute_name,
        field_code=indicator.code,
        description=f"{indicator.attribute_name}.",
        units=indicator.units,
    )


def _wide_stage_field(
    indicator: LCAResultIndicator,
    stage: LCAStageOrModule,
    suffix: str,
) -> str:
    required = indicator.required_in_wide and suffix == "a1_a3"
    return _render_field(
        name=f"{indicator.code}_{suffix}",
        type_="Decimal" if required else "Optional[Decimal]",
        default=None if required else "None",
        requirements="Required" if required else indicator.requirements,
        attribute_name=f"{indicator.attribute_name} ({stage.value})",
        field_code=f"{indicator.code}_{suffix}",
        description=f"{indicator.attribute_name} for module {stage.value}.",
        units=indicator.units,
    )


def _wide_total_field(indicator: LCAResultIndicator) -> str:
    required = indicator.required_in_wide
    total_name = _total_code(indicator.code)
    total_attribute = _total_attribute_name(indicator.attribute_name)
    return _render_field(
        name=total_name,
        type_="Decimal" if required else "Optional[Decimal]",
        default=None if required else "None",
        requirements="Required" if required else indicator.requirements,
        attribute_name=total_attribute,
        field_code=total_name,
        description=f"{total_attribute}.",
        units=indicator.units,
    )


_TALL_IMPORTS = (
    "from __future__ import annotations\n\n"
    "from decimal import Decimal\n"
    "from typing import Optional\n\n"
    "from sqlmodel import Field, SQLModel\n\n"
    "from openbdf.model.enums.lca import LCAStageOrModule\n\n"
    "from .field_metadata import openbdf_field_metadata\n\n\n"
)

_WIDE_IMPORTS = (
    "from __future__ import annotations\n\n"
    "from decimal import Decimal\n"
    "from typing import Optional\n\n"
    "from sqlmodel import Field, SQLModel\n\n"
    "from .field_metadata import openbdf_field_metadata\n\n\n"
)


def render_tall_module() -> str:
    """Render the source of the LCAResultsTallBase model module."""
    blocks: list[str] = [
        _material_id_field(),
        _lca_service_life_field(),
        _lca_stage_or_module_field(),
    ]
    blocks.extend(_tall_indicator_field(indicator) for indicator in INDICATORS)
    body = "\n\n".join(blocks)
    return _HEADER + _TALL_IMPORTS + "class LCAResultsTallBase(SQLModel):\n" + body + "\n"


def render_wide_module() -> str:
    """Render the source of the LCAResultsWideFullBase model module."""
    blocks: list[str] = [_material_id_field()]
    for indicator in INDICATORS:
        for stage, suffix in STAGES:
            blocks.append(_wide_stage_field(indicator, stage, suffix))
        blocks.append(_wide_total_field(indicator))
    body = "\n\n".join(blocks)
    return _HEADER + _WIDE_IMPORTS + "class LCAResultsWideFullBase(SQLModel):\n" + body + "\n"


# Ordered (file name, render callable) pairs for every generated model module.
GENERATED_MODULES: tuple[tuple[str, Callable], ...] = (
    ("lca_results_full_tall.py", render_tall_module),
    ("lca_results_full_wide.py", render_wide_module),
)


def format_module_source(source: str) -> str:
    """
    Format rendered model source with ruff to match the repository style.

    The generated files are committed and must stay byte-identical to what a
    later ``ruff format`` pre-commit hook would produce. Spawning the real ruff
    binary guarantees this without duplicating its formatting rules here.
    """
    ruff = shutil.which("ruff")
    if ruff is None:
        raise RuntimeError("ruff is not installed. Install the project dev extras and re-run (uv sync --extra dev).")
    with tempfile.TemporaryDirectory() as tmp_dir:
        module_path = Path(tmp_dir) / "generated_module.py"
        module_path.write_text(source, encoding="utf-8")
        subprocess.run(
            [ruff, "format", str(module_path)],
            check=True,
            capture_output=True,
        )
        return module_path.read_text(encoding="utf-8")
