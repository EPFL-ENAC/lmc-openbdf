from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule
from openbdf.model.enums.references import ReferenceAlignment
from openbdf.model.enums.requirement import Requirement


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
    requirements: Requirement
    # Reference alignment of the wide stage columns and of the tall field. Both sheets
    # cite the same standard in different words, so each one carries its own value.
    wide_alignment: ReferenceAlignment
    tall_alignment: ReferenceAlignment
    description: str | None = None
    required_in_wide: bool = False
    # Alignment of the b8, d1, d2 and total columns, which most indicators align with the
    # regulation only. Five indicators align these columns with TRACI as well.
    wide_total_alignment: ReferenceAlignment = ReferenceAlignment.EU2026_52_ANNEX_III
    # Wide-sheet label and description overrides reproduced from the target workbook:
    # some indicators label every stage column (and the total column) with a fixed
    # attribute instead of '<attribute> (<stage>)', and some use a fixed description.
    wide_attribute: str | None = None
    wide_total_attribute: str | None = None
    wide_constant_description: str | None = None
    wide_b7_b8_attribute: str | None = None
    # Append the stage suffix to the wide_attribute instead of using it as a constant label.
    wide_stage_suffixed: bool = False
    # Wide-only description base, for indicators whose wide stage columns describe
    # themselves differently from the tall description.
    wide_description: str | None = None


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

# Reference alignment of the sub-module columns. Only gwp_total carries them.
SUB_MODULE_ALIGNMENTS: dict[str, ReferenceAlignment] = {
    "a5_1": ReferenceAlignment.TRACI,
    "a5_2": ReferenceAlignment.TRACI,
    "a5_3": ReferenceAlignment.TRACI,
    "a5_4": ReferenceAlignment.TRACI,
    "b1_1": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b1_2": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b6_1": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b6_2": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b6_3": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b7_1": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b7_2": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b7_3": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b8_1": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b8_2": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    "b8_3": ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
}

