from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Enum as SAEnum
from sqlmodel import Field, SQLModel

from openbdf.model.ingest import make_ingest_model

from .enums.materials import DeclaredUnit, MaterialDataType, MaterialEPDMatch
from .enums.references import Reference
from .enums.requirement import Requirement
from .field_metadata import openbdf_field_metadata


class ProjectMaterialDatabaseBase(SQLModel):
    material_ref_id: str = Field(
        description="Pairing of the same material. Example: M0001. Same value for every row that pairs the same material.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material reference ID",
            field_code="material_ref_id",
            description="Pairing of the same material. Example: M0001. Same value for every row that pairs the same material.",
            constraint="max 200 characters",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    custom_material_name: str = Field(
        description="Material name as built. as it appears in the model or the bill of quantities.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Name (or ID)",
            field_code="custom_material_name",
            description="Material name as built. as it appears in the model or the bill of quantities.",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    lca_dataset_material_name: str = Field(
        description="Product declared in the EPD from the dataset used.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material name in EPD dataset",
            field_code="lca_dataset_material_name",
            description="Product declared in the EPD from the dataset used.",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    lca_database_name: str = Field(
        description="EPD database name. ",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD database name",
            field_code="lca_database_name",
            description="EPD database name. ",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.EN_15941,
        ),
    )

    declared_unit: Optional[DeclaredUnit] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(DeclaredUnit),
        description="Unit to which the declared impacts refer. Example: m3 for ready-mixed concrete, kg for reinforcing steel, m2 for a membrane.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Declared unit",
            field_code="declared_unit",
            description="Unit to which the declared impacts refer. Example: m3 for ready-mixed concrete, kg for reinforcing steel, m2 for a membrane.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15804_A2,
        ),
    )

    bom_row_count: int = Field(
        description="Number of Bill of Materials rows using this pairing. Example: 412, meaning this material appears on 412 Bill of Materials rows.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Bill of Materials Row Count",
            field_code="bom_row_count",
            description="Number of Bill of Materials rows using this pairing. Example: 412, meaning this material appears on 412 Bill of Materials rows.",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    material_mass_kg: Decimal = Field(
        description="Total mass of this pairing. Example: 4522330.6, the sum over those rows, in kilograms.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Material Mass (kg)",
            field_code="material_mass_kg",
            description="Total mass of this pairing. Example: 4522330.6, the sum over those rows, in kilograms.",
            units="kg",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    material_mass_share: Decimal = Field(
        description="Share of total inventory mass. Example: 68.8, meaning this pairing has 68.8% of the inventory mass.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Mass share",
            field_code="material_mass_share",
            description="Share of total inventory mass. Example: 68.8, meaning this pairing has 68.8% of the inventory mass.",
            units="%",
            requirements=Requirement.AUTOMATIC,
            reference=Reference.BILL_OF_MATERIALS,
        ),
    )

    material_data_type: Optional[MaterialDataType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(MaterialDataType),
        description="Type of construction product data behind the dataset. Example: project_specific for an EPD commissioned for this project; generic for an OKOBAUDAT average.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD data type",
            field_code="material_data_type",
            description="Type of construction product data behind the dataset. Example: project_specific for an EPD commissioned for this project; generic for an OKOBAUDAT average.",
            requirements=Requirement.STRONGLY_RECOMMENDED,
            reference=Reference.EU2026_52_ANNEX_III_EN15804_A2,
        ),
    )

    material_epd_match: Optional[MaterialEPDMatch] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(MaterialEPDMatch),
        description="Representativeness of the EPD against the material built. Example: same_product_group when a sectoral average covers the product.",
        schema_extra=openbdf_field_metadata(
            attribute_name="EPD representativeness",
            field_code="material_epd_match",
            description="Representativeness of the EPD against the material built. Example: same_product_group when a sectoral average covers the product.",
            requirements=Requirement.STRONGLY_RECOMMENDED,
            reference=Reference.EN_15941_2024,
        ),
    )

    assessor_note: Optional[str] = Field(
        default=None,
        description="Free note from the assessor. Example: No EPD for the sports floor.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Assessor note",
            field_code="assessor_note",
            description="Free note from the assessor. Example: No EPD for the sports floor.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.GBDI,
        ),
    )

    product_form: Optional[str] = Field(
        default=None,
        description="Form in which the product is supplied. Example: Ready-mixed, precast, sheet, roll, board, profile.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Product form or unit type",
            field_code="product_form",
            description="Form in which the product is supplied. Example: Ready-mixed, precast, sheet, roll, board, profile.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15978_2026_ISO_21930,
        ),
    )

    strength_class: Optional[str] = Field(
        default=None,
        description="Declared strength class of the concrete or grade of the structural steel. Example: C25/30 for concrete, S235 for structural steel, C24 for sawn timber.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Strength class or grade",
            field_code="strength_class",
            description="Declared strength class of the concrete or grade of the structural steel. Example: C25/30 for concrete, S235 for structural steel, C24 for sawn timber.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_206_EN_10025,
        ),
    )

    declared_strength: Optional[Decimal] = Field(
        default=None,
        description="Strength declared for the product: characteristic compressive strength for concrete, characteristic yield strength for steel, normalised mean compressive strength for masonry units. Example: 30, in MPa, the characteristic cylinder strength behind the class.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Declared strength",
            field_code="declared_strength",
            description="Strength declared for the product: characteristic compressive strength for concrete, characteristic yield strength for steel, normalised mean compressive strength for masonry units. Example: 30, in MPa, the characteristic cylinder strength behind the class.",
            units="MPa",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_206_EN_1992_1_1_EN_10025_EN_771_EN_772_1,
        ),
    )

    exposure_class: Optional[str] = Field(
        default=None,
        description="Environmental exposure class of the concrete, stated with its standard. Example: XC3 for carbonation, XD1 for chlorides. EN 206 notation.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Exposure class",
            field_code="exposure_class",
            description="Environmental exposure class of the concrete, stated with its standard. Example: XC3 for carbonation, XD1 for chlorides. EN 206 notation.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_206_ACI_318_CSA_A23_1,
        ),
    )

    cement_type: Optional[str] = Field(
        default=None,
        description="Type of cement in the product. Example: CEM II/B-S 42,5 N. EN 197-1 notation.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Cement type",
            field_code="cement_type",
            description="Type of cement in the product. Example: CEM II/B-S 42,5 N. EN 197-1 notation.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_197_1,
        ),
    )

    reinforcement_steel_grade: Optional[str] = Field(
        default=None,
        description="Grade of the reinforcing steel, as designated in the national product standard. Example: B500B.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Reinforcement steel grade",
            field_code="reinforcement_steel_grade",
            description="Grade of the reinforcing steel, as designated in the national product standard. Example: B500B.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_1992_1_1_ANNEX_C,
        ),
    )

    reinforcement_content: Optional[Decimal] = Field(
        default=None,
        description="Mass of reinforcing steel per unit volume of concrete. Example: 110, in kg of reinforcement per m3 of concrete.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Reinforcement content",
            field_code="reinforcement_content",
            description="Mass of reinforcing steel per unit volume of concrete. Example: 110, in kg of reinforcement per m3 of concrete.",
            units="kg/m3",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15978_2026_EUROCODE_2_EN_1992,
        ),
    )

    recycled_content: Optional[Decimal] = Field(
        default=None,
        description="Share by mass of recycled material in the product, pre-consumer and post-consumer. Example: 30, meaning 30% of the mass is recycled input.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Recycled content",
            field_code="recycled_content",
            description="Share by mass of recycled material in the product, pre-consumer and post-consumer. Example: 30, meaning 30% of the mass is recycled input.",
            units="%",
            requirements=Requirement.OPTIONAL,
            reference=Reference.ISO_14021_2016,
        ),
    )

    manufacturing_route: Optional[str] = Field(
        default=None,
        description="Production route of the material. Example: Electric arc furnace for steel; clinker substitution with blast furnace slag for cement.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Manufacturing route",
            field_code="manufacturing_route",
            description="Production route of the material. Example: Electric arc furnace for steel; clinker substitution with blast furnace slag for cement.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15804_A2,
        ),
    )

    thermal_conductivity: Optional[Decimal] = Field(
        default=None,
        description="Declared thermal conductivity of the material. Example: 0.035, in W/(m·K), for mineral wool.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Thermal conductivity",
            field_code="thermal_conductivity",
            description="Declared thermal conductivity of the material. Example: 0.035, in W/(m·K), for mineral wool.",
            units="W/(m·K)",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN_ISO_10456,
        ),
    )

    biogenic_carbon_content: Optional[Decimal] = Field(
        default=None,
        description="Biogenic carbon in the product as it leaves the factory gate, per declared unit. Example: 0.45, in kg of biogenic carbon per declared unit of sawn timber.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Biogenic carbon content",
            field_code="biogenic_carbon_content",
            description="Biogenic carbon in the product as it leaves the factory gate, per declared unit. Example: 0.45, in kg of biogenic carbon per declared unit of sawn timber.",
            units="kg C per declared unit",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15804_A2_EN_16449,
        ),
    )

    end_of_life_scenario: Optional[str] = Field(
        default=None,
        description="End-of-life route of the material. Example: Concrete crushed and used as aggregate, C3 recycling with 5 per cent to landfill in C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="End-of-life scenario",
            field_code="end_of_life_scenario",
            description="End-of-life route of the material. Example: Concrete crushed and used as aggregate, C3 recycling with 5 per cent to landfill in C4.",
            requirements=Requirement.OPTIONAL,
            reference=Reference.EN15978_2026,
        ),
    )


_ProjectMaterialDatabaseBaseIngest = make_ingest_model(ProjectMaterialDatabaseBase)


class ProjectMaterialDatabaseBaseIngest(_ProjectMaterialDatabaseBaseIngest):  # type: ignore[valid-type,misc]
    pass
