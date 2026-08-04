from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

from openbdf.model.enums.lca import LCAStageOrModule

from .field_metadata import openbdf_field_metadata


class LCAResultsTallBase(SQLModel):
    material_id: str = Field(
        max_length=200,
        description="The unique identifier for the material within the project context, referencing the Bill of Materials.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material ID",
            field_code="material_id",
            description="The unique identifier for the material within the project context, referencing the Bill of Materials.",
            requirements="Required",
        ),
    )

    lca_service_life: Decimal = Field(
        description="Declared reference service life.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Service life",
            field_code="lca_service_life",
            description="Declared reference service life.",
            units="years",
        ),
    )

    lca_stage_or_module: LCAStageOrModule = Field(
        description="Life cycle assessment stage or module for this result row.",
        schema_extra=openbdf_field_metadata(
            attribute_name="LCA stage or module",
            field_code="lca_stage_or_module",
            description="Life cycle assessment stage or module for this result row.",
            units=None,
            requirements="Required",
        ),
    )

    gwp_total: Optional[Decimal] = Field(
        default=None,
        description="Global Warming Potential - Total.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total",
            field_code="gwp_total",
            description="Global Warming Potential - Total.",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f: Optional[Decimal] = Field(
        default=None,
        description="Global Warming Potential - Fossil.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil",
            field_code="gwp_f",
            description="Global Warming Potential - Fossil.",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b: Optional[Decimal] = Field(
        default=None,
        description="Global Warming Potential - Biogenic.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic",
            field_code="gwp_b",
            description="Global Warming Potential - Biogenic.",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc: Optional[Decimal] = Field(
        default=None,
        description="Global Warming Potential - Land Use and Land Use Change.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Land Use and Land Use Change",
            field_code="gwp_luc",
            description="Global Warming Potential - Land Use and Land Use Change.",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    odp: Optional[Decimal] = Field(
        default=None,
        description="Ozone Depletion Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential",
            field_code="odp",
            description="Ozone Depletion Potential.",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    ap: Optional[Decimal] = Field(
        default=None,
        description="Acidification Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential",
            field_code="ap",
            description="Acidification Potential.",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ep: Optional[Decimal] = Field(
        default=None,
        description="Eutrophication Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential",
            field_code="ep",
            description="Eutrophication Potential.",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_af: Optional[Decimal] = Field(
        default=None,
        description="Eutrophication Potential - Aquatic Freshwater.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater",
            field_code="ep_af",
            description="Eutrophication Potential - Aquatic Freshwater.",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )

    ep_am: Optional[Decimal] = Field(
        default=None,
        description="Eutrophication Potential - Aquatic Marine.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine",
            field_code="ep_am",
            description="Eutrophication Potential - Aquatic Marine.",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_t: Optional[Decimal] = Field(
        default=None,
        description="Eutrophication Potential - Terrestrial.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial",
            field_code="ep_t",
            description="Eutrophication Potential - Terrestrial.",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )

    pocp: Optional[Decimal] = Field(
        default=None,
        description="Photochemical Ozone Creation Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Creation Potential",
            field_code="pocp",
            description="Photochemical Ozone Creation Potential.",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )

    sfp: Optional[Decimal] = Field(
        default=None,
        description="Smog Forming Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential",
            field_code="sfp",
            description="Smog Forming Potential.",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )

    pofp: Optional[Decimal] = Field(
        default=None,
        description="Photochemical Ozone Formation Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential",
            field_code="pofp",
            description="Photochemical Ozone Formation Potential.",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )

    adpmm: Optional[Decimal] = Field(
        default=None,
        description="Abiotic Depletion Potential (Minerals and Metals).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals)",
            field_code="adpmm",
            description="Abiotic Depletion Potential (Minerals and Metals).",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpf: Optional[Decimal] = Field(
        default=None,
        description="Abiotic Depletion Potential (Fossil Fuels).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels)",
            field_code="adpf",
            description="Abiotic Depletion Potential (Fossil Fuels).",
            units="MJ",
            requirements="Optional",
        ),
    )

    wdp: Optional[Decimal] = Field(
        default=None,
        description="Water Depletion Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential",
            field_code="wdp",
            description="Water Depletion Potential.",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    pere: Optional[Decimal] = Field(
        default=None,
        description="Primary Energy Renewable (Energy resources).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources)",
            field_code="pere",
            description="Primary Energy Renewable (Energy resources).",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre: Optional[Decimal] = Field(
        default=None,
        description="Primary Energy Non-Renewable (Energy resources).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources)",
            field_code="penre",
            description="Primary Energy Non-Renewable (Energy resources).",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert: Optional[Decimal] = Field(
        default=None,
        description="Primary Energy Renewable Total.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total",
            field_code="pert",
            description="Primary Energy Renewable Total.",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt: Optional[Decimal] = Field(
        default=None,
        description="Primary Energy Non-Renewable Total.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total",
            field_code="penrt",
            description="Primary Energy Non-Renewable Total.",
            units="MJ",
            requirements="Optional",
        ),
    )
