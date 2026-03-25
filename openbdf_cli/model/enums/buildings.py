from .openbdf_enum import OpenBDFEnum


class BuildingTypology(OpenBDFEnum):
    SFH = ("sfh", "Single family houses (SFH)")
    MFH = ("mfh", "Multifamily houses (MFH)")
    ABL = ("abl", "Apartment blocks (ABL)")
    OFF = ("off", "Offices (OFF)")
    TRA = ("tra", "Trade (TRA)")
    EDU = ("edu", "Education (EDU)")
    HEA = ("hea", "Health (HEA)")
    HOR = ("hor", "Hotels and Restaurants (HOR)")
    OTH = ("oth", "Other non-residential buildings (OTH)")


class RoofType(OpenBDFEnum):
    FLAT = ("flat", "Flat roof")
    SINGLE_PITCHED = ("single_pitched", "Single pitched roof")
    GABLE_SADDLE = ("gable_saddle", "Gable or saddle roof")
    PYRAMID = ("pyramid", "Pyramid roof")


class AboveBelowGround(OpenBDFEnum):
    ABOVE = ("above", "Above ground")
    BELOW = ("below", "Below ground")


class BuildingFacingDirection(OpenBDFEnum):
    NORTH = ("N", "North", "North-facing")
    SOUTH = ("S", "South", "South-facing")
    EAST = ("E", "East", "East-facing")
    WEST = ("W", "West", "West-facing")
    NORTH_EAST = ("NE", "Northeast", "Northeast-facing")
    NORTH_WEST = ("NW", "Northwest", "Northwest-facing")
    SOUTH_EAST = ("SE", "Southeast", "Southeast-facing")
    SOUTH_WEST = ("SW", "Southwest", "Southwest-facing")


class FoundationType(OpenBDFEnum):
    # EN1997 Foundations
    EN1997_PAD_FOOTINGS = (
        "en1997_pad_footings",
        "EN1997 - Pad Footings (Isolated)",
        "Spread foundation - Pad Footings (Isolated) according to Eurocode 7.",
    )
    EN1997_STRIP_FOOTINGS = (
        "en1997_strip_footings",
        "EN1997 - Strip Footings (Continuous)",
        "Spread foundation - Strip Footings (Continuous) according to Eurocode 7.",
    )
    EN1997_RAFT_FOUNDATIONS = (
        "en1997_raft_foundations",
        "EN1997 - Raft Foundations (Mat)",
        "Spread foundation - Raft Foundations (Mat) according to Eurocode 7.",
    )
    EN1997_DISPLACEMENT_PILES = (
        "en1997_displacement_piles",
        "EN1997 - Displacement Piles (Driven)",
        "Piled Foundations - Displacement Piles (Driven) according to Eurocode 7.",
    )
    EN1997_REPLACEMENT_PILES = (
        "en1997_replacement_piles",
        "EN1997 - Replacement Piles (Bored/Drilled)",
        "Piled Foundations - Replacement Piles (Bored/Drilled) according to Eurocode 7.",
    )
    EN1997_RETAINING_WALLS = (
        "en1997_retaining_walls",
        "EN1997 - Retaining Walls",
        "Other Geotechnical Structures - Retaining Walls according to Eurocode 7.",
    )
    EN1997_DEEP_SHAFTS = (
        "en1997_deep_shafts",
        "EN1997 - Deep Shafts (Caissons)",
        "Other Geotechnical Structures - Deep Shafts (Caissons) according to Eurocode 7.",
    )
    EN1997_GROUND_ANCHORS = (
        "en1997_ground_anchors",
        "EN1997 - Ground Anchors",
        "Other Geotechnical Structures - Ground Anchors according to Eurocode 7.",
    )

    # IBC Foundations
    IBC_ISOLATED_FOOTINGS = (
        "ibc_isolated_footings",
        "IBC - Isolated (Spread) Footings",
        "Shallow Foundations - Isolated (Spread) Footings according to IBC Chapter 18.",
    )
    IBC_COMBINED_FOOTINGS = (
        "ibc_combined_footings",
        "IBC - Combined Footings",
        "Shallow Foundations - Combined Footings according to IBC Chapter 18.",
    )
    IBC_STRIP_FOOTINGS = (
        "ibc_strip_footings",
        "IBC - Strip / Continuous Footings",
        "Shallow Foundations - Strip / Continuous Footings according to IBC Chapter 18.",
    )
    IBC_RAFT_FOUNDATIONS = (
        "ibc_raft_foundations",
        "IBC - Raft / Mat Foundations",
        "Shallow Foundations - Raft / Mat Foundations according to IBC Chapter 18.",
    )
    IBC_SLAB_ON_GRADE = (
        "ibc_slab_on_grade",
        "IBC - Slab‑on‑Grade Foundations",
        "Shallow Foundations - Slab‑on‑Grade Foundations according to IBC Chapter 18.",
    )
    IBC_DRIVEN_PILES = (
        "ibc_driven_piles",
        "IBC - Driven Piles",
        "Deep Foundations - Driven Piles according to IBC Chapter 18.",
    )
    IBC_DRILLED_SHAFTS = (
        "ibc_drilled_shafts",
        "IBC - Drilled Shafts / Caissons",
        "Deep Foundations - Drilled Shafts / Caissons according to IBC Chapter 18.",
    )
    IBC_PIERS = (
        "ibc_piers",
        "IBC - Piers",
        "Deep Foundations - Piers according to IBC Chapter 18.",
    )
    IBC_FROST_PROTECTED = (
        "ibc_frost_protected",
        "IBC - Frost‑Protected Foundations",
        "Specialized Foundations - Frost‑Protected Foundations according to IBC Chapter 18.",
    )
    IBC_SOIL_SPECIFIC = (
        "ibc_soil_specific",
        "IBC - Soil‑Specific Foundations",
        "Specialized Foundations - Soil‑Specific Foundations (Clay, Sand, Silt, Rock) according to IBC Chapter 18.",
    )


