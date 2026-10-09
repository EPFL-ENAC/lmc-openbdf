from .openbdf_enum import OpenBDFEnum


class RecordType(OpenBDFEnum):
    REAL_BUILDING = (
        "real_building",
        "real building (a building that exists or is being built)",
        "a building that exists or is being built",
    )
    ARCHETYPE = (
        "archetype",
        "archetype (a representative building of a stock model)",
        "a representative building of a stock model",
    )
    DESIGN_VARIANT = (
        "design_variant",
        "design variant (an alternative design of the same building)",
        "an alternative design of the same building",
    )
    PARAMETRIC_SCENARIO = (
        "parametric_scenario",
        "parametric scenario (a generated variation)",
        "a generated variation",
    )


class ProjectPhase(OpenBDFEnum):
    RIBA_UK_0 = ("RIBA_UK_0_StrategicDefinition", "RIBA_UK_0_StrategicDefinition")
    RIBA_UK_1 = ("RIBA_UK_1_PreparationAndBriefing", "RIBA_UK_1_PreparationAndBriefing")
    RIBA_UK_2 = ("RIBA_UK_2_ConceptDesign", "RIBA_UK_2_ConceptDesign")
    RIBA_UK_3 = ("RIBA_UK_3_SpatialCoordination", "RIBA_UK_3_SpatialCoordination")
    RIBA_UK_4 = ("RIBA_UK_4_TechnicalDesign", "RIBA_UK_4_TechnicalDesign")
    RIBA_UK_5 = ("RIBA_UK_5_ManufacturingAndConstruction", "RIBA_UK_5_ManufacturingAndConstruction")
    RIBA_UK_6 = ("RIBA_UK_6_Handover", "RIBA_UK_6_Handover")
    RIBA_UK_7 = ("RIBA_UK_7_Use", "RIBA_UK_7_Use")
    HOAI_DE_LP1 = ("HOAI_DE_LP1_Grundlagenermittlung", "HOAI_DE_LP1_Grundlagenermittlung")
    HOAI_DE_LP2 = ("HOAI_DE_LP2_Vorplanung", "HOAI_DE_LP2_Vorplanung")
    HOAI_DE_LP3 = ("HOAI_DE_LP3_Entwurfsplanung", "HOAI_DE_LP3_Entwurfsplanung")
    HOAI_DE_LP4 = ("HOAI_DE_LP4_Genehmigungsplanung", "HOAI_DE_LP4_Genehmigungsplanung")
    HOAI_DE_LP5 = ("HOAI_DE_LP5_Ausfuehrungsplanung", "HOAI_DE_LP5_Ausfuehrungsplanung")
    HOAI_DE_LP6 = ("HOAI_DE_LP6_VorbereitungDerVergabe", "HOAI_DE_LP6_VorbereitungDerVergabe")
    HOAI_DE_LP7 = ("HOAI_DE_LP7_MitwirkungBeiDerVergabe", "HOAI_DE_LP7_MitwirkungBeiDerVergabe")
    HOAI_DE_LP8 = ("HOAI_DE_LP8_Objektueberwachung", "HOAI_DE_LP8_Objektueberwachung")
    HOAI_DE_LP9 = ("HOAI_DE_LP9_Objektbetreuung", "HOAI_DE_LP9_Objektbetreuung")
    AIA_US_SD = ("AIA_US_SD_SchematicDesign", "AIA_US_SD_SchematicDesign")
    AIA_US_DD = ("AIA_US_DD_DesignDevelopment", "AIA_US_DD_DesignDevelopment")
    AIA_US_CD = ("AIA_US_CD_ConstructionDocuments", "AIA_US_CD_ConstructionDocuments")
    AIA_US_BN = ("AIA_US_BN_BiddingNegotiation", "AIA_US_BN_BiddingNegotiation")
    AIA_US_CA = ("AIA_US_CA_ConstructionAdministration", "AIA_US_CA_ConstructionAdministration")
    SIA_CH_1 = ("SIA_CH_1_StrategischePlanung", "SIA_CH_1_StrategischePlanung")
    SIA_CH_2 = ("SIA_CH_2_Vorstudien", "SIA_CH_2_Vorstudien")
    SIA_CH_3 = ("SIA_CH_3_Projektierung", "SIA_CH_3_Projektierung")
    SIA_CH_4 = ("SIA_CH_4_Ausschreibung", "SIA_CH_4_Ausschreibung")
    SIA_CH_5 = ("SIA_CH_5_Realisierung", "SIA_CH_5_Realisierung")
    SIA_CH_6 = ("SIA_CH_6_Bewirtschaftung", "SIA_CH_6_Bewirtschaftung")
    GBDI_END_OF_USE = ("GBDI_EndOfUse", "GBDI_EndOfUse")
    OTHER_NATIONAL = ("Other_National", "Other_National")


class ProjectPhaseCommon(OpenBDFEnum):
    PHASE_0 = ("0 Strategic definition", "0 Strategic definition")
    PHASE_1 = ("1 Preliminary studies", "1 Preliminary studies")
    PHASE_2 = ("2 Concept design", "2 Concept design")
    PHASE_3 = ("3 Developed design", "3 Developed design")
    PHASE_4 = ("4 Technical design", "4 Technical design")
    PHASE_5 = ("5 Manufacturing and construction", "5 Manufacturing and construction")
    PHASE_6 = ("6 Handover and commissioning", "6 Handover and commissioning")
    PHASE_7 = ("7 Operation and management", "7 Operation and management")
    PHASE_8 = ("8 End of use, re-cycling", "8 End of use, re-cycling")


class ConstructionType(OpenBDFEnum):
    NEW_CONSTRUCTION = ("new_construction", "New Construction")
    TENANT_IMPROVEMENT = ("tenant_improvement", "Tenant Improvements")
    MINOR_RENOVATION = (
        "minor_renovation",
        "Minor Renovation (without addition)",
    )
    MAJOR_RENOVATION = (
        "major_renovation",
        "Major Renovation (with addition)",
    )


class ProjectUnits(OpenBDFEnum):
    IMPERIAL = ("imperial", "Imperial Units System (IP, USA)")
    METRIC = ("metric", "Metric, International Units System (SI)")