# Stage columns that report an indicator total instead of a single stage.
TOTAL_STAGE_SUFFIXES = ("b8", "d1", "d2")

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
# its `a1_a3` stage field is strongly recommended instead of suggested.
INDICATORS: tuple[LCAResultIndicator, ...] = (
    LCAResultIndicator(
        code="gwp_total",
        attribute_name="Global Warming Potential - Total",
        units="kg CO₂ eq",
        requirements=Requirement.SUGGESTED,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_TRACI_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_A2_AND_TRACI,
        wide_total_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
        required_in_wide=True,
    ),
    LCAResultIndicator(
        code="gwp_f",
        attribute_name="Global Warming Potential - Fossil",
        units="kg CO₂ eq",
        requirements=Requirement.SUGGESTED,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
    ),
    LCAResultIndicator(
        code="gwp_b",
        attribute_name="Global Warming Potential - Biogenic",
        units="kg CO₂ eq",
        requirements=Requirement.SUGGESTED,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
    ),
    LCAResultIndicator(
        code="gwp_luc",
        attribute_name="Global Warming Potential - Land Use and Land Use Change",
        units="kg CO₂ eq",
        requirements=Requirement.SUGGESTED,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
    ),
    LCAResultIndicator(
        code="odp",
        attribute_name="Ozone Depletion Potential",
        units="kg CFC-11 eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_TRACI_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_A2_AND_TRACI,
        wide_total_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
        description="Ozone Depletion Potential",
    ),
    LCAResultIndicator(
        code="ap",
        attribute_name="Acidification Potential",
        units="kg SO₂ eq.",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_TRACI_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_TRACI,
        wide_total_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    ),
    LCAResultIndicator(
        code="ap_ae",
        attribute_name="Acidification Potential - Accumulated Exceedance",
        units="mol H+ eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Acidification Potential.",
        wide_description="Acidification Potential (accumulated exceedance)",
    ),
    LCAResultIndicator(
        code="ep",
        attribute_name="Eutrophication Potential",
        units="kg N eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.TRACI,
        wide_total_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
    ),
    LCAResultIndicator(
        code="ep_af",
        attribute_name="Eutrophication Potential - Aquatic Freshwater",
        units="kg PO4 eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Eutrophication Potential - Aquatic Freshwater.",
        wide_b7_b8_attribute="Eutrophication Potential - Freshwater",
    ),
    LCAResultIndicator(
        code="ep_am",
        attribute_name="Eutrophication Potential - Aquatic Marine",
        units="kg N eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Eutrophication Potential - Aquatic Marine.",
    ),
    LCAResultIndicator(
        code="ep_t",
        attribute_name="Eutrophication Potential - Terrestrial",
        units="mol N eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Eutrophication Potential - Terrestrial.",
        wide_b7_b8_attribute="Eutrophication Potential - Aquatic Marine",
    ),
    LCAResultIndicator(
        code="pocp",
        attribute_name="Photochemical Ozone Creation Potential",
        units="kg C2H4 eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1,
        description="Photochemical Ozone Creation Potential.",
        wide_b7_b8_attribute="Eutrophication Potential - Aquatic Marine",
    ),
    LCAResultIndicator(
        code="sfp",
        attribute_name="Smog Forming Potential",
        units="kg O3 eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.TRACI,
        wide_total_alignment=ReferenceAlignment.TRACI_EU2026_52_ANNEX_III,
        description="Smog Forming Potential.",
        wide_b7_b8_attribute="Photochemical Ozone Creation Potential",
    ),
    LCAResultIndicator(
        code="pofp",
        attribute_name="Formation potential of tropospheric ozone",
        units="kg NMVOC eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Photochemical Ozone Formation Potential.",
        wide_attribute="Photochemical Ozone Formation Potential",
        wide_stage_suffixed=True,
        wide_total_attribute="Total Photochemical Ozone Formation Potential",
        wide_b7_b8_attribute="Smog Forming Potential",
    ),
    LCAResultIndicator(
        code="adpmm",
        attribute_name="Abiotic Depletion Potential - Minerals and Metals",
        units="kg Sb eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        description="Abiotic Depletion Potential (Minerals and Metals).",
        wide_b7_b8_attribute="Photochemical Ozone Formation Potential",
    ),
    # The target keeps the parenthesized style on the adpf total and wdp B7/B8 wide labels.
    LCAResultIndicator(
        code="adpf",
        attribute_name="Abiotic Depletion Potential - Fossil Fuels",
        units="MJ",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        description="Abiotic Depletion Potential (Fossil Fuels).",
        wide_total_attribute="Total Abiotic Depletion Potential (Fossil Fuels)",
    ),
    LCAResultIndicator(
        code="wdp",
        attribute_name="Water Depletion Potential",
        units="m3 world eq deprived",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2_M3_WORLD_EQ_DEPRIVED,
        wide_b7_b8_attribute="Abiotic Depletion Potential (Fossil Fuels)",
    ),
    LCAResultIndicator(
        code="pere",
        attribute_name="Primary Energy Renewable - Energy Resources",
        units="MJ",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        description="Primary Energy Renewable (Energy resources).",
    ),
    LCAResultIndicator(
        code="penre",
        attribute_name="Primary Energy Non-Renewable - Energy Resources",
        units="MJ",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        description="Primary Energy Non-Renewable (Energy resources).",
    ),
    LCAResultIndicator(
        code="pert",
        attribute_name="Primary Energy Renewable Total",
        units="MJ",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        wide_b7_b8_attribute="Primary Energy Renewable (Energy resources)",
    ),
    LCAResultIndicator(
        code="penrt",
        attribute_name="Primary Energy Non-Renewable Total",
        units="MJ",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A1_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A1_AND_EN15804_A2,
        wide_b7_b8_attribute="Primary Energy Non-Renewable (Energy resources)",
    ),
    LCAResultIndicator(
        code="pm",
        attribute_name="Particulate Matter Emissions",
        units="disease incidence",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Particulate matter emissions",
        wide_constant_description="Particulate Matter Emissions",
        wide_total_attribute="Particulate Matter Emissions (total)",
    ),
    LCAResultIndicator(
        code="irp",
        attribute_name="Ionising Radiation - Human Health",
        units="kBq U235 eq",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Ionising radiation, human health",
        wide_constant_description="Ionising radiation, human health",
        wide_total_attribute="Ionising Radiation - Human Health (total)",
    ),
    LCAResultIndicator(
        code="etp_fw",
        attribute_name="Ecotoxicity - Freshwater",
        units="CTUe",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Ecotoxicity, freshwater",
        wide_constant_description="Ecotoxicity - Freshwater",
        wide_total_attribute="Ecotoxicity - Freshwater (total)",
    ),
    LCAResultIndicator(
        code="htp_c",
        attribute_name="Human Toxicity - Cancer Effects",
        units="CTUh",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Human toxicity, cancer effects",
        wide_constant_description="Human Toxicity - Cancer Effects",
        wide_total_attribute="Human Toxicity - Cancer Effects (total)",
    ),
    LCAResultIndicator(
        code="htp_nc",
        attribute_name="Human Toxicity - Non-cancer Effects",
        units="CTUh",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Human toxicity, non-cancer effects",
        wide_constant_description="Human Toxicity - Non-cancer Effects",
        wide_total_attribute="Human Toxicity - Non-cancer Effects (total)",
    ),
    LCAResultIndicator(
        code="sqp",
        attribute_name="Soil Quality Index",
        units="-",
        requirements=Requirement.OPTIONAL,
        wide_alignment=ReferenceAlignment.EN15804_A2_EU2026_52_ANNEX_III,
        tall_alignment=ReferenceAlignment.EN15804_A2,
        description="Soil quality index",
        wide_constant_description="Soil Quality Index",
        wide_total_attribute="Soil Quality Index (total)",
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


def _wide_description_base(indicator: LCAResultIndicator) -> str:
    """Attribute phrase the wide stage and total descriptions are built from."""
    base = (
        indicator.wide_description
        if indicator.wide_description is not None
        else indicator.description
        if indicator.description is not None
        else indicator.attribute_name
    )
    if base.endswith("."):
        base = base[:-1]
    return base


def _total_description(indicator: LCAResultIndicator) -> str:
    """Description of the wide total field for an indicator."""
    base = _wide_description_base(indicator)
    if base.endswith(_TRAILING_TOTAL_SUFFIX):
        base = base[: -len(_TRAILING_TOTAL_SUFFIX)]
    return f"Total {base}."


def _wide_stage_description(indicator: LCAResultIndicator, stage: LCAStageOrModuleOrSubModule, suffix: str) -> str:
    """Description of one wide stage field for an indicator."""
    if indicator.wide_constant_description is not None:
        return indicator.wide_constant_description
    return f"{_wide_description_base(indicator)} for module {stage.value}."


def _wide_stage_attribute(indicator: LCAResultIndicator, stage: LCAStageOrModuleOrSubModule, suffix: str) -> str:
    """Attribute name of one wide stage field for an indicator."""
    if suffix in ("b7", "b8"):
        base = (
            indicator.wide_b7_b8_attribute if indicator.wide_b7_b8_attribute is not None else indicator.attribute_name
        )
        return f"{base} ({stage.value})"
    if indicator.wide_attribute is not None:
        if indicator.wide_stage_suffixed:
            return f"{indicator.wide_attribute} ({stage.value})"
        return indicator.wide_attribute
    return f"{indicator.attribute_name} ({stage.value})"


def _render_field(
    *,
    name: str,
    type_: str,
    default: str | None,
    requirements: Requirement,
    attribute_name: str,
    field_code: str,
    description: str,
    units: str | None,
    reference_alignment: ReferenceAlignment | None = None,
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
    lines.append(f"            requirements=Requirement.{requirements.name},")
    if reference_alignment is not None:
        lines.append(f"            reference_alignment=ReferenceAlignment.{reference_alignment.name},")
    lines.append("        ),")
    lines.append("    )")
    return "\n".join(lines)


def _material_id_field(tall: bool) -> str:
    return _render_field(
        name="material_id",
        type_="str",
        default=None,
        requirements=Requirement.REQUIRED,
        attribute_name="Material ID",
        field_code="material_id",
        description=(
            "The unique identifier for the material within the project context, referencing the Bill of Materials."
        ),
        units=None,
        # The target workbook leaves the wide cell empty.
        reference_alignment=ReferenceAlignment.GBDI if tall else None,
        max_length=200,
    )


def _lca_stage_module_submodule_field() -> str:
    return _render_field(
        name="lca_stage_module_submodule",
        type_="LCAStageOrModuleOrSubModule",
        default=None,
        requirements=Requirement.REQUIRED,
        attribute_name="Life cycle stage or module or submodule",
        field_code="lca_stage_module_submodule",
        description="Life-cycle stage or module or submodule of this result row, such as A1-A3 or A5 or A5.1 ",
        units=None,
        reference_alignment=ReferenceAlignment.EN15978_EN15978_2026,
    )


def _lca_stage_field() -> str:
    return _render_field(
        name="lca_stage",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements=Requirement.AUTOMATIC,
        attribute_name="Life cycle stage",
        field_code="lca_stage",
        description="Life-cycle stage of the module, derived by the parser from Life cycle module.",
        units=None,
        reference_alignment=ReferenceAlignment.EN15978_EN15978_2027,
    )


def _lca_module_field() -> str:
    return _render_field(
        name="lca_module",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements=Requirement.AUTOMATIC,
        attribute_name="Life cycle module",
        field_code="lca_module",
        description="Life-cycle of the module, derived by the parser from Life cycle module.",
        units=None,
        reference_alignment=ReferenceAlignment.EN15978_EN15978_2028,
    )


def _lca_submodule_field() -> str:
    return _render_field(
        name="lca_submodule",
        type_="Optional[LCAStageOrModuleOrSubModule]",
        default="None",
        requirements=Requirement.AUTOMATIC,
        attribute_name="Life cycle sub-module",
        field_code="lca_submodule",
        description="Sub-module where the standard defines one.",
        units=None,
        reference_alignment=ReferenceAlignment.EN15978_EN15978_2029,
    )


def _process_year_field() -> str:
    return _render_field(
        name="process_year",
        type_="Optional[int]",
        default="None",
        requirements=Requirement.SUGGESTED,
        attribute_name="Process year",
        field_code="process_year",
        description="Year in which the activity occurs.",
        units="year",
        reference_alignment=ReferenceAlignment.EN15804_EN15978_ISO_21930,
    )


def _material_flow_type_field() -> str:
    return _render_field(
        name="material_flow_type",
        type_="Optional[MaterialFlowType]",
        default="None",
        requirements=Requirement.SUGGESTED,
        attribute_name="Material flow type",
        field_code="material_flow_type",
        description="Type of flow at this row.",
        units="None",
        reference_alignment=ReferenceAlignment.EN15978_ISO14040_14044,
    )


def _material_flow_mass_kg_field() -> str:
    return _render_field(
        name="material_flow_mass_kg",
        type_="Optional[Decimal]",
        default="None",
        requirements=Requirement.SUGGESTED,
        attribute_name="Material Flow Mass (kg)",
        field_code="material_flow_mass_kg",
        description="Mass carried by the flow at this row.",
        units="kg",
        reference_alignment=ReferenceAlignment.EN15978_ISO14040_14044,
    )


def _scenario_label_field() -> str:
    return _render_field(
        name="scenario_label",
        type_="Optional[str]",
        default="None",
        requirements=Requirement.SUGGESTED,
        attribute_name="Scenario label",
        field_code="scenario_label",
        description="Scenario the result belongs to.",
        units="None",
        reference_alignment=ReferenceAlignment.EN15978,
    )


def _tall_indicator_field(indicator: LCAResultIndicator) -> str:
    return _render_field(
        name=indicator.code,
        type_="Optional[Decimal]",
        default="None",
        requirements=indicator.requirements,
        attribute_name=indicator.attribute_name,
        field_code=indicator.code,
        description=(indicator.description if indicator.description is not None else f"{indicator.attribute_name}."),
        units=indicator.units,
        reference_alignment=indicator.tall_alignment,
    )


def _wide_stage_field(
    indicator: LCAResultIndicator,
    stage: LCAStageOrModuleOrSubModule,
    suffix: str,
) -> str:
    required = indicator.required_in_wide and suffix == "a1_a3"
    if required:
        requirements = Requirement.STRONGLY_RECOMMENDED
    elif suffix in OPTIONAL_STAGE_SUFFIXES:
        requirements = Requirement.OPTIONAL
    else:
        requirements = indicator.requirements
    field_code = f"{indicator.code}_{suffix}"
    if suffix in SUB_MODULE_ALIGNMENTS:
        reference_alignment = SUB_MODULE_ALIGNMENTS[suffix]
    elif suffix in TOTAL_STAGE_SUFFIXES:
        reference_alignment = indicator.wide_total_alignment
    else:
        reference_alignment = indicator.wide_alignment
    return _render_field(
        name=field_code,
        type_="Optional[Decimal]",
        default="None",
        requirements=requirements,
        attribute_name=_wide_stage_attribute(indicator, stage, suffix),
        field_code=field_code,
        description=_wide_stage_description(indicator, stage, suffix),
        units=indicator.units,
        reference_alignment=reference_alignment,
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
        attribute_name=total_attribute,
        field_code=total_name,
        description=total_description,
        units=indicator.units,
        reference_alignment=indicator.wide_total_alignment,
    )


_TALL_IMPORTS = (
    "from __future__ import annotations\n\n"
    "from decimal import Decimal\n"
    "from typing import Optional\n\n"
    "from sqlmodel import Field, SQLModel\n\n"
    "from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule\n"
    "from openbdf.model.enums.materials import MaterialFlowType\n"
    "from openbdf.model.enums.references import ReferenceAlignment\n"
    "from openbdf.model.enums.requirement import Requirement\n\n"
    "from .field_metadata import openbdf_field_metadata\n\n\n"
)

_WIDE_IMPORTS = (
    "from __future__ import annotations\n\n"
    "from decimal import Decimal\n"
    "from typing import Optional\n\n"
    "from sqlmodel import Field, SQLModel\n\n"
    "from openbdf.model.enums.references import ReferenceAlignment\n"
    "from openbdf.model.enums.requirement import Requirement\n\n"
    "from .field_metadata import openbdf_field_metadata\n\n\n"
)


def render_tall_module() -> str:
    """Render the source of the LCAResultsTallBase model module."""
    blocks: list[str] = [
        _material_id_field(tall=True),
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
    blocks: list[str] = [_material_id_field(tall=False)]
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