# Gross Floor Area (GFA) Measurement Methods
class GFAMeasurementMethod(OpenBDFEnum):
    IPMS = (
        "ipms",
        "IPMS",
        "International Property Measurement Standards. Global standard used to unify how buildings are measured worldwide.",
    )
    RICS = (
        "rics",
        "RICS Measurement Standards",
        "UK-based but internationally used rules for measuring buildings. Often aligned with IPMS.",
    )
    ANSI = (
        "ansi",
        "ANSI Standards (USA)",
        "US national standard for measuring residential and commercial floor area. Defines how total area should be measured.",
    )
    BOMA = (
        "boma",
        "BOMA Gross Area Methods (1–5)",
        "Widely used in global commercial real estate; includes methods for leasing, international comparison, construction, volumetric measurement, and ENERGY STAR® compatibility.",
    )
    CBPS = (
        "cbps",
        "CBPS GFA Method (Washington State, USA)",
        "Regulatory method measuring GFA from exterior wall surfaces for energy compliance.",
    )
    INSTITUTIONAL = (
        "institutional",
        "Institutional Methods (GBA, UFA, NLA, FECA)",
        "Used by universities and facility managers; define gross, usable, and net areas on campuses.",
    )
    PLAN_BASED = (
        "plan_based",
        "Plan-Based Measurement",
        "Practical methods used globally: measuring onsite or using architectural floor plans to calculate GFA.",
    )


