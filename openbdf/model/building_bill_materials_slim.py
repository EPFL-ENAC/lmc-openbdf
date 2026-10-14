from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Enum as SAEnum
from sqlmodel import Field, SQLModel

from openbdf.model.draft import make_draft_model

from .enums.buildings import AboveBelowGround
from .enums.element_classifications import OpenBDFBuildingElementClassification
from .enums.materials import MaterialDataType, MaterialEPDMatch, OpenBDFMaterialClassification
from .field_metadata import openbdf_field_metadata


class BuildingBillMaterialsSlimRecordBase(SQLModel):
    material_id: str = Field(
        max_length=200,
        description="Identifier of the bill of materials rows. The distinct material is identified by Material reference ID. "
        "Example: MAT-2. One row from the Bill of Materials and the key that the result rows connect on.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Bill of materials row ID",
            field_code="material_id",
            description="Identifier of the bill of materials rows. The distinct material is identified by Material reference ID. "
            "Example: MAT-2. One row from the Bill of Materials and the key that the result rows connect on.",
            requirements="Automatic",
            criticality="MUST",
        ),
    )

    material_ref_id: Optional[str] = Field(
        default=None,
        description="Pairing of the same material. Example: M0001. Same value for every row that pairs the same material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material reference ID",
            field_code="material_ref_id",
            description="Pairing of the same material. Example: M0001. Same value for every row that pairs the same material.",
            requirements="Automatic",
            criticality="MAY",
        ),
    )

    custom_floor_level: Optional[str] = Field(
        default=None,
        description="Storey of the building element, as labelled in the source model. Example: EG, 1.OG, UG1, as written in the source model.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Floor level (as given)",
            field_code="custom_floor_level",
            description="Storey of the building element, as labelled in the source model. Example: EG, 1.OG, UG1, as written in the source model.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    common_floor_level: Optional[int] = Field(
        default=None,
        description="Floor level on the OpenBDF convention. Example: 0 for ground, 1 for the first storey above, -1 for the first below.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Floor level (harmonised)",
            field_code="common_floor_level",
            description="Floor level on the OpenBDF convention. Example: 0 for ground, 1 for the first storey above, -1 for the first below.",
            requirements="Automatic",
            criticality="MAY",
        ),
    )

    floor_repetition: Optional[int] = Field(
        default=None,
        description="Number of identical storeys this row represents. Example: 4, when one row describes a storey that repeats four times. "
        "Quantities and results are for one storey.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Floor repetition",
            field_code="floor_repetition",
            description="Number of identical storeys this row represents. Example: 4, when one row describes a storey that repeats four times. "
            "Quantities and results are for one storey.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    common_above_below_ground: AboveBelowGround = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(AboveBelowGround),
        description="Position of the finished floor level relative to the natural or finished ground elevation. "
        "Example: Below ground for a foundation slab, Above ground for a facade.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Above/Below Ground",
            field_code="common_above_below_ground",
            description="Position of the finished floor level relative to the natural or finished ground elevation. "
            "Example: Below ground for a foundation slab, Above ground for a facade.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    bec_custom: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Hierarchical category of the custom or national building element classification.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Class",
            field_code="bec_custom",
            description="Hierarchical category of the custom or national building element classification.",
            requirements="Required",
            criticality="SHOULD",
        ),
    )

    custom_bec_description: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The Description of the custom or national element class.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Custom BEC Description",
            field_code="custom_bec_description",
            description="The Description of the custom or national element class.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    bec_openbdf: Optional[OpenBDFBuildingElementClassification] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(OpenBDFBuildingElementClassification),
        description="The highest applicable tier of the building element within the standardized openBDF framework. "
        "Example: 1.1 for foundations and piling, 2.1 for the frame.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Building Element Classification",
            field_code="bec_openbdf",
            description="The highest applicable tier of the building element within the standardized openBDF framework. "
            "Example: 1.1 for foundations and piling, 2.1 for the frame.",
            requirements="Recommended",
            criticality="SHOULD",
        ),
    )

    custom_element_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The specific, user-defined identifier for the building element. Example: the name the designer gave the element.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Element Name (or ID)",
            field_code="custom_element_name",
            description="The specific, user-defined identifier for the building element. Example: the name the designer gave the element.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    work_section: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Layer or work section of the building element to which the material belongs. "
        "Example: Screed layer of a floor build-up, insulation layer of a roof.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Work section",
            field_code="work_section",
            description="Layer or work section of the building element to which the material belongs. "
            "Example: Screed layer of a floor build-up, insulation layer of a roof.",
            requirements="Optional",
            criticality="MAY",
        ),
    )

    layer_thickness: Optional[Decimal] = Field(
        default=None,
        description="Thickness of the work section. Example: 6, in cm, for a cement screed.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Layer thickness",
            field_code="layer_thickness",
            description="Thickness of the work section. Example: 6, in cm, for a cement screed.",
            units="cm",
            requirements="Optional",
            criticality="MAY",
        ),
    )

    common_material_name: Optional[OpenBDFMaterialClassification] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(OpenBDFMaterialClassification),
        description="The corresponding material classification from the standardized openBDF taxonomy. Example: Concrete, ready-mixed.",
        schema_extra=openbdf_field_metadata(
            attribute_name="OpenBDF Material Classification",
            field_code="common_material_name",
            description="The corresponding material classification from the standardized openBDF taxonomy. Example: Concrete, ready-mixed.",
            requirements="Recommended",
            criticality="SHOULD",
        ),
    )

    custom_material_name: str = Field(
        max_length=200,
        description="Material name as built. as it appears in the model or the bill of quantities.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name (or ID)",
            field_code="custom_material_name",
            description="Material name as built. as it appears in the model or the bill of quantities.",
            requirements="Required",
            criticality="MUST",
        ),
    )

    lca_dataset_material_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The precise material declared in the Environmental Product Declaration (EPD) database used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material name in EPD dataset",
            field_code="lca_dataset_material_name",
            description="The precise material declared in the Environmental Product Declaration (EPD) database used.",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    lca_database_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the database.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD database name",
            field_code="lca_database_name",
            description="Name of the database.",
            requirements="Recommended",
            criticality="SHOULD",
        ),
    )

    lca_dataset_link: Optional[str] = Field(
        default=None,
        max_length=200,
        description="The URL of the specific Environmental Product Declaration (EPD) dataset used. "
        "Example: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=...",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material EPD Database Link",
            field_code="lca_dataset_link",
            description="The URL of the specific Environmental Product Declaration (EPD) dataset used. "
            "Example: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=...",
            requirements="Optional",
            criticality="MAY",
        ),
    )

    material_data_type: Optional[MaterialDataType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(MaterialDataType),
        description="Type of dataset in the data hierarchy.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Construction product data type",
            field_code="material_data_type",
            description="Type of dataset in the data hierarchy.",
            requirements="Automatic",
            criticality="MAY",
        ),
    )

    material_epd_match: Optional[MaterialEPDMatch] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(MaterialEPDMatch),
        description="How the declared product relates to the material built.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD representativeness",
            field_code="material_epd_match",
            description="How the declared product relates to the material built.",
            requirements="Automatic",
            criticality="MAY",
        ),
    )

    material_reference_service_life: Decimal = Field(
        description="Declared reference service life. Example: 50, in years, for a structural element; 25 for a membrane.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Reference Service Life (RSL)",
            field_code="material_reference_service_life",
            description="Declared reference service life. Example: 50, in years, for a structural element; 25 for a membrane.",
            units="years",
            requirements="Required",
            criticality="SHOULD",
        ),
    )

    maintenance_interval: Optional[Decimal] = Field(
        default=None,
        description="Interval between maintenance activities on the material. Example: 10, in years, for repainting a facade.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Maintenance interval",
            field_code="maintenance_interval",
            description="Interval between maintenance activities on the material. Example: 10, in years, for repainting a facade.",
            units="years",
            requirements="Optional",
            criticality="MAY",
        ),
    )

    repair_interval: Optional[Decimal] = Field(
        default=None,
        description="Interval between repair activities on the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Repair interval",
            field_code="repair_interval",
            description="Interval between repair activities on the material.",
            units="years",
            constraint="None",
            requirements="Optional",
            criticality="MAY",
        ),
    )

    material_quantity_m3: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (volume) of the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m3)",
            field_code="material_quantity_m3",
            description="The measured scalar amount (volume) of the material.",
            units="m3",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    material_quantity_m2: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (area) of the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m2)",
            field_code="material_quantity_m2",
            description="The measured scalar amount (area) of the material.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    material_quantity_m: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (length) of the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (m)",
            field_code="material_quantity_m",
            description="The measured scalar amount (length) of the material.",
            units="m",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    material_quantity_count: Optional[Decimal] = Field(
        default=None,
        description="The measured scalar amount (count) of the material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Quantity (count)",
            field_code="material_quantity_count",
            description="The measured scalar amount (count) of the material.",
            units="#",
            requirements="Recommended",
            criticality="MAY",
        ),
    )

    material_weight_kg: Optional[Decimal] = Field(
        default=None,
        description="The absolute physical mass of the material. Example: 184862.3. "
        "Mass is the field that makes material efficiency analysis possible, so it is never left blank.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Weight (kg)",
            field_code="material_weight_kg",
            description="The absolute physical mass of the material. Example: 184862.3. "
            "Mass is the field that makes material efficiency analysis possible, so it is never left blank.",
            units="kg",
            requirements="Required",
            criticality="SHOULD",
        ),
    )

    material_density: Optional[Decimal] = Field(
        default=None,
        description="The mass per unit volume of the material. Example: 2400, in kg/m3, for normal weight concrete.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Density",
            field_code="material_density",
            description="The mass per unit volume of the material. Example: 2400, in kg/m3, for normal weight concrete.",
            units="kg/m3",
            requirements="Required",
            criticality="SHOULD",
        ),
    )


_BuildingBillMaterialsSlimRecordBaseDraft = make_draft_model(BuildingBillMaterialsSlimRecordBase)


class BuildingBillMaterialsSlimRecordBaseDraft(_BuildingBillMaterialsSlimRecordBaseDraft):  # type: ignore[valid-type,misc]
    pass
