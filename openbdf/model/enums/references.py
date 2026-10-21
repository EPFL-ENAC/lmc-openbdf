"""Reference and reference alignment values taken from the OpenBDF v2.0.0 target workbook."""

from .openbdf_enum import OpenBDFEnum


class Reference(OpenBDFEnum):
    """Source or origin of a field value."""

    ANSI_ASHRAE_169_IECC_KOPPEN_GEIGER = (
        "ANSI/ASHRAE 169; IECC; Koppen-Geiger",
        "ANSI/ASHRAE 169; IECC; Koppen-Geiger",
    )
    ASHRAE_169_IECC_KOPPEN_GEIGER = (
        "ASHRAE 169; IECC; Koppen-Geiger",
        "ASHRAE 169; IECC; Koppen-Geiger",
    )
    BILL_OF_MATERIALS = (
        "Bill of Materials",
        "Bill of Materials",
    )
    CLF = (
        "CLF",
        "CLF",
    )
    ECHO = (
        "ECHO",
        "ECHO",
    )
    ECHO_GBDB = (
        "ECHO; GBDB",
        "ECHO; GBDB",
    )
    ECHO_REGULATION_EU_2026_52_ANNEX_III = (
        "ECHO; Regulation (EU) 2026/52 Annex III",
        "ECHO; Regulation (EU) 2026/52 Annex III",
    )
    EN15804_A1_A2_EN15978_EN15978_2026 = (
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2011; EN 15978:2026",
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2011; EN 15978:2026",
    )
    EN15804_A1_A2_EN15978_2026 = (
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2026",
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2026",
    )
    EN15804_A1_A2_EN15978_2026_TRACI = (
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2026; US EPA TRACI 2.1",
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; EN 15978:2026; US EPA TRACI 2.1",
    )
    EN15804_A1_TRACI = (
        "EN 15804:2012+A1:2013; US EPA TRACI 2.1",
        "EN 15804:2012+A1:2013; US EPA TRACI 2.1",
    )
    EN15804_A2 = (
        "EN 15804:2012+A2:2019",
        "EN 15804:2012+A2:2019",
    )
    EN15804_A2_EN15804_A1_TRACI = (
        "EN 15804:2012+A2:2019; EN 15804+A1; US EPA TRACI 2.1",
        "EN 15804:2012+A2:2019; EN 15804+A1; US EPA TRACI 2.1",
    )
    EN15804_A2_EN15978_2026 = (
        "EN 15804:2012+A2:2019; EN 15978:2026",
        "EN 15804:2012+A2:2019; EN 15978:2026",
    )
    EN15804_A2_EN_16449 = (
        "EN 15804:2012+A2:2019; EN 16449",
        "EN 15804:2012+A2:2019; EN 16449",
    )
    EN15804_A2_ISO_14044_2006 = (
        "EN 15804:2012+A2:2019; ISO 14044:2006",
        "EN 15804:2012+A2:2019; ISO 14044:2006",
    )
    EN15804_A2_TRACI_RECIPE_2016_IPCC_AR6 = (
        "EN 15804:2012+A2:2019; US EPA TRACI 2.1; ReCiPe 2016; IPCC AR6",
        "EN 15804:2012+A2:2019; US EPA TRACI 2.1; ReCiPe 2016; IPCC AR6",
    )
    EN15804_A2_ECOINVENT_SYSTEM_MODELS = (
        "EN 15804:2012+A2:2019; ecoinvent system models",
        "EN 15804:2012+A2:2019; ecoinvent system models",
    )
    EN15804_EN15978_EN15978_2026 = (
        "EN 15804; EN 15978:2011; EN 15978:2026",
        "EN 15804; EN 15978:2011; EN 15978:2026",
    )
    EN_15941 = (
        "EN 15941",
        "EN 15941",
    )
    EN_15941_2024 = (
        "EN 15941:2024",
        "EN 15941:2024",
    )
    EN15978_EN15978_2026 = (
        "EN 15978:2011; EN 15978:2026",
        "EN 15978:2011; EN 15978:2026",
    )
    EN15978_EN15978_2026_RICS_WLCA = (
        "EN 15978:2011; EN 15978:2026; RICS WLCA",
        "EN 15978:2011; EN 15978:2026; RICS WLCA",
    )
    EN15978_2026 = (
        "EN 15978:2026",
        "EN 15978:2026",
    )
    EN15978_2026_ECHO_GBDB = (
        "EN 15978:2026; ECHO; GBDB",
        "EN 15978:2026; ECHO; GBDB",
    )
    EN15978_2026_EN15804_A2_5_2_EU2026_52_ANNEX_III = (
        "EN 15978:2026; EN 15804:2012+A2:2019, 5.2; Regulation (EU) 2026/52, Annex III",
        "EN 15978:2026; EN 15804:2012+A2:2019, 5.2; Regulation (EU) 2026/52, Annex III",
    )
    EN15978_2026_EUROCODE_2_EN_1992 = (
        "EN 15978:2026; Eurocode 2 (EN 1992)",
        "EN 15978:2026; Eurocode 2 (EN 1992)",
    )
    EN15978_2026_ISO_14040 = (
        "EN 15978:2026; ISO 14040",
        "EN 15978:2026; ISO 14040",
    )
    EN15978_2026_ISO_21930 = (
        "EN 15978:2026; ISO 21930",
        "EN 15978:2026; ISO 21930",
    )
    EN15978_2026_RICS_WLCA = (
        "EN 15978:2026; RICS WLCA",
        "EN 15978:2026; RICS WLCA",
    )
    EN15978_2026_REGULATION_EU_2026_52_ANNEX_III = (
        "EN 15978:2026; Regulation (EU) 2026/52 Annex III",
        "EN 15978:2026; Regulation (EU) 2026/52 Annex III",
    )
    EN15978_2026_EU2026_52_ANNEX_III = (
        "EN 15978:2026; Regulation (EU) 2026/52, Annex III",
        "EN 15978:2026; Regulation (EU) 2026/52, Annex III",
    )
    EN_197_1 = (
        "EN 197-1",
        "EN 197-1",
    )
    EN_1992_1_1_ANNEX_C = (
        "EN 1992-1-1 Annex C",
        "EN 1992-1-1 Annex C",
    )
    EN_1992_EN_1993_EN_1995_EN_1996 = (
        "EN 1992; EN 1993; EN 1995; EN 1996",
        "EN 1992; EN 1993; EN 1995; EN 1996",
    )
    EN_1997 = (
        "EN 1997",
        "EN 1997",
    )
    EN_1998_FEMA_P_2082 = (
        "EN 1998; FEMA P-2082",
        "EN 1998; FEMA P-2082",
    )
    EN_206_ACI_318_CSA_A23_1 = (
        "EN 206; ACI 318; CSA A23.1",
        "EN 206; ACI 318; CSA A23.1",
    )
    EN_206_EN_10025 = (
        "EN 206; EN 10025",
        "EN 206; EN 10025",
    )
    EN_206_EN_1992_1_1_EN_10025_EN_771_EN_772_1 = (
        "EN 206; EN 1992-1-1; EN 10025; EN 771; EN 772-1",
        "EN 206; EN 1992-1-1; EN 10025; EN 771; EN 772-1",
    )
    EN_ISO_10456 = (
        "EN ISO 10456",
        "EN ISO 10456",
    )
    EN_ISO_52000_1 = (
        "EN ISO 52000-1",
        "EN ISO 52000-1",
    )
    EN_ISO_52000_1_2017 = (
        "EN ISO 52000-1:2017",
        "EN ISO 52000-1:2017",
    )
    GBDI = (
        "GBDI",
        "GBDI",
    )
    GBDI_SLICE = (
        "GBDI, SLiCe",
        "GBDI, SLiCe",
    )
    GBDI_SLICE_2 = (
        "GBDI; SLiCe",
        "GBDI; SLiCe",
    )
    IEA_EBC_ANNEX_72 = (
        "IEA EBC Annex 72",
        "IEA EBC Annex 72",
    )
    INDICATE_BUILDING_MATERIAL_CLASSIFICATION = (
        "INDICATE building material classification",
        "INDICATE building material classification",
    )
    INDICATE_MATERIALS_TAXONOMY = (
        "INDICATE materials taxonomy",
        "INDICATE materials taxonomy",
    )
    ISO_12006_2 = (
        "ISO 12006-2",
        "ISO 12006-2",
    )
    ISO_12006_2_REGULATION_EU_2026_52_ANNEX_III = (
        "ISO 12006-2; Regulation (EU) 2026/52 Annex III",
        "ISO 12006-2; Regulation (EU) 2026/52 Annex III",
    )
    ISO_12006_3_2022 = (
        "ISO 12006-3:2022",
        "ISO 12006-3:2022",
    )
    ISO_14021_2016 = (
        "ISO 14021:2016",
        "ISO 14021:2016",
    )
    ISO_14040_2006_ISO_14044_2006 = (
        "ISO 14040:2006; ISO 14044:2006",
        "ISO 14040:2006; ISO 14044:2006",
    )
    ISO_15686_1_ISO_15686_2 = (
        "ISO 15686-1; ISO 15686-2",
        "ISO 15686-1; ISO 15686-2",
    )
    ISO_15686_EN15978_2026 = (
        "ISO 15686; EN 15978:2026",
        "ISO 15686; EN 15978:2026",
    )
    ISO_3166_1_ALPHA_3 = (
        "ISO 3166-1 alpha-3",
        "ISO 3166-1 alpha-3",
    )
    ISO_6709 = (
        "ISO 6709",
        "ISO 6709",
    )
    ISO_6709_2022 = (
        "ISO 6709:2022",
        "ISO 6709:2022",
    )
    ISO_80000 = (
        "ISO 80000",
        "ISO 80000",
    )
    ISO_9836 = (
        "ISO 9836",
        "ISO 9836",
    )
    ISO_9836_2017 = (
        "ISO 9836:2017",
        "ISO 9836:2017",
    )
    ISO_9836_2017_IPMS_ALL_BUILDINGS_EU2026_52_ANNEX_III = (
        "ISO 9836:2017; IPMS All Buildings; Regulation (EU) 2026/52, Annex III",
        "ISO 9836:2017; IPMS All Buildings; Regulation (EU) 2026/52, Annex III",
    )
    ISO_9836_2017_IPMS_ONORM_B_1800_DIN_277_SIA_416 = (
        "ISO 9836:2017; IPMS; ONORM B 1800; DIN 277; SIA 416",
        "ISO 9836:2017; IPMS; ONORM B 1800; DIN 277; SIA 416",
    )
    ISO_9836_IPMS_REGULATION_EU_2026_52_ANNEX_III = (
        "ISO 9836; IPMS; Regulation (EU) 2026/52 Annex III",
        "ISO 9836; IPMS; Regulation (EU) 2026/52 Annex III",
    )
    NATIONAL_ELEMENT_CLASSIFICATION_BEC_TRANSLATOR = (
        "National element classification; BEC translator",
        "National element classification; BEC translator",
    )
    RIBA_PLAN_OF_WORK_2020_HOAI_2021_AIA_SIA_112 = (
        "RIBA Plan of Work 2020; HOAI 2021; AIA; SIA 112",
        "RIBA Plan of Work 2020; HOAI 2021; AIA; SIA 112",
    )
    RICS_WLCA_2ND_ED = (
        "RICS WLCA 2nd ed.",
        "RICS WLCA 2nd ed.",
    )
    REGULATION_EU_2026_52_ANNEX_III = (
        "Regulation (EU) 2026/52 Annex III",
        "Regulation (EU) 2026/52 Annex III",
    )
    REGULATION_EU_2026_52_ANNEX_III_TABLE_4 = (
        "Regulation (EU) 2026/52 Annex III Table 4",
        "Regulation (EU) 2026/52 Annex III Table 4",
    )
    REGULATION_EU_2026_52_ANNEX_III_EN15804 = (
        "Regulation (EU) 2026/52 Annex III; EN 15804",
        "Regulation (EU) 2026/52 Annex III; EN 15804",
    )
    REGULATION_EU_2026_52_ANNEX_III_IPMS = (
        "Regulation (EU) 2026/52 Annex III; IPMS",
        "Regulation (EU) 2026/52 Annex III; IPMS",
    )
    REGULATION_EU_2026_52_ANNEX_III_ISO_9836 = (
        "Regulation (EU) 2026/52 Annex III; ISO 9836",
        "Regulation (EU) 2026/52 Annex III; ISO 9836",
    )
    EU2026_52_ANNEX_III = (
        "Regulation (EU) 2026/52, Annex III",
        "Regulation (EU) 2026/52, Annex III",
    )
    EU2026_52_ANNEX_III_EN15804_A2 = (
        "Regulation (EU) 2026/52, Annex III; EN 15804:2012+A2:2019",
        "Regulation (EU) 2026/52, Annex III; EN 15804:2012+A2:2019",
    )
    EU2026_52_ANNEX_III_EN15978_2026 = (
        "Regulation (EU) 2026/52, Annex III; EN 15978:2026",
        "Regulation (EU) 2026/52, Annex III; EN 15978:2026",
    )
    ECOINVENT_EN15804_A2 = (
        "ecoinvent; EN 15804:2012+A2:2019",
        "ecoinvent; EN 15804:2012+A2:2019",
    )