class GrossFloorAreaStandard(OpenBDFEnum):
    ABNT_NBR_12721 = (
        "abnt_nbr_12721",
        "Área Real Global",
        "ABNT NBR 12.721 (Brazil), Área Real Global / Área Construída",
    )
    BOMA_Z65_3 = (
        "boma_z65_3",
        "GBA (BOMA)",
        "BOMA Z65.3 / CSA Z249 (Canada), Gross Building Area (GBA)",
    )
    JAPAN_BSA = (
        "japan_bsa",
        "Nobe-yuka-menseki",
        "Building Standards Act (Japan), Nobe-yuka-menseki (Total Floor Area)",
    )
    HK_BD = (
        "hk_bd",
        "GFA (Hong Kong)",
        "Buildings Department (Hong Kong), Gross Floor Area (GFA)",
    )
    FRANCE_SDP = (
        "france_sdp",
        "Surface de Plancher (SDP)",
        "Code de l'urbanisme (France), Surface de Plancher (SDP)",
    )
    DIN_277 = (
        "din_277",
        "Brutto-Grundfläche (BGF)",
        "DIN 277 (Germany), Brutto-Grundfläche (BGF)",
    )
    DUBAI_RICS = (
        "dubai_rics",
        "GFA (Dubai)",
        "Dubai Land Department / RICS (UAE), Gross Floor Area (GFA)",
    )
    CHINA_GBT = (
        "china_gbt",
        "Jianzhu Mianji",
        "GB/T 50353 (China), Gross Floor Area (GFA) / Jianzhu Mianji",
    )
    IPMS_1 = (
        "ipms_1",
        "IPMS 1 / GBA",
        "IPMS 1 / BOMA (International / USA), Gross Building Area (GBA)",
    )
    ARGENTINA_IRAM = (
        "argentina_iram",
        "Superficie Cubierta Total",
        "IRAM (Argentina), Superficie Cubierta Total",
    )
    INDIA_RERA = (
        "india_rera",
        "Plinth / Super Built-up Area",
        "IS 3861 / RERA (India), Plinth Area / Super Built-up Area",
    )
    SAUDI_SBC = (
        "saudi_sbc",
        "Total Built-up Area (TBA)",
        "MOMRA / Saudi Building Code (Saudi Arabia), Total Built-up Area (TBA)",
    )
    PHILIPPINES_NBC = (
        "philippines_nbc",
        "GFA (Philippines)",
        "NBC (Philippines), Gross Floor Area (GFA)",
    )
    NEN_2580 = (
        "nen_2580",
        "Bruto Vloeroppervlak (BVO)",
        "NEN 2580 (Netherlands), Bruto Vloeroppervlak (BVO)",
    )
    NS_3940 = (
        "ns_3940",
        "Bruttoareal (BTA)",
        "NS 3940 (Norway), Bruttoareal (BTA)",
    )
    ONORM_B_1800 = (
        "onorm_b_1800",
        "Brutto-Grundfläche (BGF)",
        "ÖNORM B 1800 (Austria), Brutto-Grundfläche (BGF)",
    )
    AUSTRALIA_PCA = (
        "australia_pca",
        "GFA (Australia)",
        "Property Council of Australia (Australia), Gross Floor Area (GFA)",
    )
    VIETNAM_QCVN = (
        "vietnam_qcvn",
        "Dien tich san",
        "QCVN 03:2012/BXD (Vietnam), Gross Floor Area (GFA) / Dien tich san",
    )
    SPAIN_RD_1020 = (
        "spain_rd_1020",
        "Superficie Construida",
        "Real Decreto 1020/1993 (Spain), Superficie Construida",
    )
    MEXICO_REGLAMENTO = (
        "mexico_reglamento",
        "Superficie de Construcción",
        "Reglamento de Construcciones (Mexico), Superficie de Construcción",
    )
    RICS_UK_TYPE_1 = (
        "rics_uk_type_1",
        "GEA (RICS Type 1)",
        "RICS (UK), Type 1: GEA (Gross External Area)",
    )
    RICS_UK_TYPE_2 = (
        "rics_uk_type_2",
        "GIA (RICS Type 2)",
        "RICS (UK), Type 2: GIA (Gross Internal Area)",
    )
    SANS_10400 = (
        "sans_10400",
        "GFA (South Africa)",
        "SANS 10400 (South Africa), Gross Floor Area (GFA)",
    )
    SFS_5139 = (
        "sfs_5139",
        "Bruttoala (BrlA)",
        "SFS 5139 (Finland), Bruttoala (BrlA)",
    )
    SIA_416 = (
        "sia_416",
        "BGF / SPB",
        "SIA 416 (Switzerland), Bruttogeschossfläche (BGF) / Surface de plancher brute (SPB)",
    )
    INDONESIA_SNI = (
        "indonesia_sni",
        "Luas Lantai Bangunan",
        "SNI 03-1728 (Indonesia), Luas Lantai Bangunan (Building Floor Area)",
    )
    RUSSIA_SNIP = (
        "russia_snip",
        "Obshchaya Ploshchad",
        "SNiP / SP 54.13330 (Russia), Obshchaya Ploshchad (Total Area)",
    )
    SS_21054 = (
        "ss_21054",
        "Bruttoarea (BTA)",
        "SS 21054 (Sweden), Bruttoarea (BTA)",
    )
    TURKEY_TS_01 = (
        "turkey_ts_01",
        "Brüt Alan",
        "Turkish Standard TS 01 (Turkey), Brüt Alan (Gross Area)",
    )
    UNI_11136 = (
        "uni_11136",
        "Superficie Lorda (SL)",
        "UNI 11136 (Italy), Superficie Lorda (SL)",
    )
    URA_SINGAPORE = (
        "ura_singapore",
        "GFA (Singapore)",
        "URA (Singapore), Gross Floor Area (GFA)",
    )
