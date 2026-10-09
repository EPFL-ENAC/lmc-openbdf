from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule


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
    description: str | None = None
    required_in_wide: bool = False
    criticality: str = "MAY"
    # Wide-sheet label and description overrides reproduced from the target workbook:
    # some indicators label every stage column (and the total column) with a fixed
    # attribute instead of '<attribute> (<stage>)', and some use a fixed description.
    wide_attribute: str | None = None
    wide_total_attribute: str | None = None
    wide_constant_description: str | None = None
    wide_b7_b8_attribute: str | None = None


# Every LCA stage or module present in the wide model, as (enum, suffix) pairs.
# The suffix becomes the field name suffix, the enum value becomes the display label.
STAGES: tuple[tuple[LCAStageOrModuleOrSubModule, str], ...] = (
    (LCAStageOrModuleOrSubModule.A1_A3, "a1_a3"),
    (LCAStageOrModuleOrSubModule.A1, "a1"),
    (LCAStageOrModuleOrSubModule.A2, "a2"),
    (LCAStageOrModuleOrSubModule.A3, "a3"),
    (LCAStageOrModuleOrSubModule.A4, "a4"),
    (LCAStageOrModuleOrSubModule.A5, "a5"),
    (LCAStageOrModuleOrSubModule.B1, "b1"),
    (LCAStageOrModuleOrSubModule.B2, "b2"),
    (LCAStageOrModuleOrSubModule.B3, "b3"),
    (LCAStageOrModuleOrSubModule.B4, "b4"),
    (LCAStageOrModuleOrSubModule.B5, "b5"),
    (LCAStageOrModuleOrSubModule.B6, "b6"),
    (LCAStageOrModuleOrSubModule.B7, "b7"),
    (LCAStageOrModuleOrSubModule.B8, "b8"),
    (LCAStageOrModuleOrSubModule.C1, "c1"),
    (LCAStageOrModuleOrSubModule.C2, "c2"),
    (LCAStageOrModuleOrSubModule.C3, "c3"),
    (LCAStageOrModuleOrSubModule.C4, "c4"),
    (LCAStageOrModuleOrSubModule.D, "d"),
    (LCAStageOrModuleOrSubModule.D1, "d1"),
    (LCAStageOrModuleOrSubModule.D2, "d2"),
)

OPTIONAL_STAGE_SUFFIXES = (
    "a1",
    "a2",
    "a3",
    "b7",
    "b8",
    # Sub-module columns are always optional.
    "a5_1",
    "a5_2",
    "a5_3",
    "a5_4",
    "b1_1",
    "b1_2",
    "b6_1",
    "b6_2",
    "b6_3",
    "b7_1",
    "b7_2",
    "b7_3",
    "b8_1",
    "b8_2",
    "b8_3",
)

# Stage columns of the gwp_total indicator, which additionally carries the sub-module
# columns of the target workbook, inserted directly after their parent module.
GWP_TOTAL_STAGES: tuple[tuple[LCAStageOrModuleOrSubModule, str], ...] = (
    (LCAStageOrModuleOrSubModule.A1_A3, "a1_a3"),
    (LCAStageOrModuleOrSubModule.A1, "a1"),
    (LCAStageOrModuleOrSubModule.A2, "a2"),
    (LCAStageOrModuleOrSubModule.A3, "a3"),
    (LCAStageOrModuleOrSubModule.A4, "a4"),
    (LCAStageOrModuleOrSubModule.A5, "a5"),
    (LCAStageOrModuleOrSubModule.A5_1, "a5_1"),
    (LCAStageOrModuleOrSubModule.A5_2, "a5_2"),
    (LCAStageOrModuleOrSubModule.A5_3, "a5_3"),
    (LCAStageOrModuleOrSubModule.A5_4, "a5_4"),
    (LCAStageOrModuleOrSubModule.B1, "b1"),
    (LCAStageOrModuleOrSubModule.B1_1, "b1_1"),
    (LCAStageOrModuleOrSubModule.B1_2, "b1_2"),
    (LCAStageOrModuleOrSubModule.B2, "b2"),
    (LCAStageOrModuleOrSubModule.B3, "b3"),
    (LCAStageOrModuleOrSubModule.B4, "b4"),
    (LCAStageOrModuleOrSubModule.B5, "b5"),
    (LCAStageOrModuleOrSubModule.B6, "b6"),
    (LCAStageOrModuleOrSubModule.B6_1, "b6_1"),
    (LCAStageOrModuleOrSubModule.B6_2, "b6_2"),
    (LCAStageOrModuleOrSubModule.B6_3, "b6_3"),
    (LCAStageOrModuleOrSubModule.B7, "b7"),
    (LCAStageOrModuleOrSubModule.B7_1, "b7_1"),
    (LCAStageOrModuleOrSubModule.B7_2, "b7_2"),
    (LCAStageOrModuleOrSubModule.B7_3, "b7_3"),
    (LCAStageOrModuleOrSubModule.B8, "b8"),
    (LCAStageOrModuleOrSubModule.B8_1, "b8_1"),
    (LCAStageOrModuleOrSubModule.B8_2, "b8_2"),
    (LCAStageOrModuleOrSubModule.B8_3, "b8_3"),
    (LCAStageOrModuleOrSubModule.C1, "c1"),
    (LCAStageOrModuleOrSubModule.C2, "c2"),
    (LCAStageOrModuleOrSubModule.C3, "c3"),
    (LCAStageOrModuleOrSubModule.C4, "c4"),
    (LCAStageOrModuleOrSubModule.D, "d"),
    (LCAStageOrModuleOrSubModule.D1, "d1"),
    (LCAStageOrModuleOrSubModule.D2, "d2"),
)

