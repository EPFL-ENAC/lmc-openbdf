from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel

from openbdf.model.draft import make_draft_model

from .enums.buildings import (
    BuildingClassificationCode,
    BuildingElementClassificationTier,
    BuildingFacingDirection,
    BuildingStructureType,
    BuildingTypology,
    FloorAreaInclusions,
    FoundationType,
    GFAMeasurementMethod,
    GrossFloorAreaStandard,
    SharedComponentAllocationRule,
)
from .enums.countries import Country
from .enums.energy import (
    BuildingEnergyClassificationSystem,
    BuildingEnergyCodeSystem,
    EmissionFactorScenario,
    OnSiteRenewableAllocationApproach,
    PrimaryEnergySource,
)
from .enums.geography import (
    ClimateZone,
    ExtendedDefaultDataBasis,
    FEMASeismicActivity,
    SoilType,
)
from .enums.lca import (
    AssessmentType_EN15978,
    BiogenicCarbonAccounting,
    DataWeightingBasis,
    LCADatabase,
    LCADatabaseSystemModel,
    LCATemporalApproach,
    LCIAMethodology,
    LCIModelingApproach,
    LifeCycleSystemBoundary,
    LimitValueScopeReduction,
)
from .enums.materials import (
    MaterialQuantitiesSource,
    ReplacementCountMethod,
)
from .enums.project import (
    ConstructionType,
    ProjectPhase,
    ProjectPhaseCommon,
    ProjectUnits,
    RecordType,
)
from .enums.references import Reference
from .field_metadata import openbdf_field_metadata


