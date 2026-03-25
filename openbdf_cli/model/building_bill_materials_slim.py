from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Column, Field, Integer, Numeric, Relationship, SQLModel, String
from sqlmodel import Enum as SAEnum

# Assuming these enums exist based on the CSV "Categorical (Predefined)" status
from .enums.buildings import AboveBelowGround
from .enums.element_classifications import OpenBDFBuildingElementClassification
from .enums.materials import OpenBDFMaterialClassification
from .field_metadata import openbdf_field_metadata
from .general_info import ProjectRecord


class BuildingBillMaterialsSlimRecordBase(SQLModel):
    floor_level: int = Field(
        sa_column=Column(Integer),
        description="Storey of the building element.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Floor level",
            field_code="floor_level",
            description="Storey of the building element.",
            requirements="Required",
        ),
    )

    above_below_ground: AboveBelowGround = Field(
        sa_column=Column(SAEnum(AboveBelowGround)),
        description="Position of the finished floor level relative to the natural or finished ground elevation.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Above/Below Ground",
            field_code="above_below_ground",
            description="Position of the finished floor level relative to the natural or finished ground elevation.",
            units="none",
            requirements="Required",
        ),
    )

    bec_custom_tier1: str = Field(
        sa_column=Column(String(200)),
        description="Primary (top-level) hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 1)",
            field_code="bec_custom_tier1",
            description="Primary (top-level) hierarchical category of the custom or national building element classification.",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
        ),
    )

    bec_custom_tier2: str = Field(
        sa_column=Column(String(200)),
        description="Secondary hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 2)",
            field_code="bec_custom_tier2",
            description="Secondary hierarchical category of the custom or national building element classification.",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
        ),
    )

    bec_custom_tier3: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The tertiary hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 3)",
            field_code="bec_custom_tier3",
            description="The tertiary hierarchical category of the custom or national building element classification.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
        ),
    )

    bec_custom_tier4: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The quaternary (lowest-level) hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class (Tier 4)",
            field_code="bec_custom_tier4",
            description="The quaternary (lowest-level) hierarchical category of the custom or national building element classification.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
        ),
    )

    bec_custom_description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The Description of the custom or national element class.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class Description",
            field_code="bec_custom_description",
            description="The Description of the custom or national element class.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
        ),
    )

    bec_openbdf_selection: Optional[OpenBDFBuildingElementClassification] = Field(
        default=None,
        sa_column=Column(SAEnum(OpenBDFBuildingElementClassification), nullable=True),
        description="The highest applicable tier of the building element within the standardized openBDF framework.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Building Element Classification",
            field_code="bec_openbdf_selection",
            description="The highest applicable tier of the building element within the standardized openBDF framework.",
            units="none",
            requirements="Recommended",
        ),
    )

    element_name_custom: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The specific, user-defined identifier for the building element.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Name (or ID)",
            field_code="element_name_custom",
            description="The specific, user-defined identifier for the building element.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
        ),
    )

    openbdf_material_name: Optional[OpenBDFMaterialClassification] = Field(
        default=None,
        sa_column=Column(SAEnum(OpenBDFMaterialClassification), nullable=True),
        description="The corresponding material classification from the standardized openBDF taxonomy.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Common Material Classification",
            field_code="openbdf_material_name",
            description="The corresponding material classification from the standardized openBDF taxonomy.",
            units="none",
            requirements="Optional",
        ),
    )

    material_name_custom: str = Field(
        sa_column=Column(String(200)),
        description="The specific, user-defined identifier for the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name (or ID)",
            field_code="material_name_custom",
            description="The specific, user-defined identifier for the material.",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
        ),
    )

    material_name_database: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The precise material designation as cataloged in the associated Environmental Product Declaration (EPD) database.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name from EPD database",
            field_code="material_name_database",
            description="The precise material designation as cataloged in the associated Environmental Product Declaration (EPD) database.",
            constraint="dropdown",
            units="none",
            requirements="Recommended",
        ),
    )

    lca_dataset_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The nomenclature of the specific Environmental Product Declaration (EPD) dataset used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD Database Name",
            field_code="lca_dataset",
            description="The nomenclature of the specific Environmental Product Declaration (EPD) dataset used.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
        ),
    )

    lca_dataset_link: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="The URL of the specific Environmental Product Declaration (EPD) dataset used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD Database Link",
            field_code="lca_dataset",
            description="The URL of the specific Environmental Product Declaration (EPD) dataset used.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
        ),
    )

    custom_material_quantity_m3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The measured scalar amount (volume) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m3)",
            field_code="custom_material_quantity_m3",
            description="The measured scalar amount (volume) of the custom material.",
            constraint="numerical",
            units="#",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_m2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The measured scalar amount (area) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m2)",
            field_code="custom_material_quantity_m2",
            description="The measured scalar amount (area) of the custom material.",
            constraint="numerical",
            units="#",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_m: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The measured scalar amount (length) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m)",
            field_code="custom_material_quantity_m",
            description="The measured scalar amount (length) of the custom material.",
            constraint="numerical",
            units="#",
            requirements="Recommended",
        ),
    )

    custom_material_quantity_count: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The measured scalar amount (count) of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (count)",
            field_code="custom_material_quantity_count",
            description="The measured scalar amount (count) of the custom material.",
            constraint="numerical",
            units="#",
            requirements="Recommended",
        ),
    )

    custom_material_weight_kg: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The absolute physical mass of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Weight (kg)",
            field_code="custom_material_weight_kg",
            description="The absolute physical mass of the custom material.",
            constraint="numerical",
            units="kg",
            requirements="Required",
        ),
    )

    custom_material_density: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="The mass per unit volume of the custom material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Density",
            field_code="custom_material_density",
            description="The mass per unit volume of the custom material.",
            constraint="numerical",
            units="kg/m3",
            requirements="Recommended",
        ),
    )


class BuildingBillMaterialsSlimRecord(BuildingBillMaterialsSlimRecordBase, table=True):
    __tablename__ = "building_bill_materials_slim_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_id: int = Field(foreign_key="project_record.id", nullable=False)

    # Linking back to the Project model
    project: Optional["ProjectRecord"] = Relationship(back_populates="bill_of_materials")