# Every LCA impact indicator present in the tall and wide models.
# `gwp_total` is special: it carries the sub-module stage columns (GWP_TOTAL_STAGES) and
# its `a1_a3` stage field is required.
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
        description="Ozone Depletion Potential",
    ),
    LCAResultIndicator(
        code="ap",
        attribute_name="Acidification Potential",
        units="kg SO₂ eq.",
        requirements="Optional",
        wide_attribute="Acidification potential",
    ),
    LCAResultIndicator(
        code="ep",
        attribute_name="Eutrophication Potential",
        units="kg N eq",
        requirements="Optional",
        wide_attribute="Eutrophication potential",
        wide_b7_b8_attribute="Total Acidification Potential",
    ),
    LCAResultIndicator(
        code="ep_af",
        attribute_name="Eutrophication potential, freshwater",
        units="kg PO4 eq",
        requirements="Optional",
        description="Eutrophication Potential - Aquatic Freshwater.",
        wide_attribute="Eutrophication potential, freshwater, EN 15804+A2",
        wide_b7_b8_attribute="Eutrophication Potential",
    ),
    LCAResultIndicator(
        code="ep_am",
        attribute_name="Eutrophication potential, marine",
        units="kg N eq",
        requirements="Optional",
        description="Eutrophication Potential - Aquatic Marine.",
        wide_attribute="Eutrophication potential, marine, EN 15804+A2",
        wide_b7_b8_attribute="Eutrophication Potential - Aquatic Freshwater",
    ),
    LCAResultIndicator(
        code="ep_t",
        attribute_name="Eutrophication potential, terrestrial",
        units="mol N eq",
        requirements="Optional",
        description="Eutrophication Potential - Terrestrial.",
        wide_attribute="Eutrophication potential, terrestrial, EN 15804+A2",
        wide_b7_b8_attribute="Eutrophication Potential - Aquatic Marine",
    ),
    LCAResultIndicator(
        code="pocp",
        attribute_name="Formation potential of tropospheric ozone",
        units="kg C2H4 eq",
        requirements="Optional",
        description="Photochemical Ozone Creation Potential.",
        wide_attribute="Formation potential of tropospheric ozone, EN 15804+A1",
        wide_b7_b8_attribute="Eutrophication Potential - Aquatic Marine",
    ),
    LCAResultIndicator(
        code="sfp",
        attribute_name="Smog formation potential",
        units="kg O3 eq",
        requirements="Optional",
        description="Smog Forming Potential.",
        wide_attribute="Smog formation potential",
        wide_b7_b8_attribute="Photochemical Ozone Creation Potential",
    ),
    LCAResultIndicator(
        code="pofp",
        attribute_name="Formation potential of tropospheric ozone",
        units="kg NMVOC eq",
        requirements="Optional",
        description="Photochemical Ozone Formation Potential.",
        wide_attribute="Formation potential of tropospheric ozone, EN 15804+A2",
        wide_b7_b8_attribute="Smog Forming Potential",
    ),
    LCAResultIndicator(
        code="adpmm",
        attribute_name="Abiotic Depletion Potential (Minerals and Metals)",
        units="kg Sb eq",
        requirements="Optional",
        wide_b7_b8_attribute="Photochemical Ozone Formation Potential",
    ),
    LCAResultIndicator(
        code="adpf",
        attribute_name="Abiotic Depletion Potential (Fossil Fuels)",
        units="MJ",
        requirements="Optional",
        wide_b7_b8_attribute="Abiotic Depletion Potential (Minerals and Metals)",
    ),
    LCAResultIndicator(
        code="wdp",
        attribute_name="Water Depletion Potential",
        units="m3 world eq",
        requirements="Optional",
        wide_b7_b8_attribute="Abiotic Depletion Potential (Fossil Fuels)",
    ),
    LCAResultIndicator(
        code="pere",
        attribute_name="Primary Energy Renewable (Energy resources)",
        units="MJ",
        requirements="Optional",
        wide_b7_b8_attribute="Water Depletion Potential",
    ),
    LCAResultIndicator(
        code="penre",
        attribute_name="Primary Energy Non-Renewable (Energy resources)",
        units="MJ",
        requirements="Optional",
        wide_b7_b8_attribute="Total Water Depletion Potential",
    ),
    LCAResultIndicator(
        code="pert",
        attribute_name="Primary Energy Renewable Total",
        units="MJ",
        requirements="Optional",
        wide_b7_b8_attribute="Primary Energy Renewable (Energy resources)",
    ),
    LCAResultIndicator(
        code="penrt",
        attribute_name="Primary Energy Non-Renewable Total",
        units="MJ",
        requirements="Optional",
        wide_b7_b8_attribute="Primary Energy Non-Renewable (Energy resources)",
    ),
    LCAResultIndicator(
        code="pm",
        attribute_name="Particulate matter emissions",
        units="disease incidence",
        requirements="Optional",
        description="Particulate matter emissions",
        wide_constant_description="Particulate matter emissions",
        wide_total_attribute="Particulate matter emissions (total)",
        wide_b7_b8_attribute="Primary Energy Renewable Total",
    ),
    LCAResultIndicator(
        code="irp",
        attribute_name="Ionising radiation, human health",
        units="kBq U235 eq",
        requirements="Optional",
        description="Ionising radiation, human health",
        wide_constant_description="Ionising radiation, human health",
        wide_total_attribute="Ionising radiation, human health (total)",
        wide_b7_b8_attribute="Primary Energy Non-Renewable (Energy resources)",
    ),
    LCAResultIndicator(
        code="etp_fw",
        attribute_name="Ecotoxicity, freshwater",
        units="CTUe",
        requirements="Optional",
        description="Ecotoxicity, freshwater",
        wide_constant_description="Ecotoxicity, freshwater",
        wide_total_attribute="Ecotoxicity, freshwater (total)",
        wide_b7_b8_attribute="Particulate matter emissions",
    ),
    LCAResultIndicator(
        code="htp_c",
        attribute_name="Human toxicity, cancer effects",
        units="CTUh",
        requirements="Optional",
        description="Human toxicity, cancer effects",
        wide_constant_description="Human toxicity, cancer effects",
        wide_total_attribute="Human toxicity, cancer effects (total)",
        wide_b7_b8_attribute="Ionising radiation, human health",
    ),
    LCAResultIndicator(
        code="htp_nc",
        attribute_name="Human toxicity, non-cancer effects",
        units="CTUh",
        requirements="Optional",
        description="Human toxicity, non-cancer effects",
        wide_constant_description="Human toxicity, non-cancer effects",
        wide_total_attribute="Human toxicity, non-cancer effects (total)",
        wide_b7_b8_attribute="Ecotoxicity, freshwater",
    ),
    LCAResultIndicator(
        code="sqp",
        attribute_name="Soil quality index",
        units="-",
        requirements="Optional",
        description="Soil quality index",
        wide_constant_description="Soil quality index",
        wide_total_attribute="Soil quality index (total)",
        wide_b7_b8_attribute="Human toxicity, cancer effects",
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

# Row-1 attribute labels of the wide sheet reproduced verbatim from the target workbook:
# the target keeps a stray 'UPDATED Criticality (RFC 2119)' header on the gwp_total_b4 column.
_WIDE_ATTRIBUTE_OVERRIDES: dict[str, str] = {
    "gwp_total_b4": "UPDATED Criticality (RFC 2119)",
}

# Descriptions of the gwp_total sub-module columns, from the target workbook.
_GWP_TOTAL_SUBMODULE_DESCRIPTIONS: dict[str, str] = {
    "a5_1": "Pre-construction demolition.",
    "a5_2": "Construction activities.",
    "a5_3": "Waste and waste management.",
    "a5_4": "Worker transport.",
}

# The target workbook labels the descriptions of the B7 and B8 columns 'module B6'
# (carried over from the B6 columns). Reproduced verbatim.
_DESC_MODULE_B6_SUFFIXES = frozenset({"b7", "b8", "b7_1", "b7_2", "b7_3", "b8_1", "b8_2", "b8_3"})


def _q(value: str) -> str:
    """Wrap a string in double quotes for source emission."""
    return '"' + value.replace('"', '\\"') + '"'


def _total_code(code: str) -> str:
    """Field code of the wide total field for an indicator."""
    return f"{code}_total"


def _total_attribute_name(attribute_name: str) -> str:
    """Attribute name of the wide total field for an indicator.

    The target keeps a trailing ' - Total' suffix on the attribute
    ('Total Global Warming Potential - Total').
    """
    return f"Total {attribute_name}"


def _total_description(indicator: LCAResultIndicator) -> str:
    """Description of the wide total field for an indicator."""
    base = indicator.description if indicator.description is not None else indicator.attribute_name
    if base.endswith("."):
        base = base[:-1]
    if base.endswith(_TRAILING_TOTAL_SUFFIX):
        base = base[: -len(_TRAILING_TOTAL_SUFFIX)]
    return f"Total {base}."


def _wide_stage_description(indicator: LCAResultIndicator, stage: LCAStageOrModuleOrSubModule, suffix: str) -> str:
    """Description of one wide stage field for an indicator."""
    if indicator.wide_constant_description is not None:
        return indicator.wide_constant_description
    base = indicator.description if indicator.description is not None else indicator.attribute_name
    if base.endswith("."):
        base = base[:-1]
    if suffix in _DESC_MODULE_B6_SUFFIXES:
        module = "B6"
    elif "." in stage.value:
        # Sub-module columns describe their parent module ('B1.1' describes module B1).
        module = stage.value.split(".")[0]
    else:
        module = stage.value
    return f"{base} for module {module}."


def _wide_stage_attribute(indicator: LCAResultIndicator, stage: LCAStageOrModuleOrSubModule, suffix: str) -> str:
    """Attribute name of one wide stage field for an indicator."""
    if suffix in ("b7", "b8"):
        base = (
            indicator.wide_b7_b8_attribute if indicator.wide_b7_b8_attribute is not None else indicator.attribute_name
        )
        return f"{base} ({stage.value})"
    if indicator.wide_attribute is not None:
        return indicator.wide_attribute
    return f"{indicator.attribute_name} ({stage.value})"


def _render_field(
    *,
    name: str,
    type_: str,
    default: str | None,
    requirements: str | None,
    criticality: str,
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
    lines.append(f"            criticality={_q(criticality)},")
    lines.append("        ),")
    lines.append("    )")
    return "\n".join(lines)


def _material_id_field() -> str:
    return _render_field(
        name="material_id",
        type_="str",
        default=None,
        requirements="Required",
        criticality="MUST",
        attribute_name="Material ID",
        field_code="material_id",
        description=(
            "The unique identifier for the material within the project context, referencing the Bill of Materials."
        ),
        units=None,
        max_length=200,
    )


def _lca_stage_module_submodule_field() -> str:
    return _render_field(
        name="lca_stage_module_submodule",
        type_="LCAStageOrModuleOrSubModule",
        default=None,
        requirements="Required",
        criticality="MUST",
        attribute_name="Life cycle stage or module or submodule",
        field_code="lca_stage_module_submodule",
        description="Life-cycle stage or module or submodule of this result row, such as A1-A3 or A5 or A5.1 ",
        units=None,
    )


def _lca_stage_field() -> str:
    return _render_field(
        name="lca_stage",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements="Automatic",
        criticality="MAY",
        attribute_name="Life cycle stage",
        field_code="lca_stage",
        description="Life-cycle stage of the module, derived by the parser from Life cycle module.",
        units=None,
    )


def _lca_module_field() -> str:
    return _render_field(
        name="lca_module",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements="Automatic",
        criticality="MAY",
        attribute_name="Life cycle module",
        field_code="lca_module",
        description="Life-cycle of the module, derived by the parser from Life cycle module.",
        units=None,
    )


def _lca_submodule_field() -> str:
    return _render_field(
        name="lca_submodule",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements="Automatic",
        criticality="MAY",
        attribute_name="Life cycle sub-module",
        field_code="lca_submodule",
        description="Sub-module where the standard defines one.",
        units=None,
    )


def _process_year_field() -> str:
    return _render_field(
        name="process_year",
        type_="Optional[int]",
        default="None",
        requirements="Recommended",
        criticality="MAY",
        attribute_name="Process year",
        field_code="process_year",
        description="Year in which the activity occurs.",
        units="year",
    )


def _material_flow_type_field() -> str:
    return _render_field(
        name="material_flow_type",
        type_="Optional[MaterialFlowType]",
        default="None",
        requirements="Recommended",
        criticality="MAY",
        attribute_name="Material flow type",
        field_code="material_flow_type",
        description="Type of flow at this row.",
        units="None",
    )


def _material_flow_mass_kg_field() -> str:
    return _render_field(
        name="material_flow_mass_kg",
        type_="Optional[Decimal]",
        default="None",
        requirements="Recommended",
        criticality="MAY",
        attribute_name="Material Flow Mass (kg)",
        field_code="material_flow_mass_kg",
        description="Mass carried by the flow at this row.",
        units="kg",
    )


def _scenario_label_field() -> str:
    return _render_field(
        name="scenario_label",
        type_="Optional[str]",
        default="None",
        requirements="Recommended",
        criticality="MAY",
        attribute_name="Scenario label",
        field_code="scenario_label",
        description="Scenario the result belongs to.",
        units="None",
    )


def _tall_indicator_field(indicator: LCAResultIndicator) -> str:
    return _render_field(
        name=indicator.code,
        type_="Optional[Decimal]",
        default="None",
        requirements=indicator.requirements,
        criticality=indicator.criticality,
        attribute_name=indicator.attribute_name,
        field_code=indicator.code,
        description=(indicator.description if indicator.description is not None else f"{indicator.attribute_name}."),
        units=indicator.units,
    )


def _wide_stage_field(
    indicator: LCAResultIndicator,
    stage: LCAStageOrModuleOrSubModule,
    suffix: str,
) -> str:
    required = indicator.required_in_wide and suffix == "a1_a3"
    if required:
        requirements = "Required"
    elif suffix in OPTIONAL_STAGE_SUFFIXES:
        requirements = "Optional"
    else:
        requirements = indicator.requirements
    field_code = f"{indicator.code}_{suffix}"
    return _render_field(
        name=field_code,
        type_="Decimal" if required else "Optional[Decimal]",
        default=None if required else "None",
        requirements=requirements,
        criticality="SHOULD" if required else "MAY",
        attribute_name=_WIDE_ATTRIBUTE_OVERRIDES.get(field_code, _wide_stage_attribute(indicator, stage, suffix)),
        field_code=field_code,
        description=_GWP_TOTAL_SUBMODULE_DESCRIPTIONS.get(suffix, _wide_stage_description(indicator, stage, suffix)),
        units=indicator.units,
    )


def _wide_total_field(indicator: LCAResultIndicator) -> str:
    total_name = _total_code(indicator.code)
    if indicator.wide_total_attribute is not None:
        total_attribute = indicator.wide_total_attribute
    elif indicator.wide_attribute is not None:
        total_attribute = indicator.wide_attribute
    else:
        total_attribute = _total_attribute_name(indicator.attribute_name)
    if indicator.wide_constant_description is not None:
        total_description = indicator.wide_constant_description
    else:
        total_description = _total_description(indicator)
    return _render_field(
        name=total_name,
        type_="Optional[Decimal]",
        default="None",
        requirements=indicator.requirements,
        criticality="MAY",
        attribute_name=total_attribute,
        field_code=total_name,
        description=total_description,
        units=indicator.units,
    )


_TALL_IMPORTS = (
    "from __future__ import annotations\n\n"
    "from decimal import Decimal\n"
    "from typing import Optional\n\n"
    "from sqlmodel import Field, SQLModel\n\n"
    "from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule\n"
    "from openbdf.model.enums.materials import MaterialFlowType\n\n"
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
        _lca_stage_module_submodule_field(),
        _lca_stage_field(),
        _lca_module_field(),
        _lca_submodule_field(),
        _process_year_field(),
        _material_flow_type_field(),
        _material_flow_mass_kg_field(),
        _scenario_label_field(),
    ]
    blocks.extend(_tall_indicator_field(indicator) for indicator in INDICATORS)
    body = "\n\n".join(blocks)
    return _HEADER + _TALL_IMPORTS + "class LCAResultsTallBase(SQLModel):\n" + body + "\n"


def render_wide_module() -> str:
    """Render the source of the LCAResultsWideFullBase model module."""
    blocks: list[str] = [_material_id_field()]
    for indicator in INDICATORS:
        stages = GWP_TOTAL_STAGES if indicator.code == "gwp_total" else STAGES
        for stage, suffix in stages:
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