class ProjectRecordBase(SQLModel):
    project_id: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Unique ID assigned to this specific project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project ID",
            field_code="project_id",
            description="Unique ID assigned to this specific project.",
            constraint="max 200 characters",
            requirements="Automatic",
            criticality="SHOULD",
            example="ABC1234",
            reference=Reference.ECHO_GBDB,
        ),
    )

    project_custom_id: Optional[str] = Field(
        default=None,
        description="Unique custom ID assigned to this specific project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project ID custom",
            field_code="project_custom_id ",
            description="Unique custom ID assigned to this specific project.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.GBDI_SLICE,
        ),
    )

    record_type: RecordType = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(RecordType),
        description="Kind of object the submission describes",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Record type",
            field_code="record_type",
            description="Kind of object the submission describes",
            requirements="Required",
            criticality="MUST",
            reference=Reference.GBDI_SLICE,
        ),
    )

    project_units: ProjectUnits = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(ProjectUnits),
        description="Unit system used in the assessment.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project Unit System",
            field_code="project_units",
            description="Unit system used in the assessment.",
            requirements="Required",
            criticality="MUST",
            example="Metric, International Units System (SI)",
            reference=Reference.ECHO,
        ),
    )

    project_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project name",
            field_code="project_name",
            description="Name of the project.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="Brilliant Group Hotel",
            reference=Reference.ECHO,
        ),
    )

    project_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="General description of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project description",
            field_code="project_description",
            description="General description of the project.",
            constraint="max 500 characters",
            requirements="Optional",
            criticality="MAY",
            example="A new hotel on the harbour",
            reference=Reference.ECHO,
        ),
    )

    project_construction_type: Optional[ConstructionType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ConstructionType),
        description="Construction type of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project construction type",
            field_code="project_construction_type",
            description="Construction type of the project.",
            requirements="Required",
            criticality="SHOULD",
            example="New construction",
            reference=Reference.EN15978_2026,
        ),
    )

    project_country: Optional[Country] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(Country),
        description="Country where the project is located.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Country",
            field_code="project_country",
            description="Country where the project is located.",
            requirements="Required",
            criticality="SHOULD",
            example="Afghanistan",
            reference=Reference.ECHO,
        ),
    )

    project_city: Optional[str] = Field(
        default=None,
        max_length=200,
        description="City where the project is located.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="City",
            field_code="project_city",
            description="City where the project is located.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Potsdam",
            reference=Reference.ECHO,
        ),
    )

    project_state: Optional[str] = Field(
        default=None,
        max_length=200,
        description="State, province, or country subdivision.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="State",
            field_code="project_state",
            description="State, province, or country subdivision.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="Brandenburg",
            reference=Reference.ECHO,
        ),
    )

    project_address: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Address of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Address",
            field_code="project_address",
            description="Address of the project.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="Voorstrasse 20, 1417 Potsdam",
            reference=Reference.ECHO,
        ),
    )

    project_owner_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Individual or entity that owns the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Owner/client name",
            field_code="project_owner_name",
            description="Individual or entity that owns the project.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Mr. Brown Alter",
            reference=Reference.ECHO,
        ),
    )

    project_sustainability_certification: Optional[bool] = Field(
        default=None,
        description="Indicate if a sustainability certification was used for the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Sustainability certification",
            field_code="project_sustainability_certification",
            description="Indicate if a sustainability certification was used for the project.",
            requirements="Recommended",
            criticality="MAY",
            reference=Reference.ECHO,
        ),
    )

    project_sustainability_certification_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Sustainability certification applied for the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Sustainability certification Name",
            field_code="project_sustainability_certification_name",
            description="Sustainability certification applied for the project.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="LEED",
            reference=Reference.ECHO,
        ),
    )

    project_sustainability_certification_date: Optional[date] = Field(
        default=None,
        description="Date of certification application.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Sustainability certification application date",
            field_code="project_sustainability_certification_date",
            description="Date of certification application.",
            requirements="Recommended",
            criticality="MAY",
            example="08/02/2026",
            reference=Reference.GBDI,
        ),
    )

    project_sustainability_certification_id: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Unique ID assigned to the certification application.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Sustainability certification application ID",
            field_code="project_sustainability_certification_id",
            description="Unique ID assigned to the certification application.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="ABC1234",
            reference=Reference.GBDI,
        ),
    )

    project_permit_date: Optional[date] = Field(
        default=None,
        description="Date of application for construction permit.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project permit application date",
            field_code="project_permit_date",
            description="Date of application for construction permit.",
            requirements="Recommended",
            criticality="MAY",
            example="08/02/2026",
            reference=Reference.GBDI,
        ),
    )

    project_permit_id: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Unique ID of the project permit.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project permit ID",
            field_code="project_permit_id",
            description="Unique ID of the project permit.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="ABC1234",
            reference=Reference.GBDI,
        ),
    )

    project_no_of_buildings: Optional[int] = Field(
        default=None,
        description="Total number of buildings in the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="No. of buildings",
            field_code="project_no_of_buildings",
            description="Total number of buildings in the project.",
            requirements="Required",
            criticality="SHOULD",
            example="5",
            reference=Reference.CLF,
        ),
    )

    project_phase: Optional[ProjectPhase] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ProjectPhase),
        description="Stage of the project when LCA is conducted.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project phase at time of assessment",
            field_code="project_phase",
            description="Stage of the project when LCA is conducted.",
            requirements="Required",
            criticality="SHOULD",
            example="Preliminary studies",
            reference=Reference.RIBA_PLAN_OF_WORK_2020_HOAI_2021_AIA_SIA_112,
        ),
    )

    project_phase_common: Optional[ProjectPhaseCommon] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ProjectPhaseCommon),
        description="Project phase mapped to the common definition of design steps and project phases.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project phase, common definition",
            field_code="project_phase_common",
            description="Project phase mapped to the common definition of design steps and project phases.",
            requirements="Automatic",
            criticality="MAY",
            reference=Reference.IEA_EBC_ANNEX_72,
        ),
    )

    project_assessment_type: AssessmentType_EN15978 = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(AssessmentType_EN15978),
        description="Granularity of the building model behind the assessment",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Assessment type",
            field_code="project_assessment_type",
            description="Granularity of the building model behind the assessment",
            requirements="Required",
            criticality="MUST",
            reference=Reference.EN15978_2026,
        ),
    )

    project_design_start_date: Optional[date] = Field(
        default=None,
        description="Project design start date.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project design start date",
            field_code="project_design_start_date",
            description="Project design start date.",
            requirements="Recommended",
            criticality="MAY",
            example="08/02/2026",
            reference=Reference.GBDI,
        ),
    )

    project_construction_company_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the company constructing the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Construction company name",
            field_code="project_construction_company_name",
            description="Name of the company constructing the project.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Terranova Construction Company",
            reference=Reference.GBDI,
        ),
    )

    project_construction_company_address: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Physical location of the construction company.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Construction company address",
            field_code="project_construction_company_address",
            description="Physical location of the construction company.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Seebachstrasse 21, 5100 Zurich",
            reference=Reference.GBDI,
        ),
    )

    project_contractor_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the contractor executing the construction.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Contractor name",
            field_code="project_contractor_name",
            description="Name of the contractor executing the construction.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Regionale Contractors",
            reference=Reference.GBDI,
        ),
    )

    project_architect_engineer_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the architect/engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Architect/engineer name",
            field_code="project_architect_engineer_name",
            description="Name of the architect/engineer appointed on the project.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Peter Sylon",
            reference=Reference.GBDI,
        ),
    )

    project_structural_engineer_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the structural engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Structural engineer name",
            field_code="project_structural_engineer_name",
            description="Name of the structural engineer appointed on the project.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Peter Sylon",
            reference=Reference.GBDI,
        ),
    )

    project_mep_engineer_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the MEP engineer appointed on the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="MEP engineer name",
            field_code="project_mep_engineer_name",
            description="Name of the MEP engineer appointed on the project.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Peter Sylon",
            reference=Reference.GBDI,
        ),
    )

    project_environmental_consultant_company_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Company conducting the LCA assessment.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Environmental consultant company name",
            field_code="project_environmental_consultant_company_name",
            description="Company conducting the LCA assessment.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Environmental Design Consultants",
            reference=Reference.GBDI,
        ),
    )

    project_environmental_assessor_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the environmental assessor.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Environmental assessor name",
            field_code="project_environmental_assessor_name",
            description="Name of the environmental assessor.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="Thomas Casper",
            reference=Reference.GBDI,
        ),
    )

    building_age_class: Optional[str] = Field(
        default=None,
        description="Construction period of the archetype, as given in the source stock dataset.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Administrative data",
            attribute_name="Building age class",
            field_code="building_age_class",
            description="Construction period of the archetype, as given in the source stock dataset.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.GBDI,
        ),
    )

    project_plot_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total plot area of the project.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="Project total plot area",
            field_code="project_plot_area",
            description="Total plot area of the project.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="500",
            reference=Reference.ECHO,
        ),
    )

    project_gfa_method: GFAMeasurementMethod = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(GFAMeasurementMethod),
        description="Gross Floor Area measurement method.",
        schema_extra=openbdf_field_metadata(
            group="Project",
            sub_group="Administrative data",
            attribute_name="GFA measurement method",
            field_code="project_gfa_method",
            description="Gross Floor Area measurement method.",
            requirements="Required",
            criticality="MUST",
            example="IPMS – International Property Measurement Standards",
            reference=Reference.ISO_9836_IPMS_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    building_id: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Assigned identifier for the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building ID",
            field_code="building_id",
            description="Assigned identifier for the building.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="ABC1234",
            reference=Reference.GBDI,
        ),
    )

    building_gps_coordinates: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Latitude and longitude of the building project.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building GPS coordinates",
            field_code="building_gps_coordinates",
            description="Latitude and longitude of the building project.",
            constraint="max 100 characters",
            requirements="Recommended",
            criticality="MAY",
            example="41.40338, 2.17403",
            reference=Reference.ISO_6709,
        ),
    )

    building_geographic_climate_zone: Optional[ClimateZone] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ClimateZone),
        description="Climate zone of the building site, with its classification system: ASHRAE 169, IECC or Koppen-Geiger.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Climate zone",
            field_code="building_geographic_climate_zone",
            description="Climate zone of the building site, with its classification system: ASHRAE 169, IECC or Koppen-Geiger.",
            requirements="Recommended",
            criticality="SHOULD",
            example="2A (Hot - Humid)",
            reference=Reference.ASHRAE_169_IECC_KOPPEN_GEIGER,
        ),
    )

    building_altitude: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Elevation of the project site above sea level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Altitude",
            field_code="building_altitude",
            description="Elevation of the project site above sea level.",
            units="m",
            requirements="Recommended",
            criticality="MAY",
            example="200m or 400 ft.",
            reference=Reference.GBDI,
        ),
    )

    building_seismic_zone: Optional[FEMASeismicActivity] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(FEMASeismicActivity),
        description="Classification of seismic activity level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Seismic zone",
            field_code="building_seismic_zone",
            description="Classification of seismic activity level.",
            requirements="Recommended",
            criticality="MAY",
            example="SDC A: Minor expected ground shaking.",
            reference=Reference.ECHO,
        ),
    )

    building_use_type: Optional[BuildingTypology] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingTypology),
        description="Main use of the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building use type",
            field_code="building_use_type",
            description="Main use of the building.",
            requirements="Required",
            criticality="SHOULD",
            example="Multi-family buildings",
            reference=Reference.EN15978_2026_ECHO_GBDB,
        ),
    )

    building_residential_units: Optional[int] = Field(
        default=None,
        description="Total number of individual residential units.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of individual residential units",
            field_code="building_residential_units",
            description="Total number of individual residential units.",
            requirements="Recommended",
            criticality="MAY",
            example="25",
            reference=Reference.ECHO,
        ),
    )

    building_rooms: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total number of rooms in residential units.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of rooms in the residential units",
            field_code="building_rooms",
            description="Total number of rooms in residential units.",
            requirements="Optional",
            criticality="MAY",
            example="100",
            reference=Reference.GBDI,
        ),
    )

    building_construction_start_date: Optional[date] = Field(
        default=None,
        description="The year/date building construction officially started.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Construction start date",
            field_code="building_construction_start_date",
            description="The year/date building construction officially started.",
            requirements="Optional",
            criticality="MAY",
            example="07/02/2026",
            reference=Reference.ECHO,
        ),
    )

    building_construction_end_date: Optional[date] = Field(
        default=None,
        description="The year/date building construction completed.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Construction end date",
            field_code="building_construction_end_date",
            description="The year/date building construction completed.",
            requirements="Recommended",
            criticality="MAY",
            example="07/02/2026",
            reference=Reference.ECHO,
        ),
    )

    building_demolished_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Floor area dismantled or destroyed in end-of-life phase.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Demolished area",
            field_code="building_demolished_area",
            description="Floor area dismantled or destroyed in end-of-life phase.",
            units="m2",
            requirements="Optional",
            criticality="MAY",
            example="500",
            reference=Reference.ISO_9836,
        ),
    )

    building_roof_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total roof surface area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Roof area",
            field_code="building_roof_area",
            description="Total roof surface area.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="500",
            reference=Reference.ISO_9836,
        ),
    )

    building_floors_bg: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2,
        description="Number of floor levels below ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of floors (below ground)",
            field_code="building_floors_bg",
            description="Number of floor levels below ground.",
            requirements="Recommended",
            criticality="SHOULD",
            example="2",
            reference=Reference.ECHO,
        ),
    )

    building_floors_ag: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2,
        description="Number of floor levels above ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of floors (above ground)",
            field_code="building_floors_ag",
            description="Number of floor levels above ground.",
            requirements="Recommended",
            criticality="SHOULD",
            example="3",
            reference=Reference.ECHO,
        ),
    )

    building_parking_building: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2,
        description="Parking spots included in the building perimeter.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of parking spots (in building)",
            field_code="building_parking_building",
            description="Parking spots included in the building perimeter.",
            requirements="Recommended",
            criticality="MAY",
            example="5",
            reference=Reference.ECHO_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    building_parking_dislocated: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2,
        description="Parking spots dislocated from the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="No. of parking spots (dislocated)",
            field_code="building_parking_dislocated",
            description="Parking spots dislocated from the building.",
            requirements="Recommended",
            criticality="MAY",
            example="6",
            reference=Reference.ECHO_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    building_element_classification_code_name: Optional[BuildingClassificationCode] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingClassificationCode),
        description="Name of the custom or national building element classification code utilized.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building Element Classification Code Name",
            field_code="building_element_classification_code_name",
            description="Name of the custom or national building element classification code utilized.",
            requirements="Recommended",
            criticality="MAY",
            reference=Reference.ISO_12006_2_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    building_element_classification_code_link: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Link of the custom or national building element classification code utilized.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building Element Classification Code Link",
            field_code="building_element_classification_code_link",
            description="Link of the custom or national building element classification code utilized.",
            constraint="max 500 characters",
            requirements="Recommended",
            criticality="MAY",
            reference=Reference.ISO_12006_2,
        ),
    )

    building_element_classification_code_version: Optional[str] = Field(
        default=None,
        description="Version of the custom or national building element classification code utilized.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building Element Classification Code Version",
            field_code="building_element_classification_code_version",
            description="Version of the custom or national building element classification code utilized.",
            requirements="Recommended",
            criticality="MAY",
            reference=Reference.ISO_12006_2,
        ),
    )

    building_element_classification_tier: Optional[BuildingElementClassificationTier] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingElementClassificationTier),
        description="Tiers of the custom or national building element classification covered",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (general)",
            attribute_name="Building Element Classification Tier",
            field_code="building_element_classification_tier",
            description="Tiers of the custom or national building element classification covered",
            requirements="Recommended",
            criticality="MAY",
            reference=Reference.REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    building_structure_type: Optional[BuildingStructureType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingStructureType),
        description="Main structural material and structural system of the building, or a mixed combination.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building structure type",
            field_code="building_structure_type",
            description="Main structural material and structural system of the building, or a mixed combination.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Concrete (In-Situ)",
            reference=Reference.EN_1992_EN_1993_EN_1995_EN_1996,
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
            description="Whether prefabricated elements are used.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15978_2026,
        ),
    )

    building_soil_data: Optional[SoilType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(SoilType),
        description="Information about the category of soil.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Soil data",
            field_code="building_soil_data",
            description="Information about the category of soil.",
            requirements="Recommended",
            criticality="MAY",
            example="sandy gravel",
            reference=Reference.ECHO,
        ),
    )

    building_foundation_type: Optional[FoundationType] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(FoundationType),
        description="Construction method used to support a building below ground.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Foundation type",
            field_code="building_foundation_type",
            description="Construction method used to support a building below ground.",
            requirements="Required",
            criticality="SHOULD",
            example="Spread foundation- Pad Footings (Isolated)",
            reference=Reference.ECHO,
        ),
    )

    building_required_service_life: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Service life required by the client or by regulation for the building, in years",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Required Service Life (RSL)",
            field_code="building_required_service_life",
            description="Service life required by the client or by regulation for the building, in years",
            units="years",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.ISO_15686_1_ISO_15686_2,
        ),
    )

    building_energy_classification_system: Optional[BuildingEnergyClassificationSystem] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingEnergyClassificationSystem),
        description="Energy classification of the building.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy classification system",
            field_code="building_energy_classification_system",
            description="Energy classification of the building.",
            requirements="Recommended",
            criticality="MAY",
            example="A, B, A+",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_energy_code_system: Optional[BuildingEnergyCodeSystem] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingEnergyCodeSystem),
        description="Which energy code or standard the energy figures are calculated against",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy code system",
            field_code="building_energy_code_system",
            description="Which energy code or standard the energy figures are calculated against",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_energy_demand_thermal: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Energy demand for thermal space services.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy demand - thermal",
            field_code="building_energy_demand_thermal",
            description="Energy demand for thermal space services.",
            units="kWh/y",
            requirements="Recommended",
            criticality="MAY",
            example="100",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_energy_demand_electricity: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Energy demand for electrical equipment.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy demand - electric",
            field_code="building_energy_demand_electricity",
            description="Energy demand for electrical equipment.",
            units="kWh/y",
            requirements="Recommended",
            criticality="MAY",
            example="101",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_energy_supply_thermal: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Energy supply from local thermal RES.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy supply - thermal",
            field_code="building_energy_supply_thermal",
            description="Energy supply from local thermal RES.",
            units="kWh/y",
            requirements="Recommended",
            criticality="MAY",
            example="102",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_energy_supply_electricity: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Energy supply from local electrical RES.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Energy supply - electric",
            field_code="building_energy_supply_electricity",
            description="Energy supply from local electrical RES.",
            units="kWh/y",
            requirements="Recommended",
            criticality="MAY",
            example="103",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_primary_energy_source: Optional[PrimaryEnergySource] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(PrimaryEnergySource),
        description="Primary energy source for heating/cooling/DHW.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building primary energy source",
            field_code="building_primary_energy_source",
            description="Primary energy source for heating/cooling/DHW.",
            requirements="Recommended",
            criticality="MAY",
            example="Coal",
            reference=Reference.EN_ISO_52000_1,
        ),
    )

    building_bipv_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Type and scope of BIPV.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (technical)",
            attribute_name="Building BIPV description",
            field_code="building_bipv_description",
            description="Type and scope of BIPV.",
            constraint="max 500 characters",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_2026,
        ),
    )

    building_orientation: Optional[BuildingFacingDirection] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BuildingFacingDirection),
        description="Orientation of the main façade.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building orientation",
            field_code="building_orientation",
            description="Orientation of the main façade.",
            requirements="Recommended",
            criticality="MAY",
            example="E",
            reference=Reference.GBDI,
        ),
    )

    building_footprint: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Area covered by the building on the plot.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building footprint area",
            field_code="building_footprint",
            description="Area covered by the building on the plot.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="500",
            reference=Reference.ECHO,
        ),
    )

    building_unconditioned_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Floor area within the building that is not conditioned.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Unconditioned floor area",
            field_code="building_unconditioned_area",
            description="Floor area within the building that is not conditioned.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="501",
            reference=Reference.ECHO,
        ),
    )

    building_conditioned_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Area used to calculate building zone energy performance.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Conditioned floor area",
            field_code="building_conditioned_area",
            description="Area used to calculate building zone energy performance.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="502",
            reference=Reference.ECHO,
        ),
    )

    building_useful_floor_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total area intended for primary use of the building zone.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Useful floor area (UFA)",
            field_code="building_useful_floor_area",
            description="Total area intended for primary use of the building zone.",
            units="m2",
            requirements="Required",
            criticality="SHOULD",
            example="503",
            reference=Reference.REGULATION_EU_2026_52_ANNEX_III_IPMS,
        ),
    )

    building_gross_floor_area: Decimal = Field(
        max_digits=18,
        decimal_places=4,
        description="Total gross floor area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Gross floor area (GFA)",
            field_code="building_gross_floor_area",
            description="Total gross floor area.",
            units="m2",
            requirements="Required",
            criticality="MUST",
            example="504",
            reference=Reference.ECHO,
        ),
    )

    building_gross_floor_area_standard: Optional[GrossFloorAreaStandard] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(GrossFloorAreaStandard),
        description="Definition of GFA according to national standards.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Gross floor area (GFA) Standard",
            field_code="building_gross_floor_area_standard",
            description="Definition of GFA according to national standards.",
            requirements="Recommended",
            criticality="SHOULD",
            example="RICS (UK), Type 2: GIA (Gross Internal Area)",
            reference=Reference.EN15978_2026,
        ),
    )

    building_floor_area_inclusions: Optional[FloorAreaInclusions] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(FloorAreaInclusions),
        description="What the reported floor area contains",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Floor area spatial inclusions",
            field_code="building_floor_area_inclusions",
            description="What the reported floor area contains",
            constraint="multi-select",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.REGULATION_EU_2026_52_ANNEX_III_ISO_9836,
        ),
    )

    building_circulation_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total circulation area.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Circulation area",
            field_code="building_circulation_area",
            description="Total circulation area.",
            units="m2",
            requirements="Optional",
            criticality="MAY",
            example="500",
            reference=Reference.ISO_9836,
        ),
    )

    building_technical_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total area reserved for building services and equipment.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Technical area",
            field_code="building_technical_area",
            description="Total area reserved for building services and equipment.",
            units="m2",
            requirements="Optional",
            criticality="MAY",
            example="501",
            reference=Reference.ISO_9836,
        ),
    )

    building_built_floor_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="GFA plus parking area located inside the building shell.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Built floor area (BFA)",
            field_code="building_built_floor_area",
            description="GFA plus parking area located inside the building shell.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="502",
            reference=Reference.ISO_9836,
        ),
    )

    building_envelope_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total area of the thermal envelope, enclosing the conditioned volume.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Thermal envelope area",
            field_code="building_envelope_area",
            description="Total area of the thermal envelope, enclosing the conditioned volume.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="503",
            reference=Reference.ECHO,
        ),
    )

    building_window_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Combined surface area of all windows.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Window area",
            field_code="building_window_area",
            description="Combined surface area of all windows.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="504",
            reference=Reference.ISO_9836,
        ),
    )

    building_wall_area_interior: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total surface area of internal walls.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Wall area (interior)",
            field_code="building_wall_area_interior",
            description="Total surface area of internal walls.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="505",
            reference=Reference.ISO_9836,
        ),
    )

    building_enclosed_parking_area: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Parking area enclosed and/or attached to the building shell.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Enclosed parking area",
            field_code="building_enclosed_parking_area",
            description="Parking area enclosed and/or attached to the building shell.",
            units="m2",
            requirements="Recommended",
            criticality="MAY",
            example="506",
            reference=Reference.EN15978_2026,
        ),
    )

    building_height: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Total height of the building above finished ground level.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building height",
            field_code="building_height",
            description="Total height of the building above finished ground level.",
            units="m",
            requirements="Recommended",
            criticality="MAY",
            example="20",
            reference=Reference.ECHO,
        ),
    )

    building_floor_height: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Average vertical distance between finished floors.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Average floor height",
            field_code="building_floor_height",
            description="Average vertical distance between finished floors.",
            units="m",
            requirements="Recommended",
            criticality="MAY",
            example="3",
            reference=Reference.ISO_9836,
        ),
    )

    building_volume: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Gross building volume.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Building volume",
            field_code="building_volume",
            description="Gross building volume.",
            units="m3",
            requirements="Recommended",
            criticality="MAY",
            example="50",
            reference=Reference.ISO_9836,
        ),
    )

    building_occupancy_count: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Estimated occupancy count.",
        schema_extra=openbdf_field_metadata(
            group="Building",
            sub_group="Building data (geometry)",
            attribute_name="Occupancy count",
            field_code="building_occupancy_count",
            description="Estimated occupancy count.",
            requirements="Recommended",
            criticality="MAY",
            example="10",
            reference=Reference.ECHO,
        ),
    )

    lca_assessment_date: Optional[date] = Field(
        default=None,
        description="Date of the life-cycle assessment conducted by the assessor.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Administrative data",
            attribute_name="Project date of assessment",
            field_code="lca_assessment_date",
            description="Date of the life-cycle assessment conducted by the assessor.",
            requirements="Recommended",
            criticality="SHOULD",
            example="11/02/2026",
            reference=Reference.ECHO,
        ),
    )

    lca_third_party_verified: Optional[bool] = Field(
        default=None,
        description="Whether the project LCA is verified by a third party.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Administrative data",
            attribute_name="Third party verified",
            field_code="lca_third_party_verified",
            description="Whether the project LCA is verified by a third party.",
            requirements="Recommended",
            criticality="MAY",
            example="True",
            reference=Reference.ECHO,
        ),
    )

    lca_third_party_verifier_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the third-party verifier.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Administrative data",
            attribute_name="Third party verifier name",
            field_code="lca_third_party_verifier_name",
            description="Name of the third-party verifier.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="MAY",
            example="Pullmann Consultants, Zurich",
            reference=Reference.ECHO,
        ),
    )

    lca_verification_date: Optional[date] = Field(
        default=None,
        description="Date of third-party verification.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Administrative data",
            attribute_name="Verification date",
            field_code="lca_verification_date",
            description="Date of third-party verification.",
            requirements="Optional",
            criticality="MAY",
            example="07/02/2026",
            reference=Reference.ECHO,
        ),
    )

    lca_building_regulation_code: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Building regulation and code compliance methodology.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Administrative data",
            attribute_name="Building regulation/code",
            field_code="lca_building_regulation_code",
            description="Building regulation and code compliance methodology.",
            constraint="max 200 characters",
            requirements="Required",
            criticality="SHOULD",
            example="ASHRAE 204p",
            reference=Reference.ECHO,
        ),
    )

    lca_goal: Optional[str] = Field(
        default=None,
        description="Goal of the study.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Goal & Scope",
            attribute_name="LCA goal",
            field_code="lca_goal",
            description="Goal of the study.",
            requirements="Required",
            criticality="SHOULD",
            example="Permission from municipal corporation",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_reference_unit: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Reference unit the results are primarily expressed for. E.g., 1 m2 GFA / year.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Goal & Scope",
            attribute_name="Reference Unit",
            field_code="lca_reference_unit",
            description="Reference unit the results are primarily expressed for. E.g., 1 m2 GFA / year.",
            constraint="max 200 characters",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_reference_study_period: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Duration over which the environmental impacts of a building are assessed, typically ranging from 50 to 100 years.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Goal & Scope",
            attribute_name="Reference Study Period (RSP)",
            field_code="lca_reference_study_period",
            description="Duration over which the environmental impacts of a building are assessed, typically ranging from 50 to 100 years.",
            constraint="max 200 characters",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.EN15978_2026_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    lca_replacement_count_method: Optional[ReplacementCountMethod] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ReplacementCountMethod),
        description="Rule used to count component replacements in module B4",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Goal & Scope",
            attribute_name="Replacement count method",
            field_code="lca_replacement_count_method",
            description="Rule used to count component replacements in module B4",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    lca_functional_unit: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Functional equivalence specified for the assessment. E.g., 1 m2 GFA over 50-year RSL.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Goal & Scope",
            attribute_name="Functional unit",
            field_code="lca_functional_unit",
            description="Functional equivalence specified for the assessment. E.g., 1 m2 GFA over 50-year RSL.",
            constraint="max 200 characters",
            requirements="Required",
            criticality="SHOULD",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_software_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Details of the software used for LCA calculation.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA Software name",
            field_code="lca_software_name",
            description="Details of the software used for LCA calculation.",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="SHOULD",
            example="GBDI tool",
            reference=Reference.ECHO,
        ),
    )

    lca_software_publisher: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Company or entity that publishes the software.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA software publisher",
            field_code="lca_software_publisher",
            description="Company or entity that publishes the software.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="SHOULD",
            example="GBDI",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_software_version: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Specific version number of the software being used.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA inventory",
            attribute_name="LCA software version",
            field_code="lca_software_version",
            description="Specific version number of the software being used.",
            constraint="max 200 characters",
            requirements="Optional",
            criticality="MAY",
            example="v2.1.1",
            reference=Reference.ECHO,
        ),
    )

    lca_database_name: Optional[LCADatabase] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(LCADatabase),
        description="Background database and its release, in one value, for example OKOBAUDAT_20.23.050.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA database name",
            field_code="lca_database_name",
            description="Background database and its release, in one value, for example OKOBAUDAT_20.23.050.",
            requirements="Required",
            criticality="SHOULD",
            example="ecoinvent",
            reference=Reference.EN_15941_2024,
        ),
    )

    lca_database_system_model: LCADatabaseSystemModel = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(LCADatabaseSystemModel),
        description="System model of the background database",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Database system model",
            field_code="lca_database_system_model",
            description="System model of the background database",
            requirements="Required",
            criticality="MUST",
            reference=Reference.ECOINVENT_EN15804_A2,
        ),
    )

    lca_database_version: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Background data version or I-O source.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA database version",
            field_code="lca_database_version",
            description="Background data version or I-O source.",
            requirements="Removed",
            criticality="",
            example="v3.1",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_data_cpr_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share of the weighting basis documented with data from a declaration of performance and conformity.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Construction Products Regulation data share",
            field_code="lca_data_cpr_share",
            description="Share of the weighting basis documented with data from a declaration of performance and conformity.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_ecodesign_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with compatible data issued under product regulations adopted.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Ecodesign and energy labelling data share",
            field_code="lca_data_ecodesign_share",
            description="Share documented with compatible data issued under product regulations adopted.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_project_specific_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with project-specific data calculated to EN 15804 or EN 50693 or a compatible standard. Usable only where national legislation permits it.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Project-specific data share",
            field_code="lca_data_project_specific_share",
            description="Share documented with project-specific data calculated to EN 15804 or EN 50693 or a compatible standard. Usable only where national legislation permits it.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_product_specific_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with product-specific data calculated to EN 15804 or EN 50693 or a compatible standard. Usable only where national legislation permits it.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Product-specific data share",
            field_code="lca_data_product_specific_share",
            description="Share documented with product-specific data calculated to EN 15804 or EN 50693 or a compatible standard. Usable only where national legislation permits it.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_product_group_average_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with sectoral data representing the average of multiple products from one or more companies, provided by an industrial association or equivalent body covering the product. Usable only where national legislation permits it.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Average data for a product group share",
            field_code="lca_data_product_group_average_share",
            description="Share documented with sectoral data representing the average of multiple products from one or more companies, provided by an industrial association or equivalent body covering the product. Usable only where national legislation permits it.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_generic_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with generic data calculated to EN 15804 or EN 50693 or a compatible standard for a group of products for a country or region, neither site nor enterprise specific.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Generic data share",
            field_code="lca_data_generic_share",
            description="Share documented with generic data calculated to EN 15804 or EN 50693 or a compatible standard for a group of products for a country or region, neither site nor enterprise specific.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_default_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share documented with default values used to fill data gaps where no other type of data is available, or to simplify the calculation.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Default values share",
            field_code="lca_data_default_share",
            description="Share documented with default values used to fill data gaps where no other type of data is available, or to simplify the calculation.",
            constraint="0 to 1",
            units="fraction",
            requirements="Automatic",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_data_undeclared_share: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share of the weighting basis whose data type is not declared.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Undeclared share",
            field_code="lca_data_undeclared_share",
            description="Share of the weighting basis whose data type is not declared.",
            units="%",
            requirements="Automatic",
            criticality="MAY",
            reference=Reference.GBDI,
        ),
    )

    lca_data_weighting_basis: Optional[DataWeightingBasis] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(DataWeightingBasis),
        description="Quantity used to weight the data quality shares.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Data quality weighting basis",
            field_code="lca_data_weighting_basis",
            description="Quantity used to weight the data quality shares.",
            requirements="Automatic",
            criticality="MAY",
            reference=Reference.GBDI,
        ),
    )

    lca_completeness_score: Optional[Decimal] = Field(
        default=None,
        max_digits=18,
        decimal_places=4,
        description="Share of fields actually populated.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Submission completeness",
            field_code="lca_completeness_score",
            description="Share of fields actually populated.",
            units="%",
            requirements="Automatic",
            criticality="MAY",
            reference=Reference.EN_15941_2024,
        ),
    )

    lca_undeclared_material_note: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Basis used for materials without a verified EPD",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA Data quality",
            attribute_name="Undeclared material justification",
            field_code="lca_undeclared_material_note",
            description="Basis used for materials without a verified EPD",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="SHOULD",
            reference=Reference.REGULATION_EU_2026_52_ANNEX_III_EN15804,
        ),
    )

    lca_temporal_approach: Optional[LCATemporalApproach] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(LCATemporalApproach),
        description="Type of LCA (e.g., probabilistic, dynamic, probabilistic, prospective)",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA temporal approach",
            field_code="lca_temporal_approach",
            description="Type of LCA (e.g., probabilistic, dynamic, probabilistic, prospective)",
            requirements="Optional",
            criticality="SHOULD",
            example="Probabilistic",
            reference=Reference.EN15978_2026_ISO_14040,
        ),
    )

    lca_onsite_renewable_allocation: Optional[OnSiteRenewableAllocationApproach] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(OnSiteRenewableAllocationApproach),
        description="Approach chosen for allocating to the building the embodied emissions of on-site renewable energy production. Energy storage components are allocated to the building in full under every approach.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Allocation of embodied emissions of on-site renewable energy production",
            field_code="lca_onsite_renewable_allocation",
            description="Approach chosen for allocating to the building the embodied emissions of on-site renewable energy production. Energy storage components are allocated to the building in full under every approach.",
            requirements="Recommended",
            criticality="SHOULD",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_shared_component_allocation_rule: Optional[SharedComponentAllocationRule] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(SharedComponentAllocationRule),
        description="Rule applied to allocate the emissions of building components shared by multiple buildings. Stated only when the submission covers more than one building.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Rule for allocating emissions of shared building components",
            field_code="lca_shared_component_allocation_rule",
            description="Rule applied to allocate the emissions of building components shared by multiple buildings. Stated only when the submission covers more than one building.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_extended_default_data_use: Optional[bool] = Field(
        default=None,
        description="Whether the calculation was simplified through an extended use of default data.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Extended use of default data",
            field_code="lca_extended_default_data_use",
            description="Whether the calculation was simplified through an extended use of default data.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_extended_default_data_basis: Optional[ExtendedDefaultDataBasis] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(ExtendedDefaultDataBasis),
        description="The provision or circumstance under which the extended use of default data was applied.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Basis for the extended use of default data",
            field_code="lca_extended_default_data_basis",
            description="The provision or circumstance under which the extended use of default data was applied.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_limit_value_compliance: Optional[bool] = Field(
        default=None,
        description="Whether the result is calculated for the verification of compliance with a limit value rather than as a complete assessment.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Verification of compliance with a limit value",
            field_code="lca_limit_value_compliance",
            description="Whether the result is calculated for the verification of compliance with a limit value rather than as a complete assessment.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_limit_value_scope_reduction: Optional[LimitValueScopeReduction] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(LimitValueScopeReduction),
        description="The parts of life-cycle stages and of the scope of building components left out for the verification of compliance with a limit value.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Parts left out for the verification of compliance",
            field_code="lca_limit_value_scope_reduction",
            description="The parts of life-cycle stages and of the scope of building components left out for the verification of compliance with a limit value.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III,
        ),
    )

    lca_emission_factor_scenario: Optional[EmissionFactorScenario] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(EmissionFactorScenario),
        description="The forward-looking emission factor scenario applied over the study period",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Emission factor scenario",
            field_code="lca_emission_factor_scenario",
            description="The forward-looking emission factor scenario applied over the study period",
            constraint="max 200 characters",
            requirements="Recommended",
            criticality="SHOULD",
            reference=Reference.EN15978_2026_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    lca_lci_modeling_approach: Optional[LCIModelingApproach] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(LCIModelingApproach),
        description="Type of Life Cycle Inventory (LCI) Modeling Approach",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCI modeling approach",
            field_code="lca_lci_modeling_approach",
            description="Type of Life Cycle Inventory (LCI) Modeling Approach",
            requirements="Optional",
            criticality="SHOULD",
            example="Process-based",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_cycle_system_boundary: LifeCycleSystemBoundary = Field(  # type: ignore[call-overload]
        sa_type=SAEnum(LifeCycleSystemBoundary),
        description="Life-cycle modules included in the assessment.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Life cycle system boundary",
            field_code="lca_cycle_system_boundary",
            description="Life-cycle modules included in the assessment.",
            requirements="Required",
            criticality="MUST",
            example="Cradle to Gate with Options (A1–A3 + others)",
            reference=Reference.EN15978_2026_REGULATION_EU_2026_52_ANNEX_III,
        ),
    )

    lcia_methodology: Optional[LCIAMethodology] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(LCIAMethodology),
        description="Impact assessment method (for GHG emissions, GWP indicator).",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCIA Methodology",
            field_code="lcia_methodology",
            description="Impact assessment method (for GHG emissions, GWP indicator).",
            requirements="Required",
            criticality="SHOULD",
            example="EN 15804+A2 (EF 3.0) - Current EU standard",
            reference=Reference.EN15804_A2_EN15804_A1_TRACI,
        ),
    )

    lca_biogenic_method: Optional[BiogenicCarbonAccounting] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(BiogenicCarbonAccounting),
        description="Method used for biogenic carbon accounting.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Biogenic Carbon Accounting Method",
            field_code="lca_biogenic_method",
            description="Method used for biogenic carbon accounting.",
            requirements="Recommended",
            criticality="SHOULD",
            example="-1/+1;",
            reference=Reference.EN15978_2026,
        ),
    )

    lca_biogenic_carbon: Optional[bool] = Field(
        default=None,
        description="Biogenic carbon included in assessment.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Biogenic Carbon",
            field_code="lca_biogenic_carbon",
            description="Biogenic carbon included in assessment.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.ECHO,
        ),
    )

    lca_material_source: Optional[MaterialQuantitiesSource] = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=SAEnum(MaterialQuantitiesSource),
        description="Main source of material quantities.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="LCA Material Quantities Source",
            field_code="lca_material_source",
            description="Main source of material quantities.",
            requirements="Required",
            criticality="SHOULD",
            example="BIM Model",
            reference=Reference.ECHO,
        ),
    )

    lca_gwp_total_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_total_a1_a3 to gwp_total_c4, and the whole-life sum by gwp_total_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Global Warming Potential - Total",
            field_code="lca_gwp_total_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_total_a1_a3 to gwp_total_c4, and the whole-life sum by gwp_total_total.",
            requirements="Required",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_gwp_f_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_f_a1_a3 to gwp_f_c4, and the whole-life sum by gwp_f_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Global Warming Potential - Fossil",
            field_code="lca_gwp_f_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_f_a1_a3 to gwp_f_c4, and the whole-life sum by gwp_f_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_gwp_b_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_b_a1_a3 to gwp_b_c4, and the whole-life sum by gwp_b_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Global Warming Potential - Biogenic",
            field_code="lca_gwp_b_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_b_a1_a3 to gwp_b_c4, and the whole-life sum by gwp_b_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_gwp_luc_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_luc_a1_a3 to gwp_luc_c4, and the whole-life sum by gwp_luc_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Global Warming Potential - Land Use and Land Use Change",
            field_code="lca_gwp_luc_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns gwp_luc_a1_a3 to gwp_luc_c4, and the whole-life sum by gwp_luc_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_odp_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns odp_a1_a3 to odp_c4, and the whole-life sum by odp_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Ozone Depletion Potential",
            field_code="lca_odp_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns odp_a1_a3 to odp_c4, and the whole-life sum by odp_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_ap_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ap_a1_a3 to ap_c4, and the whole-life sum by ap_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Acidification potential",
            field_code="lca_ap_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ap_a1_a3 to ap_c4, and the whole-life sum by ap_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_ap_ae_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ep_a1_a3 to ep_c4, and the whole-life sum by ep_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Acidification Potential - Accumulated Exceedance",
            field_code="lca_ap_ae_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ep_a1_a3 to ep_c4, and the whole-life sum by ep_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_TRACI,
        ),
    )

    lca_ep_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ep_a1_a3 to ep_c4, and the whole-life sum by ep_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Eutrophication Potential",
            field_code="lca_ep_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ep_a1_a3 to ep_c4, and the whole-life sum by ep_total.",
            requirements="Recommended",
            criticality="MAY",
            example="No",
            reference=Reference.EN15804_A1_TRACI,
        ),
    )

    lca_ep_af_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ep_af_a1_a3 to ep_af_c4, and the whole-life sum by ep_af_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Eutrophication Potential - Aquatic Freshwater",
            field_code="lca_ep_af_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ep_af_a1_a3 to ep_af_c4, and the whole-life sum by ep_af_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_ep_am_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ep_am_a1_a3 to ep_am_c4, and the whole-life sum by ep_am_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Eutrophication Potential - Aquatic Marine",
            field_code="lca_ep_am_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ep_am_a1_a3 to ep_am_c4, and the whole-life sum by ep_am_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_ep_t_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns ep_t_a1_a3 to ep_t_c4, and the whole-life sum by ep_t_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Eutrophication Potential - Terrestrial",
            field_code="lca_ep_t_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns ep_t_a1_a3 to ep_t_c4, and the whole-life sum by ep_t_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_pocp_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns pocp_a1_a3 to pocp_c4, and the whole-life sum by pocp_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Photochemical Ozone Creation Potential",
            field_code="lca_pocp_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns pocp_a1_a3 to pocp_c4, and the whole-life sum by pocp_total.",
            requirements="Recommended",
            criticality="MAY",
            example="No",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_sfp_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns sfp_a1_a3 to sfp_c4, and the whole-life sum by sfp_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Smog Forming Potential",
            field_code="lca_sfp_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns sfp_a1_a3 to sfp_c4, and the whole-life sum by sfp_total.",
            requirements="Recommended",
            criticality="MAY",
            example="No",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_pofp_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns pofp_a1_a3 to pofp_c4, and the whole-life sum by pofp_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Photochemical Ozone Formation Potential",
            field_code="lca_pofp_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns pofp_a1_a3 to pofp_c4, and the whole-life sum by pofp_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_adpmm_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns adpmm_a1_a3 to adpmm_c4, and the whole-life sum by adpmm_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Abiotic Depletion Potential (Minerals and Metals)",
            field_code="lca_adpmm_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns adpmm_a1_a3 to adpmm_c4, and the whole-life sum by adpmm_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_adpf_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns adpf_a1_a3 to adpf_c4, and the whole-life sum by adpf_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Abiotic Depletion Potential (Fossil Fuels)",
            field_code="lca_adpf_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns adpf_a1_a3 to adpf_c4, and the whole-life sum by adpf_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026_TRACI,
        ),
    )

    lca_wdp_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns wdp_a1_a3 to wdp_c4, and the whole-life sum by wdp_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Water deprivation potential (deprivation-weighted water consumption)",
            field_code="lca_wdp_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns wdp_a1_a3 to wdp_c4, and the whole-life sum by wdp_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A2_EN15978_2026,
        ),
    )

    lca_pere_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns pere_a1_a3 to pere_c4, and the whole-life sum by pere_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Primary Energy Renewable (Energy resources)",
            field_code="lca_pere_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns pere_a1_a3 to pere_c4, and the whole-life sum by pere_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_penre_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns penre_a1_a3 to penre_c4, and the whole-life sum by penre_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Primary Energy Non-Renewable (Energy resources)",
            field_code="lca_penre_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns penre_a1_a3 to penre_c4, and the whole-life sum by penre_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_pert_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns pert_a1_a3 to pert_c4, and the whole-life sum by pert_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Primary Energy Renewable Total",
            field_code="lca_pert_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns pert_a1_a3 to pert_c4, and the whole-life sum by pert_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_penrt_declared: Optional[bool] = Field(
        default=None,
        description="Whether this indicator was assessed. The value itself is carried by the result columns penrt_a1_a3 to penrt_c4, and the whole-life sum by penrt_total.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Primary Energy Non-Renewable Total",
            field_code="lca_penrt_declared",
            description="Whether this indicator was assessed. The value itself is carried by the result columns penrt_a1_a3 to penrt_c4, and the whole-life sum by penrt_total.",
            requirements="Recommended",
            criticality="MAY",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_pm_declared: Optional[bool] = Field(
        default=None,
        description="Total particulate matter emissions over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Particulate Matter Emissions",
            field_code="lca_pm_declared",
            description="Total particulate matter emissions over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_irp_declared: Optional[bool] = Field(
        default=None,
        description="Total ionising radiation, human health over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Ionising Radiation - Human Health",
            field_code="lca_irp_declared",
            description="Total ionising radiation, human health over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_etp_fw_declared: Optional[bool] = Field(
        default=None,
        description="Total ecotoxicity, freshwater over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Ecotoxicity - Freshwater",
            field_code="lca_etp_fw_declared",
            description="Total ecotoxicity, freshwater over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_htp_c_declared: Optional[bool] = Field(
        default=None,
        description="Total human toxicity, cancer over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Human Toxicity - Cancer Effects",
            field_code="lca_htp_c_declared",
            description="Total human toxicity, cancer over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_htp_nc_declared: Optional[bool] = Field(
        default=None,
        description="Total human toxicity, non-cancer over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Human Toxicity - Non-cancer Effects",
            field_code="lca_htp_nc_declared",
            description="Total human toxicity, non-cancer over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_sqp_declared: Optional[bool] = Field(
        default=None,
        description="Total land use related soil quality over modules A to C, excluding module D.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="Soil Quality Index",
            field_code="lca_sqp_declared",
            description="Total land use related soil quality over modules A to C, excluding module D.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15804_A1_A2_EN15978_2026,
        ),
    )

    lca_a1_3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A1-A3: Product Stage",
            field_code="lca_a1_3",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15804_A1_A2_EN15978_EN15978_2026,
        ),
    )

    lca_a1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A1 Raw Material Supply",
            field_code="lca_a1",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="No",
            reference=Reference.EN15804_EN15978_EN15978_2026,
        ),
    )

    lca_a2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A2 Transport",
            field_code="lca_a2",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="No",
            reference=Reference.EN15804_EN15978_EN15978_2026,
        ),
    )

    lca_a3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A3 Manufacturing",
            field_code="lca_a3",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="No",
            reference=Reference.EN15804_EN15978_EN15978_2026,
        ),
    )

    lca_a4: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A4 Transport",
            field_code="lca_a4",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026_RICS_WLCA,
        ),
    )

    lca_a5: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5 Construction/Installation: Installation of the product into the building",
            field_code="lca_a5",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026_RICS_WLCA,
        ),
    )

    lca_a5_1: Optional[bool] = Field(
        default=None,
        description="Life cycle sub-module included. Pre-construction demolition and site clearance.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5.1 Pre-construction demolition",
            field_code="lca_a5_1",
            description="Life cycle sub-module included. Pre-construction demolition and site clearance.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_2026_RICS_WLCA,
        ),
    )

    lca_a5_2: Optional[bool] = Field(
        default=None,
        description="Life cycle sub-module included. On-site construction and installation activities.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5.2 Construction activities",
            field_code="lca_a5_2",
            description="Life cycle sub-module included. On-site construction and installation activities.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_2026_RICS_WLCA,
        ),
    )

    lca_a5_3: Optional[bool] = Field(
        default=None,
        description="Life cycle sub-module included. Construction waste and its management.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5.3 Waste and waste management",
            field_code="lca_a5_3",
            description="Life cycle sub-module included. Construction waste and its management.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_2026_RICS_WLCA,
        ),
    )

    lca_a5_4: Optional[bool] = Field(
        default=None,
        description="Life cycle sub-module included. Transport of workers to and from the site.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="A5.4 Worker transport",
            field_code="lca_a5_4",
            description="Life cycle sub-module included. Transport of workers to and from the site.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_2026_RICS_WLCA,
        ),
    )

    lca_b1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B1 Use: Environmental impacts arising from the product in use (eg, release of substances)",
            field_code="lca_b1",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b1_1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Emissions from materials and carbonation within module B1.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B1.1 Emissions from materials and carbonation",
            field_code="lca_b1_1",
            description="Life cycle module included. Emissions from materials and carbonation within module B1.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b1_2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Fugitive emissions of refrigerants within module B1.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B1.2 Fugitive emissions of refrigerants",
            field_code="lca_b1_2",
            description="Life cycle module included. Fugitive emissions of refrigerants within module B1.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B2 Maintenance: Actions to maintain the product's functional quality (cleaning, painting)",
            field_code="lca_b2",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B3 Repair: Corrective actions to return the product to a functional state",
            field_code="lca_b3",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b4: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B4 Replacement: Replacing the product or parts of it at the end of its service life",
            field_code="lca_b4",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b5: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B5 Refurbishment: Major changes to restore or improve performance",
            field_code="lca_b5",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b6: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B6 Operational Energy Use: Energy consumption related to the building's operation (heating, cooling, lighting)",
            field_code="lca_b6",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b6_1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Operational energy of regulated building-integrated systems.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B6.1 Regulated building-integrated systems",
            field_code="lca_b6_1",
            description="Life cycle module included. Operational energy of regulated building-integrated systems.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b6_2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Operational energy of non-regulated building-integrated systems.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B6.2 Non-regulated building-integrated systems",
            field_code="lca_b6_2",
            description="Life cycle module included. Operational energy of non-regulated building-integrated systems.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b6_3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Other operational energy related to building user activities.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B6.3 Other energy use related to user activities",
            field_code="lca_b6_3",
            description="Life cycle module included. Other operational energy related to building user activities.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b7: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B7 Operational Water Use: Water consumption related to the building's operation",
            field_code="lca_b7",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_b7_1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Operational water of essential building-integrated systems.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B7.1 Essential building-integrated systems",
            field_code="lca_b7_1",
            description="Life cycle module included. Operational water of essential building-integrated systems.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b7_2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Operational water of other building-integrated systems.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B7.2 Other building-integrated systems",
            field_code="lca_b7_2",
            description="Life cycle module included. Operational water of other building-integrated systems.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b7_3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Operational water of non-building-integrated systems.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B7.3 Non-building-integrated systems",
            field_code="lca_b7_3",
            description="Life cycle module included. Operational water of non-building-integrated systems.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b8: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Building-integrated users activities not covered by B1 to B7. Optional stage.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B8 Building-integrated users activities",
            field_code="lca_b8",
            description="Life cycle module included. Building-integrated users activities not covered by B1 to B7. Optional stage.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b8_1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Transport of persons to and from the building.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B8.1 Transport of persons",
            field_code="lca_b8_1",
            description="Life cycle module included. Transport of persons to and from the building.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b8_2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Charging of electric vehicles within the building site.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B8.2 Charging of electric vehicles",
            field_code="lca_b8_2",
            description="Life cycle module included. Charging of electric vehicles within the building site.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_b8_3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included. Other user activities, such as consumables and unfixed furniture.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="B8.3 Other user activities",
            field_code="lca_b8_3",
            description="Life cycle module included. Other user activities, such as consumables and unfixed furniture.",
            requirements="Optional",
            criticality="MAY",
            reference=Reference.EU2026_52_ANNEX_III_EN15978_2026,
        ),
    )

    lca_c1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C1 De-construction/Demolition: Dismantling or demolishing the building/product",
            field_code="lca_c1",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_c2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C2 Transport: Transporting the waste to processing or disposal sites",
            field_code="lca_c2",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_c3: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C3 Waste Processing: Processing waste for reuse, recovery, or recycling",
            field_code="lca_c3",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_c4: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="C4 Disposal: Final disposal of waste that cannot be recovered (eg, landfill)",
            field_code="lca_c4",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_d: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="D Benefits and Loads Beyond the System Boundary",
            field_code="lca_d",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_d1: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="D1 Reuse, Recovery, and Recycling Potential: Net benefits or loads resulting from reusing or recycling materials (avoided emissions)",
            field_code="lca_d1",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )

    lca_d2: Optional[bool] = Field(
        default=None,
        description="Life cycle module included.",
        schema_extra=openbdf_field_metadata(
            group="LCA",
            sub_group="LCA impact assessment",
            attribute_name="D2 Exported Energy (or Energy Recovery Potential)",
            field_code="lca_d2",
            description="Life cycle module included.",
            requirements="Recommended",
            criticality="SHOULD",
            example="Yes",
            reference=Reference.EN15978_EN15978_2026,
        ),
    )


_ProjectRecordBaseDraft = make_draft_model(ProjectRecordBase)


class ProjectRecordBaseDraft(_ProjectRecordBaseDraft):  # type: ignore[valid-type,misc]
    pass
