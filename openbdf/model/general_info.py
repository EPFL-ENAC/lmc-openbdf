from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import JSON, Column, Date, Integer, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

from .enums.buildings import (
    BuildingFacingDirection,
    BuildingTypology,
    FoundationType,
    GFAMeasurementMethod,
    GrossFloorAreaStandard,
)
from .enums.countries import Country
from .enums.energy import BuildingEnergyClassificationSystem, PrimaryEnergySource
from .enums.geography import ASHRAEClimateZone, FEMASeismicActivity, SoilType
from .enums.lca import (
    BiogenicCarbonAccounting,
    LCAModel,
    LCATemporalApproach,
    LCIAMethodology,
    LifeCycleStage_ISO14040_44,
)
from .enums.materials import MaterialQuantitiesSource
from .enums.project import ConstructionType, ProjectPhase, ProjectUnits
from .field_metadata import openbdf_field_metadata

if TYPE_CHECKING:
    from .building_bill_materials_slim import BuildingBillMaterialsSlimRecord


class ProjectRecordBase(SQLModel):
    project_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Unique ID assigned to this specific project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project ID",
            field_code="project_id",
            description="Unique ID assigned to this specific project.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            reference_formats={"echo": True, "carbenmats": True, "clf": False},
            example="ABC1234",
        ),
    )

    project_units: ProjectUnits = Field(
        sa_column=Column(SAEnum(ProjectUnits)),
        description="Unit system used in the assessment.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project Unit System",
            field_code="project_units",
            description=(
                "Unit system used in the assessment (Imperial Units System (IP, USA); International Units System (SI))."
            ),
            units="none",
            requirements="Required",
            example="Metric, International Units System (SI)",
        ),
    )

    project_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project name",
            field_code="project_name",
            description="Name of the project (can be anonymized).",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            reference_formats={"echo": True, "carbenmats": False, "clf": True},
            example="Brilliant Group Hotel",
        ),
    )

    project_description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(500), nullable=True),
        description="General description of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project description",
            field_code="project_description",
            description=("A general description of the project focusing on its use, function, and extent of work."),
            constraint="string < 500 characters",
            units="none",
            requirements="Optional",
            reference_formats={"echo": False, "carbenmats": False, "clf": True},
            example="A new hotel on the harbour",
        ),
    )

    project_construction_type: ConstructionType = Field(
        sa_column=Column(SAEnum(ConstructionType)),
        description="Construction type of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project construction type",
            field_code="project_construction_type",
            description="New construction, Minor renovation, Major renovation",
            units="none",
            requirements="Required",
            example="New construction",
        ),
    )

    project_country: Country = Field(
        sa_column=Column(SAEnum(Country)),
        description="Country where the project is located.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Country",
            field_code="project_country",
            description="Country where the project is located.",
            units="none",
            requirements="Required",
            example="Afghanistan",
        ),
    )

    project_city: str = Field(
        sa_column=Column(String(200)),
        description="City where the project is located.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="City",
            field_code="project_city",
            description="City where the project is located.",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
            example="Potsdam",
        ),
    )

    project_state: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="State, province, or country subdivision.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="State",
            field_code="project_state",
            description=("State, province, or country subdivision where the project is located."),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="Brandenburg",
        ),
    )

    project_address: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Address of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Address",
            field_code="project_address",
            description="Address of the project.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="Voorstrasse 20, 1417 Potsdam",
        ),
    )

    project_owner_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Individual or entity that owns the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Owner / Client name",
            field_code="project_owner_name",
            description="Individual or entity that owns the project.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Mr. Brown Alter",
        ),
    )

    project_date_assessment: date = Field(
        sa_column=Column(Date),
        description="Date of the life-cycle assessment conducted by the assessor.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Date of assessment",
            field_code="project_date_assessment",
            description=("Date of the life-cycle assessment conducted by the assessor."),
            constraint="ISO date",
            units="#",
            requirements="Required",
            example="11/02/2026",
        ),
    )

    project_third_verified: Optional[bool] = Field(
        default=None,
        description="Whether the project LCA is verified by a third party.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Third party verified",
            field_code="project_third_verified",
            description="Is the project LCA verified by a third-party?",
            constraint="boolean",
            units="none",
            requirements="Recommended",
            example="Yes",
        ),
    )

    project_third_verifier_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the third-party verifier.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Third party verifier name",
            field_code="project_third_verifier_name",
            description=("Name of the third-party verification person/organisation."),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="Pullmann Consultants, Zurich",
        ),
    )

    project_verification_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="Date of third-party verification.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Verification date",
            field_code="project_verification_date",
            description="Date of the verification of the assessment by third-party.",
            constraint="ISO date",
            units="#",
            requirements="Optional",
            example="07/02/2026",
        ),
    )

    project_gfa_method: Optional[GFAMeasurementMethod] = Field(
        default=None,
        sa_column=Column(SAEnum(GFAMeasurementMethod), nullable=True),
        description="Gross Floor Area measurement method.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="GFA measurement method",
            field_code="project_gfa_method",
            description=("Gross Floor Area measurement method applied to the project (e.g., ASHRAE, LEED, IPMS)"),
            units="none",
            requirements="Recommended",
            example="IPMS – International Property Measurement Standards",
        ),
    )

    project_certification: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Sustainability certification applied for the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Certification",
            field_code="project_certification",
            description=("Type of sustainability certification being applied for the project."),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="LEED",
        ),
    )

    project_certification_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="Date of certification application.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Certification application date",
            field_code="project_certification_date",
            description=("Date of application for the sustainability certification for the project."),
            constraint="ISO date",
            units="#",
            requirements="Recommended",
            example="08/02/2026",
        ),
    )

    project_certification_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Unique ID assigned to the certification application.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Certification application ID",
            field_code="project_certification_id",
            description="Unique ID assigned to the certification application.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="ABC1234",
        ),
    )

    project_permit_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="Date of application for construction permit.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project permit application date",
            field_code="project_permit_date",
            description="Date of application for construction permit.",
            constraint="ISO date",
            units="none",
            requirements="Recommended",
            example="08/02/2026",
        ),
    )

    project_permit_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Unique ID of the project permit.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project permit ID",
            field_code="project_permit_id",
            description="Unique ID of the project permit.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="ABC1234",
        ),
    )

    project_plot_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total plot area of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project total plot area",
            field_code="project_plot_area",
            description=("Total plot area of the project according to national standard."),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="500",
        ),
    )

    project_no_of_buildings: int = Field(
        description="Total number of buildings in the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="No. of buildings",
            field_code="project_no_of_buildings",
            description="Total number of buildings in the project.",
            constraint="numerical",
            units="#",
            requirements="Required",
            example="5",
        ),
    )

    project_phase: ProjectPhase = Field(
        sa_column=Column(SAEnum(ProjectPhase)),
        description="Stage of the project when LCA is conducted.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project phase",
            field_code="project_phase",
            description=("Stage of the project when LCA is conducted (according to national standard)"),
            units="none",
            requirements="Required",
            example="Preliminary studies",
        ),
    )

    project_start_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="Project design start date.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project design start date",
            field_code="project_start_date",
            description="Project design start date.",
            constraint="ISO date",
            units="#",
            requirements="Recommended",
            example="08/02/2026",
        ),
    )

    project_construction_company_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the company constructing the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Construction company name",
            field_code="project_construction_company_name",
            description="Name of the company constructing the project.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Terranova Construction Company",
        ),
    )

    project_construction_company_address: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Physical location of the construction company.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Construction company address",
            field_code="project_construction_company_address",
            description="Physical location of the construction company.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Seebachstrasse 21, 5100 Zurich",
        ),
    )

    project_contractor_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the contractor executing the construction.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Contractor name",
            field_code="project_contractor_name",
            description="Name of the contractor executing the construction.",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Regionale Contractors",
        ),
    )

    project_architect_engineer_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the architect/engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Architect/ Engineer",
            field_code="project_architect_engineer_name",
            description=("Name of the architect/engineer appointed on the project"),
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Peter Sylon",
        ),
    )

    project_structural_engineer_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the structural engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Structural Engineer",
            field_code="project_structural_engineer_name",
            description="Name of the engineer appointed on the project",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Peter Sylon",
        ),
    )

    project_mep_engineer_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the MEP engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="MEP Engineer",
            field_code="project_mep_engineer_name",
            description="Name of the MEP Engineer appointed on the project",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Peter Sylon",
        ),
    )

    project_environmental_consultant_company: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Company conducting the LCA assessment.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Environmental consultant company",
            field_code="project_environmental_consultant_company",
            description="Name of the company conducting the LCA assessment",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Environmental Design Consultants",
        ),
    )

    project_assessor_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Name of the environmental assessor.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Environmental assessor name",
            field_code="project_assessor_name",
            description="Name of the environmental assessor",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="Thomas Casper",
        ),
    )

    project_assessor_contact: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Contact details of the environmental assessor.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Project Stakeholders",
            attribute_name="Environmental assessor contact",
            field_code="project_assessor_contact",
            description=("Contact details of the Environmental assessor (e.g. email, phone)"),
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="email or phone number",
        ),
    )

    building_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Assigned identifier for the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building ID",
            field_code="building_id",
            description="Assigned identifier for the building renovated/constructed.",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="ABC1234",
        ),
    )

    # TODO : datatype for this ?
    building_gps_coordinates: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True),
        description="Latitude and longitude of the building project.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building GPS coordinates",
            field_code="building_gps_coordinates",
            description=("Latitude and longitude of the building project (decimal degrees)"),
            constraint="numerical",
            units="#",
            requirements="Recommended",
            example="41.40338, 2.17403",
        ),
    )

    building_geographic_climate_zone: Optional[ASHRAEClimateZone] = Field(
        default=None,
        sa_column=Column(SAEnum(ASHRAEClimateZone), nullable=True),
        description="ASHRAE climate zone typology.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="ASHRAE climate zone typologies",
            field_code="building_geographic_climate_zone",
            description=("Classification of the area's climate based on ASHRAE classification"),
            units="none",
            requirements="Recommended",
            example="2A (Hot - Humid)",
        ),
    )

    building_altitude: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Elevation of the project site above sea level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Altitude",
            field_code="building_altitude",
            description="Elevation of the project site above sea level",
            constraint="numerical",
            units="m",
            requirements="Recommended",
            example="200m or 400 ft.",
        ),
    )

    building_seismic_zone: Optional[FEMASeismicActivity] = Field(
        default=None,
        sa_column=Column(SAEnum(FEMASeismicActivity), nullable=True),
        description="Classification of seismic activity level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Seismic zone",
            field_code="building_seismic_zone",
            description=("Classification of the area's seismic activity level according to national standard"),
            units="none",
            requirements="Recommended",
            example="SDC A: Minor expected ground shaking.",
        ),
    )

    building_typology: BuildingTypology = Field(
        sa_column=Column(SAEnum(BuildingTypology)),
        description="Building category according to national classification.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building typology",
            field_code="building_typology",
            description=(
                "Building category according to national classification "
                "(multi-family housing, single-family home etc.)."
            ),
            units="none",
            requirements="Required",
            example="Multi-family buildings",
        ),
    )

    building_residential_units: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="Total number of individual residential units.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of individual residential units",
            field_code="building_residential_units",
            description=("Total number of individual residential units within the building (if residential asset)."),
            units="none",
            requirements="Recommended",
            example="25",
        ),
    )

    building_rooms: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total number of rooms in residential units.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of rooms in the residential units",
            field_code="building_rooms",
            description="Total number of rooms (if residential asset).",
            constraint="numerical",
            units="#",
            requirements="Optional",
            example="100",
        ),
    )

    building_energy_classification_system: Optional[BuildingEnergyClassificationSystem] = Field(
        default=None,
        sa_column=Column(SAEnum(BuildingEnergyClassificationSystem), nullable=True),
        description="Energy classification of the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Energy classification",
            field_code="building_energy_classification_system",
            description=(
                "Energy classifications to assess the building's energy "
                "performance (e.g., EPC, SAP Rating, HERS Index, ENERGY STAR, "
                "A++, ...)."
            ),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="A, B, A+",
        ),
    )

    building_construction_start_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="The year/date building construction officially started.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Construction start date",
            field_code="building_construction_start_date",
            description=("The year the building construction officially started."),
            constraint="ISO date",
            units="#",
            requirements="Optional",
            example="07/02/2026",
        ),
    )

    building_construction_end_date: date = Field(
        sa_column=Column(Date),
        description="The year/date building construction completed.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Construction end date",
            field_code="building_construction_end_date",
            description=("The year the building construction was officially completed and started operating."),
            constraint="ISO date",
            units="#",
            requirements="Required",
            example="07/02/2026",
        ),
    )

    building_demolished_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Floor area dismantled or destroyed in end-of-life phase.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Demolished area",
            field_code="building_demolished_area",
            description=("Floor area that has been dismantled or destroyed as a part of end-of-life phase."),
            constraint="numerical",
            units="m2",
            requirements="Optional",
            example="500",
        ),
    )

    building_roof_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total roof surface area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Roof area",
            field_code="building_roof_area",
            description="The total surface area covered by the roof of a building",
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="500",
        ),
    )

    building_floors_bg: Decimal = Field(
        sa_column=Column(Numeric(10, 2)),
        description="Number of floor levels below ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of floors (below ground)",
            field_code="building_floors_bg",
            description=("Number of floor levels situated below the ground level"),
            constraint="numerical",
            units="#",
            requirements="Required",
            example="2",
        ),
    )

    building_floors_ag: Decimal = Field(
        sa_column=Column(Numeric(10, 2)),
        description="Number of floor levels above ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of floors (above ground)",
            field_code="building_floors_ag",
            description=("Number of floor levels situated above the ground level"),
            constraint="numerical",
            units="#",
            requirements="Required",
            example="3",
        ),
    )

    building_parking_building: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(10, 2), nullable=True),
        description="Parking spots included in the building perimeter.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of parking spots (in building)",
            field_code="building_parking_building",
            description=("Total number of parking spots included in the building perimeter (e.g. in the basement)"),
            constraint="numerical",
            units="#",
            requirements="Recommended",
            example="5",
        ),
    )

    building_parking_dislocated: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(10, 2), nullable=True),
        description="Parking spots dislocated from the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of parking spots (dislocated)",
            field_code="building_parking_dislocated",
            description=("Total number of parking spot dislocated from the building (on-site, off-site)"),
            constraint="numerical",
            units="#",
            requirements="Recommended",
            example="6",
        ),
    )

    building_structure_type: str = Field(
        sa_column=Column(String(100)),
        description="Overall design and construction method of a building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building structure type",
            field_code="building_structure_type",
            description=("Overall design and construction method of a building- Massive, Timber, Other"),
            constraint="dropdown",
            units="none",
            requirements="Required",
            example="Concrete (In-Situ)",
        ),
    )

    building_prefabricated_elements: Optional[bool] = Field(
        default=None,
        description="Whether prefabricated elements are used.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Prefabricated elements",
            field_code="building_prefabricated_elements",
            description=(
                "Building components manufactured off-site in a factory "
                "setting and transported to the construction site for assembly, "
                "including panels, modules, and sections"
            ),
            units="none",
            requirements="Recommended",
            example="Yes",
        ),
    )

    building_soil_data: Optional[SoilType] = Field(
        default=None,
        sa_column=Column(SAEnum(SoilType), nullable=True),
        description="Information about the category of soil.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Soil data",
            field_code="building_soil_data",
            description=("Information about the catregory of soil (according to national standard)"),
            units="none",
            requirements="Recommended",
            example="sandy gravel",
        ),
    )

    building_foundation_type: FoundationType = Field(
        sa_column=Column(SAEnum(FoundationType)),
        description="Construction method used to support a building below ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Foundation type",
            field_code="building_foundation_type",
            description=(
                "Construction method used to support a building's structure "
                "below ground, such as Strip, Raft, Pile or basement foundation"
            ),
            units=None,
            requirements="Required",
            example="Spread foundation- Pad Footings (Isolated)",
        ),
    )

    building_energy_demand_thermal: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Energy demand for thermal space services.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy demand - thermal",
            field_code="building_energy_demand_thermal",
            description=("Energy demand for space (e.g., heating /cooling, domestic hot water - DHW)."),
            constraint="numerical",
            units="kWh/y",
            requirements="Recommended",
            example="100",
        ),
    )

    building_energy_demand_electricity: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Energy demand for electrical equipment.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy demand - electric",
            field_code="building_energy_demand_electricity",
            description=("Energy demand for electrical equipment (lighting, ventilation, etc.)."),
            constraint="numerical",
            units="kWh/y",
            requirements="Recommended",
            example="101",
        ),
    )

    building_energy_supply_thermal: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Energy supply from local thermal RES.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy supply - thermal",
            field_code="building_energy_supply_thermal",
            description="Energy supply from local thermal RES (e.g., PV, etc.).",
            constraint="numerical",
            units="kWh/y",
            requirements="Recommended",
            example="102",
        ),
    )

    building_energy_supply_electricity: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Energy supply from local electrical RES.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy supply - electric",
            field_code="building_energy_supply_electricity",
            description=("Energy supply from local electrical RES (e.g., solar panel, etc.)."),
            constraint="numerical",
            units="kWh/y",
            requirements="Recommended",
            example="103",
        ),
    )

    building_primary_energy_source: Optional[PrimaryEnergySource] = Field(
        default=None,
        sa_column=Column(SAEnum(PrimaryEnergySource), nullable=True),
        description="Primary energy source for heating/cooling/DHW.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building primary energy source",
            field_code="building_primary_energy_source",
            description="Primary energy source for heating/ cooling, DHW.",
            units="none",
            requirements="Recommended",
            example="Coal",
        ),
    )

    building_bipv_description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(500), nullable=True),
        description="Type and scope of BIPV.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building BIPV description",
            field_code="building_bipv_description",
            description=(
                "Type and scope of BIPV (building integrated PV). If present, "
                "mentioning, e.g., area (m²) and power (kWpeak) as well as "
                "specific type of the system."
            ),
            constraint="string < 500 characters",
            units="none",
            requirements="Optional",
        ),
    )

    building_orientation: Optional[BuildingFacingDirection] = Field(
        default=None,
        sa_column=Column(SAEnum(BuildingFacingDirection), nullable=True),
        description="Orientation of the main façade.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building orientation",
            field_code="building_orientation",
            description="Building orientation of the 'main' façade",
            units="none",
            requirements="Recommended",
            example="E = East-facing",
        ),
    )

    building_footprint: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Area covered by the building on the plot.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building footprint area",
            field_code="building_footprint",
            description=(
                "Building footprint, i.e. the area covered by the building on "
                "the plot. Considered equivalent to projected roof area."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="500",
        ),
    )

    building_unconditioned_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Floor area within the building that is not conditioned.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Unconditioned floor area",
            field_code="building_unconditioned_area",
            description=(
                "The floor area within the building that is not conditioned. "
                "Spaces that are not actively managed for temperature, humidity, "
                "and air quality using HVAC systems."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="501",
        ),
    )

    building_conditioned_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Area used to calculate building zone energy performance.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Conditioned floor area",
            field_code="building_conditioned_area",
            description=(
                "The area used to calculate a building zone energy performance "
                "(sum of all enclosed, heated/cooled floor areas of a building "
                "where the ambient temperature is maintained above 12°C)."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="502",
        ),
    )

    building_useful_floor_area: Decimal = Field(
        sa_column=Column(Numeric(18, 4)),
        description="Total area intended for primary use of the building zone.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Useful floor area (UFA)",
            field_code="building_useful_floor_area",
            description=(
                "Total area intended for primary use of the building zone "
                "including living rooms, bedrooms, offices, classrooms, "
                "retail spaces."
            ),
            constraint="numerical",
            units="m2",
            requirements="Required",
            example="503",
        ),
    )

    building_gross_floor_area: Decimal = Field(
        sa_column=Column(Numeric(18, 4)),
        description="Total gross floor area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Gross floor area (GFA)",
            field_code="building_gross_floor_area",
            description=(
                "Total gross floor area based on the external perimeter of the "
                "building geometry, including the area all structural and "
                "non-structural elements."
            ),
            constraint="numerical",
            units="m2",
            requirements="Required",
            example="504",
        ),
    )

    building_gross_floor_area_definition: GrossFloorAreaStandard = Field(
        sa_column=Column(SAEnum(GrossFloorAreaStandard)),
        description="Definition of GFA according to national standards.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Gross floor area (GFA) Definition",
            field_code="building_gross_floor_area_definition",
            description="Definition according to national standards",
            units="none",
            requirements="Required",
            example="RICS (UK), Type 2: GIA (Gross Internal Area)",
        ),
    )

    building_circulation_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total circulation area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Circulation area",
            field_code="building_circulation_area",
            description=(
                "Total area used for the movement within the building zone "
                "including hallway, staircases, elevators and lobbies."
            ),
            constraint="numerical",
            units="m2",
            requirements="Optional",
            example="500",
        ),
    )

    building_technical_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total area reserved for building services and equipment.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Technical area",
            field_code="building_technical_area",
            description=(
                "Total area reserved for building zone services and technical "
                "equipment including boiler rooms, electrical rooms, HVAC etc."
            ),
            constraint="numerical",
            units="m2",
            requirements="Optional",
            example="501",
        ),
    )

    building_built_floor_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="GFA plus parking area located inside the building shell.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Built floor area (BFA)",
            field_code="building_built_floor_area",
            description=(
                "Equals the gross floor area plus parking area located inside "
                "the building shell/enclosed attached parking."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="502",
        ),
    )

    building_envelope_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total area of the building envelope.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building envelope area",
            field_code="building_envelope_area",
            description="Total area of the building envelope (facade and roof).",
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="503",
        ),
    )

    building_window_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Combined surface area of all windows.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Window area",
            field_code="building_window_area",
            description="The combined surface area of all windows in a building.",
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="504",
        ),
    )

    building_wall_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total surface area of internal walls.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Wall area (interior)",
            field_code="building_wall_area",
            description=(
                "The total surface area of internal walls within a building, excluding openings like doors and windows."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="505",
        ),
    )

    building_enclosed_parking_area: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Parking area enclosed and/or attached to the building shell.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Enclosed parking area",
            field_code="building_enclosed_parking_area",
            description=(
                "Parking area that is enclosed and/or attached to the building "
                "shell. This measurement excludes surface parking lots or "
                "parking structures that are entirely separate from the building."
            ),
            constraint="numerical",
            units="m2",
            requirements="Recommended",
            example="506",
        ),
    )

    building_height: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Total height of the building above finished ground level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building height",
            field_code="building_height",
            description="Total height of the building above finished ground level.",
            constraint="numerical",
            units="m",
            requirements="Recommended",
            example="20",
        ),
    )

    building_floor_height: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Average vertical distance between finished floors.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Average floor height",
            field_code="building_floor_height",
            description=(
                "Vertical distance between the upper surface of one finished "
                "floor and the upper surface of the finished floor above it."
            ),
            constraint="numerical",
            units="m",
            requirements="Recommended",
            example="3",
        ),
    )

    building_volume: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(18, 4), nullable=True),
        description="Gross building volume.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building volume",
            field_code="building_volume",
            description=(
                "Volume of the building (gross building volume), i.e. the total "
                "space enclosed incl. volume of walls, roofs."
            ),
            constraint="numerical",
            units="m3",
            requirements="Recommended",
            example="50",
        ),
    )

    building_occupancy_count: Decimal = Field(
        sa_column=Column(Numeric(18, 4)),
        description="Estimated occupancy count.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Occupancy count",
            field_code="building_occupancy_count",
            description=(
                "Estimated number of people that a building or space can "
                "accommodate (residential: number of beds; office: number of "
                "work places/desks)."
            ),
            constraint="numerical",
            units="#",
            requirements="Required",
            example="10",
        ),
    )

    lca_goal: str = Field(
        description="Goal of the study.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="Goal & Scope",
            attribute_name="LCA goal",
            field_code="lca_goal",
            description="Goal of the study",
            requirements="Required",
            example="Permission from municipal corporation",
        ),
    )

    lca_reference_unit: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Reference unit the results are primarily expressed for.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="Goal & Scope",
            attribute_name="Reference Unit",
            field_code="lca_reference_unit",
            description=("Reference unit the results are primary expressed for, as stated in source"),
            requirements="Required",
        ),
    )

    lca_required_service_life: str = Field(
        sa_column=Column(String(200)),
        description="Duration over which the environmental impacts of a building are assessed, typically ranging from 50 to 100 years.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="Goal & Scope",
            attribute_name="Required Service Life",
            field_code="lca_required_service_life",
            description=(
                "Duration over which the environmental impacts of a building are assessed, typically ranging from 50 to 100 years."
            ),
            requirements="Required",
        ),
    )

    lca_functional_unit: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Functional equivalence specified for the assessment.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="Goal & Scope",
            attribute_name="Functional unit",
            field_code="lca_functional_unit",
            description=("Functional unit, i.e., functional equivalence specified for the assessment"),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
        ),
    )

    lca_rsp: int = Field(
        description="Reference study period duration in years.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="Reference Study period",
            field_code="lca_rsp",
            description=(
                "Duration over which the environmental impacts of a building "
                "are assessed, typically ranging from 50 to 100 years"
            ),
            constraint="numerical",
            units="#",
            requirements="Required",
            example="50",
        ),
    )

    lca_building_regulation_code: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Building regulation and code compliance methodology.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="Administrative data",
            attribute_name="Building regulation / Code",
            field_code="project_building_regulation_code",
            description=(
                "Building regulation and code compliance methodology for "
                "calculating carbon emissions across the entire building life "
                "cycle."
            ),
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="ASHRAE 204p",
        ),
    )

    lca_software_name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Details of the software used for LCA calculation.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA Software name",
            field_code="lca_software_name",
            description="Details of the software used for LCA calculation",
            constraint="string < 200 characters",
            units="none",
            requirements="Recommended",
            example="GBDI tool",
        ),
    )

    lca_software_publisher: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Company or entity that publishes the software.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA software publisher",
            field_code="lca_software_publisher",
            description="Company or entity that publishes the software",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="GBDI",
        ),
    )

    lca_software_version: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200), nullable=True),
        description="Specific version number of the software being used.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA software version",
            field_code="lca_software_version",
            description="Specific version number of the software being used",
            constraint="string < 200 characters",
            units="none",
            requirements="Optional",
            example="v2.1.1",
        ),
    )

    lca_database_name: str = Field(
        sa_column=Column(String(200)),
        description="Background database name.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA database name",
            field_code="lca_database_name",
            description="Background database name",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
            example="ecoinvent",
        ),
    )

    lca_database_version: str = Field(
        sa_column=Column(String(200)),
        description="Background data version or I-O source.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA database version",
            field_code="lca_database_version",
            description="Background data version (or I-O source)",
            constraint="string < 200 characters",
            units="none",
            requirements="Required",
            example="v3.1",
        ),
    )

    lca_temporal_approach: Optional[LCATemporalApproach] = Field(
        default=None,
        sa_column=Column(SAEnum(LCATemporalApproach), nullable=True),
        description="Type of LCA.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA temporal approach",
            field_code="lca_temporal_approach",
            description="Type of LCA (e.g., probabilistic, dynamic, prospective)",
            requirements="Optional",
            example="Probabilistic",
        ),
    )

    lca_model: Optional[LCAModel] = Field(
        default=None,
        sa_column=Column(SAEnum(LCAModel), nullable=True),
        description="Type of LCA model.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA model",
            field_code="lca_model",
            description="Type of LCA model",
            units="none",
            requirements="Optional",
            example="Process-based",
        ),
    )

    lca_stages: LifeCycleStage_ISO14040_44 = Field(
        sa_column=Column(SAEnum(LifeCycleStage_ISO14040_44)),
        description="Life cycle stages included in the assessment scope.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Life cycle stages",
            field_code="lca_cyle_stages",
            description=(
                "Different Life Cycle Assessment (LCA) stages depending on where you start and stop measuring"
            ),
            units="none",
            requirements="Required",
            example="Cradle to Gate with Options (A1–A3 + others)",
        ),
    )

    lcia_methodology: LCIAMethodology = Field(
        sa_column=Column(SAEnum(LCIAMethodology)),
        description="Impact assessment method.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCIA method",
            field_code="lcia_method",
            description="Impact assessment method (for GHG emissions, GWP indicator)",
            requirements="Required",
            example="EN15804+A2, NMD",
        ),
    )

    lca_biogenic_carbon: Optional[bool] = Field(
        default=None,
        description="Whether biogenic carbon is included in the assessment.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Biogenic carbon",
            field_code="lca_biogenic_carbon",
            description="Biogenic carbon included in assessment",
            units="none",
            requirements="Recommended",
            example="Yes",
        ),
    )

    lca_biogenic_method: Optional[BiogenicCarbonAccounting] = Field(
        default=None,
        sa_column=Column(SAEnum(BiogenicCarbonAccounting), nullable=True),
        description="Method used for biogenic carbon accounting.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Biogenic carbon accounting method",
            field_code="lca_biogenic_method",
            description="Method used for biogenic carbon accounting",
            units="none",
            requirements="Recommended",
            example="-1/+1;",
        ),
    )

    lca_material_source: MaterialQuantitiesSource = Field(
        sa_column=Column(SAEnum(MaterialQuantitiesSource)),
        description="Main source of material quantities.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA material quantities source",
            field_code="lca_material_source",
            description="Main source of material quantities",
            units="none",
            requirements="Required",
            example="BIM Model",
        ),
    )

    lca_a1_3: bool = Field(
        description="Whether A1-3 Production stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A1-3 Production",
            field_code="lca_a1_3",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_a4: bool = Field(
        description="Whether A4 Transport stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A4 Transport",
            field_code="lca_a4",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_a5: bool = Field(
        description="Whether A5 Construction stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5 Construction",
            field_code="lca_a5",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b1: bool = Field(
        description="Whether B1 Use stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B1 Use",
            field_code="lca_b1",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b2: bool = Field(
        description="Whether B2 Maintenance stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B2 Maintenance",
            field_code="lca_b2",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b3: bool = Field(
        description="Whether B3 Repair stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B3 Repair",
            field_code="lca_b3",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b4: bool = Field(
        description="Whether B4 Replacement stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B4 Replacement",
            field_code="lca_b4",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b5: bool = Field(
        description="Whether B5 Refurbishment stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B5 Refurbishment",
            field_code="lca_b5",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b6: bool = Field(
        description="Whether B6 Operational energy use stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B6 Operational energy use",
            field_code="lca_b6",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_b7: bool = Field(
        description="Whether B7 Operational water use stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B7 Operational water use",
            field_code="lca_b7",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_c1: bool = Field(
        description="Whether C1 De-construction stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C1 De-construction",
            field_code="lca_c1",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_c2: bool = Field(
        description="Whether C2 Transport stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C2 Transport",
            field_code="lca_c2",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_c3: bool = Field(
        description="Whether C3 Waste processing stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C3 Waste processing",
            field_code="lca_c3",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_c4: bool = Field(
        description="Whether C4 Disposal stage is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C4 Disposal",
            field_code="lca_c4",
            description="Life cycle stage included",
            units="none",
            requirements="Required",
            example="Yes",
        ),
    )

    lca_d: bool = Field(
        description="Whether stage D is included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="(D) Reuse, recovery, recycling",
            field_code="lca_d",
            description="Life cycle stage included",
            units="none",
            requirements="Optional",
            example="Yes",
        ),
    )

    schema_metadata: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False, server_default="{}"),
        description=("Optional record-level metadata for constraints that are not enforced by SQL types alone."),
    )


class ProjectRecord(ProjectRecordBase, table=True):
    __tablename__ = "project_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    bill_of_materials: List["BuildingBillMaterialsSlimRecord"] = Relationship(back_populates="project")
