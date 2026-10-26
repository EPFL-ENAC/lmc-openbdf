from .openbdf_enum import OpenBDFEnum, enum_attribute
from .references import Reference


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
    reference = enum_attribute(Reference.GBDI_SLICE_2)


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
    LMVM_AT_LPH1 = ("LMVM_AT_LPH1_Grundlagenanalyse", "LMVM_AT_LPH1_Grundlagenanalyse")
    LMVM_AT_LPH2 = ("LMVM_AT_LPH2_Vorentwurf", "LMVM_AT_LPH2_Vorentwurf")
    LMVM_AT_LPH3 = ("LMVM_AT_LPH3_Entwurfsplanung", "LMVM_AT_LPH3_Entwurfsplanung")
    LMVM_AT_LPH4 = ("LMVM_AT_LPH4_Einreichplanung", "LMVM_AT_LPH4_Einreichplanung")
    LMVM_AT_LPH5 = ("LMVM_AT_LPH5_Ausfuehrungsplanung", "LMVM_AT_LPH5_Ausfuehrungsplanung")
    LMVM_AT_LPH6 = ("LMVM_AT_LPH6_Ausschreibung", "LMVM_AT_LPH6_Ausschreibung")
    LMVM_AT_LPH7 = ("LMVM_AT_LPH7_BegleitungBauausfuehrung", "LMVM_AT_LPH7_BegleitungBauausfuehrung")
    LMVM_AT_LPH8 = (
        "LMVM_AT_LPH8_OertlicheBauaufsichtDokumentation",
        "LMVM_AT_LPH8_OertlicheBauaufsichtDokumentation",
    )
    LMVM_AT_LPH9 = ("LMVM_AT_LPH9_Objektbetreuung", "LMVM_AT_LPH9_Objektbetreuung")
    MOP_FR_ESQ = ("MOP_FR_ESQ_Esquisse", "MOP_FR_ESQ_Esquisse")
    MOP_FR_DIAG = ("MOP_FR_DIAG_Diagnostic", "MOP_FR_DIAG_Diagnostic")
    MOP_FR_APS = ("MOP_FR_APS_AvantProjetSommaire", "MOP_FR_APS_AvantProjetSommaire")
    MOP_FR_APD = ("MOP_FR_APD_AvantProjetDefinitif", "MOP_FR_APD_AvantProjetDefinitif")
    MOP_FR_PRO = ("MOP_FR_PRO_EtudesProjet", "MOP_FR_PRO_EtudesProjet")
    MOP_FR_ACT = ("MOP_FR_ACT_AssistanceContratsTravaux", "MOP_FR_ACT_AssistanceContratsTravaux")
    MOP_FR_EXE = ("MOP_FR_EXE_EtudesExecution", "MOP_FR_EXE_EtudesExecution")
    MOP_FR_VISA = ("MOP_FR_VISA_VisaEtudesExecution", "MOP_FR_VISA_VisaEtudesExecution")
    MOP_FR_DET = ("MOP_FR_DET_DirectionExecutionTravaux", "MOP_FR_DET_DirectionExecutionTravaux")
    MOP_FR_AOR = (
        "MOP_FR_AOR_AssistanceOperationsReception",
        "MOP_FR_AOR_AssistanceOperationsReception",
    )
    DNRSTB_NL_1 = ("DNRSTB_NL_1_InitiatiefHaalbaarheid", "DNRSTB_NL_1_InitiatiefHaalbaarheid")
    DNRSTB_NL_2 = ("DNRSTB_NL_2_Projectdefinitie", "DNRSTB_NL_2_Projectdefinitie")
    DNRSTB_NL_3 = ("DNRSTB_NL_3_Structuurontwerp", "DNRSTB_NL_3_Structuurontwerp")
    DNRSTB_NL_4 = ("DNRSTB_NL_4_Voorontwerp", "DNRSTB_NL_4_Voorontwerp")
    DNRSTB_NL_5 = ("DNRSTB_NL_5_DefinitiefOntwerp", "DNRSTB_NL_5_DefinitiefOntwerp")
    DNRSTB_NL_6 = ("DNRSTB_NL_6_TechnischOntwerpBestek", "DNRSTB_NL_6_TechnischOntwerpBestek")
    DNRSTB_NL_7 = ("DNRSTB_NL_7_PrijsEnContractvorming", "DNRSTB_NL_7_PrijsEnContractvorming")
    DNRSTB_NL_8 = ("DNRSTB_NL_8_UitvoeringsgereedOntwerp", "DNRSTB_NL_8_UitvoeringsgereedOntwerp")
    DNRSTB_NL_9 = ("DNRSTB_NL_9_Directievoering", "DNRSTB_NL_9_Directievoering")
    DNRSTB_NL_10 = ("DNRSTB_NL_10_GebruikExploitatie", "DNRSTB_NL_10_GebruikExploitatie")
    LOE_ES_EP = ("LOE_ES_EP_EstudiosPrevios", "LOE_ES_EP_EstudiosPrevios")
    LOE_ES_AP = ("LOE_ES_AP_Anteproyecto", "LOE_ES_AP_Anteproyecto")
    LOE_ES_PB = ("LOE_ES_PB_ProyectoBasico", "LOE_ES_PB_ProyectoBasico")
    LOE_ES_PE = ("LOE_ES_PE_ProyectoEjecucion", "LOE_ES_PE_ProyectoEjecucion")
    LOE_ES_DO = ("LOE_ES_DO_DireccionObra", "LOE_ES_DO_DireccionObra")
    GBDI_END_OF_USE = ("GBDI_EndOfUse", "GBDI_EndOfUse")
    OTHER_NATIONAL = ("Other_National", "Other_National")
    reference = enum_attribute(Reference.RIBA_PLAN_OF_WORK_2020_HOAI_2021_AIA_SIA_112)


class ProjectPhaseCommon(OpenBDFEnum):
    PHASE_0 = ("0 Strategic definition", "0 Strategic definition")
    PHASE_1 = ("1 Preliminary studies", "1 Preliminary studies")
    PHASE_2 = ("2 Concept design", "2 Concept design")
    PHASE_3 = ("3 Developed design", "3 Developed design")
    PHASE_4 = ("4 Technical design", "4 Technical design")
    PHASE_5 = ("5 Manufacturing and construction", "5 Manufacturing and construction")
    PHASE_6 = ("6 Handover and commissioning", "6 Handover and commissioning")
    PHASE_7 = ("7 Operation and management", "7 Operation and management")
    PHASE_8 = ("8 End of use, recycling", "8 End of use, recycling")
    OTHER = ("other", "Other")
    reference = enum_attribute(Reference.IEA_EBC_ANNEX_72)


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
    UNKNOWN = ("unknown", "Unknown")
    reference = enum_attribute(Reference.EN15978_2026)


class ProjectUnits(OpenBDFEnum):
    IMPERIAL = ("imperial", "Imperial Units System (IP, USA)")
    METRIC = ("metric", "Metric, International Units System (SI)")
    reference = enum_attribute(Reference.ISO_80000)
