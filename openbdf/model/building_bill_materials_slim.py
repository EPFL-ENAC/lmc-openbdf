from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Enum as SAEnum
from sqlmodel import Field, SQLModel

from openbdf.model.draft import make_draft_model

from .enums.buildings import AboveBelowGround
from .enums.element_classifications import OpenBDFBuildingElementClassification
from .enums.materials import OpenBDFMaterialClassification
from .field_metadata import openbdf_field_metadata


class BuildingBillMaterialsSlimRecordBase(SQLModel):
    material_id: str = Field(
        max_length=200,
        description="The unique identifier for the material within the project context.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material ID",
            field_code="material_id",
            description="The unique identifier for the material within the project context.",
        ),
    )

    floor_level: Optional[int] = Field(
        default=None,
        description="Storey of the building element.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Floor level",
            field_code="floor_level",
            description="Storey of the building element.",
            requirements="Recommended",
        ),
    )

    above_below_ground: AboveBelowGround = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(AboveBelowGround),
        description="Position of the finished floor level relative to the natural or finished ground elevation.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Above/Below Ground",
            field_code="above_below_ground",
            description="Position of the finished floor level relative to the natural or finished ground elevation.",
            requirements="Required",
        ),
    )

    bec_custom_tier1: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Primary (top-level) hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 1)",
            field_code="bec_custom_tier1",
            description="Primary (top-level) hierarchical category of the custom or national building element classification.",
            requirements="Recommended",
        ),
    )

    bec_custom_tier2: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Secondary hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 2)",
            field_code="bec_custom_tier2",
            description="Secondary hierarchical category of the custom or national building element classification.",
            requirements="Recommended",
        ),
    )

    bec_custom_tier3: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The tertiary hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 3)",
            field_code="bec_custom_tier3",
            description="The tertiary hierarchical category of the custom or national building element classification.",
            requirements="Recommended",
        ),
    )

    bec_custom_tier4: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The quaternary (lowest-level) hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 4)",
            field_code="bec_custom_tier4",
            description="The quaternary (lowest-level) hierarchical category of the custom or national building element classification.",
            requirements="Optional",
        ),
    )

    bec_custom_description: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The Description of the custom or national element class.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class Description",
            field_code="bec_custom_description",
            description="The Description of the custom or national element class.",
            requirements="Recommended",
        ),
    )

    bec_openbdf_selection: Optional[OpenBDFBuildingElementClassification] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(OpenBDFBuildingElementClassification),
        description="The highest applicable tier of the building element within the standardized openBDF framework.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Building Element Classification",
            field_code="bec_openbdf_selection",
            description="The highest applicable tier of the building element within the standardized openBDF framework.",
            requirements="Recommended",
        ),
    )

    element_name_custom: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The specific, user-defined identifier for the building element.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Name (or ID)",
            field_code="element_name_custom",
            description="The specific, user-defined identifier for the building element.",
            requirements="Recommended",
        ),
    )

    openbdf_material_name: Optional[OpenBDFMaterialClassification] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(OpenBDFMaterialClassification),
        description="The corresponding material classification from the standardized openBDF taxonomy.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Common Material Classification",
            field_code="openbdf_material_name",
            description="The corresponding material classification from the standardized openBDF taxonomy.",
            requirements="Optional",
        ),
    )

    material_name_custom: str = Field(
        max_length=200,
        description="The specific, user-defined identifier for the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name (or ID)",
            field_code="material_name_custom",
            description="The specific, user-defined identifier for the material.",
            requirements="Required",
        ),
    )

    material_name_database: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The precise material designation as cataloged in the associated Environmental Product Declaration (EPD) database.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name from EPD database",
            field_code="material_name_database",
            description="The precise material designation as cataloged in the associated Environmental Product Declaration (EPD) database.",
            requirements="Recommended",
        ),
    )

    lca_dataset_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The nomenclature of the specific Environmental Product Declaration (EPD) dataset used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material EPD Database Name",
            field_code="lca_dataset_name",
            description="The nomenclature of the specific Environmental Product Declaration (EPD) dataset used.",
            requirements="Recommended",
        ),
    )

    lca_dataset_link: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The URL of the specific Environmental Product Declaration (EPD) dataset used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material EPD Database Link",
            field_code="lca_dataset_link",
            description="The URL of the specific Environmental Product Declaration (EPD) dataset used.",
            requirements="Optional",
        ),
    )

    custom_material_quantity_m3: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (volume) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m3)",
            field_code="custom_material_quantity_m3",
            description="The measured scalar amount (volume) of the custom material.",
            units="m3",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_m2: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (area) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m2)",
            field_code="custom_material_quantity_m2",
            description="The measured scalar amount (area) of the custom material.",
            units="m2",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_m: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (length) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m)",
            field_code="custom_material_quantity_m",
            description="The measured scalar amount (length) of the custom material.",
            units="m",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_count: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (count) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (count)",
            field_code="custom_material_quantity_count",
            description="The measured scalar amount (count) of the custom material.",
            units="#",
            requirements="Recommended",
        ),
    )

    custom_material_weight_kg: Optional[Decimal] = Field(
        default=None,
        description="The absolute physical mass of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Weight (kg)",
            field_code="custom_material_weight_kg",
            description="The absolute physical mass of the custom material.",
            units="kg",
            requirements="Required",
        ),
    )

    custom_material_density: Optional[Decimal] = Field(
        default=None,
        description="The mass per unit volume of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Density",
            field_code="custom_material_density",
            description="The mass per unit volume of the custom material.",
            units="kg/m3",
            requirements="Recommended",
        ),
    )


BuildingBillMaterialsSlimRecordBaseDraft = make_draft_model(BuildingBillMaterialsSlimRecordBase)