class ReferenceAlignment(OpenBDFEnum):
    """Standard or regulation that a field aligns with."""

    EN15804_A1 = (
        "EN 15804:2012+A1:2013",
        "EN 15804:2012+A1:2013",
    )
    EN15804_A1_AND_EN15804_A2 = (
        "EN 15804:2012+A1:2013 and EN 15804:2012+A2:2019",
        "EN 15804:2012+A1:2013 and EN 15804:2012+A2:2019",
    )
    EN15804_A1_AND_TRACI = (
        "EN 15804:2012+A1:2013 and US EPA TRACI 2.1",
        "EN 15804:2012+A1:2013 and US EPA TRACI 2.1",
    )
    EN15804_A1_A2_AND_TRACI = (
        "EN 15804:2012+A1:2013, EN 15804:2012+A2:2019 and US EPA TRACI 2.1",
        "EN 15804:2012+A1:2013, EN 15804:2012+A2:2019 and US EPA TRACI 2.1",
    )
    EN15804_A1_A2_EU2026_52_ANNEX_III = (
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; Regulation (EU) 2026/52, Annex III",
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; Regulation (EU) 2026/52, Annex III",
    )
    EN15804_A1_A2_TRACI_EU2026_52_ANNEX_III = (
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
        "EN 15804:2012+A1:2013; EN 15804:2012+A2:2019; US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
    )
    EN15804_A1_EU2026_52_ANNEX_III = (
        "EN 15804:2012+A1:2013; Regulation (EU) 2026/52, Annex III",
        "EN 15804:2012+A1:2013; Regulation (EU) 2026/52, Annex III",
    )
    EN15804_A1_TRACI_EU2026_52_ANNEX_III = (
        "EN 15804:2012+A1:2013; US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
        "EN 15804:2012+A1:2013; US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
    )
    EN15804_A2 = (
        "EN 15804:2012+A2:2019",
        "EN 15804:2012+A2:2019",
    )
    EN15804_A2_EU2026_52_ANNEX_III = (
        "EN 15804:2012+A2:2019; Regulation (EU) 2026/52, Annex III",
        "EN 15804:2012+A2:2019; Regulation (EU) 2026/52, Annex III",
    )
    EN15804_A2_M3_WORLD_EQ_DEPRIVED = (
        "EN 15804:2012+A2:2019; m3 world eq deprived",
        "EN 15804:2012+A2:2019; m3 world eq deprived",
    )
    EN15804_EN15978_ISO_21930 = (
        "EN 15804; EN 15978; ISO 21930",
        "EN 15804; EN 15978; ISO 21930",
    )
    EN15978 = (
        "EN 15978",
        "EN 15978",
    )
    EN15978_EN15978_2026 = (
        "EN 15978:2011; EN 15978:2026",
        "EN 15978:2011; EN 15978:2026",
    )
    EN15978_EN15978_2027 = (
        "EN 15978:2011; EN 15978:2027",
        "EN 15978:2011; EN 15978:2027",
    )
    EN15978_EN15978_2028 = (
        "EN 15978:2011; EN 15978:2028",
        "EN 15978:2011; EN 15978:2028",
    )
    EN15978_EN15978_2029 = (
        "EN 15978:2011; EN 15978:2029",
        "EN 15978:2011; EN 15978:2029",
    )
    EN15978_ISO14040_14044 = (
        "EN 15978; ISO 14040/14044",
        "EN 15978; ISO 14040/14044",
    )
    GBDI = (
        "GBDI",
        "GBDI",
    )
    EU2026_52_ANNEX_III = (
        "Regulation (EU) 2026/52, Annex III",
        "Regulation (EU) 2026/52, Annex III",
    )
    TRACI = (
        "US EPA TRACI 2.1",
        "US EPA TRACI 2.1",
    )
    TRACI_EU2026_52_ANNEX_III = (
        "US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
        "US EPA TRACI 2.1; Regulation (EU) 2026/52, Annex III",
    )
