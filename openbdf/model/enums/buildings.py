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


class BuildingElementClassificationTier(OpenBDFEnum):
    TIER_1 = (
        "tier_1",
        "Element Class (Tier 1)",
        "Primary (top-level) hierarchical category of the custom or national building element classification.",
    )
    TIER_2 = (
        "tier_2",
        "Element Class (Tier 2)",
        "Secondary hierarchical category of the custom or national building element classification.",
    )
    TIER_3 = (
        "tier_3",
        "Element Class (Tier 3)",
        "The tertiary hierarchical category of the custom or national building element classification.",
    )
    TIER_4 = (
        "tier_4",
        "Element Class (Tier 4)",
        "The quaternary (lowest-level) hierarchical category of the custom or national building element classification.",
    )


class BuildingClassificationCode(OpenBDFEnum):
    US = (
        "us",
        "US - OmniClass / UniFormat / MasterFormat (CSI)",
        "Building element classification for the United States.",
    )
    CA = (
        "ca",
        "CA - OmniClass",
        "Building element classification for Canada.",
    )
    GB = (
        "gb",
        "GB - Uniclass 2015",
        "Building element classification for the United Kingdom.",
    )
    DK = (
        "dk",
        "DK - CCS (Cuneco Classification System)",
        "Building element classification for Denmark.",
    )
    SE = (
        "se",
        "SE - CoClass",
        "Building element classification for Sweden.",
    )
    FI = (
        "fi",
        "FI - Talo 2000",
        "Building element classification for Finland.",
    )
    NO = (
        "no",
        "NO - NS 3451",
        "Building element classification for Norway.",
    )
    DE = (
        "de",
        "DE - DIN 276",
        "Building element classification for Germany.",
    )
    FR = (
        "fr",
        "FR - NF P 03-001",
        "Building element classification for France.",
    )
    CH = (
        "ch",
        "CH - eBKP-H",
        "Building element classification for Switzerland.",
    )
    NL = (
        "nl",
        "NL - NL-SfB",
        "Building element classification for the Netherlands.",
    )
    AT = (
        "at",
        "AT - ÖNORM B 1801",
        "Building element classification for Austria.",
    )
    IT = (
        "it",
        "IT - UNI 8290",
        "Building element classification for Italy.",
    )
    ES = (
        "es",
        "ES - GuBIMclass",
        "Building element classification for Spain.",
    )
    AU = (
        "au",
        "AU - NATSPEC / UniFormat (AU adaptation)",
        "Building element classification for Australia.",
    )
    JP = (
        "jp",
        "JP - JCCS (Japan Construction Classification System)",
        "Building element classification for Japan.",
    )
    BR = (
        "br",
        "BR - ABNT NBR 15965",
        "Building element classification for Brazil.",
    )
    CZ = (
        "cz",
        "CZ - TSKP",
        "Building element classification for the Czech Republic.",
    )
    INT = (
        "int",
        "INT - ISO 12006-2 (international framework)",
        "International framework for classification of construction objects.",
    )


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
        "EN1997 - Spread foundation - Pad Footings (Isolated)",
        "Spread foundation - Pad Footings (Isolated) according to Eurocode 7.",
    )
    EN1997_STRIP_FOOTINGS = (
        "en1997_strip_footings",
        "EN1997 - Spread foundation - Strip Footings (Continuous)",
        "Spread foundation - Strip Footings (Continuous) according to Eurocode 7.",
    )
    EN1997_RAFT_FOUNDATIONS = (
        "en1997_raft_foundations",
        "EN1997 - Spread foundation - Raft Foundations (Mat)",
        "Spread foundation - Raft Foundations (Mat) according to Eurocode 7.",
    )
    EN1997_DISPLACEMENT_PILES = (
        "en1997_displacement_piles",
        "EN1997 - Piled Foundations - Displacement Piles (Driven)",
        "Piled Foundations - Displacement Piles (Driven) according to Eurocode 7.",
    )
    EN1997_REPLACEMENT_PILES = (
        "en1997_replacement_piles",
        "EN1997 - Piled Foundations - Replacement Piles (Bored/Drilled)",
        "Piled Foundations - Replacement Piles (Bored/Drilled) according to Eurocode 7.",
    )
    EN1997_RETAINING_WALLS = (
        "en1997_retaining_walls",
        "EN1997 - Other Geotechnical Structures - Retaining Walls",
        "Other Geotechnical Structures - Retaining Walls according to Eurocode 7.",
    )
    EN1997_DEEP_SHAFTS = (
        "en1997_deep_shafts",
        "EN1997 - Other Geotechnical Structures - Deep Shafts (Caissons)",
        "Other Geotechnical Structures - Deep Shafts (Caissons) according to Eurocode 7.",
    )
    EN1997_GROUND_ANCHORS = (
        "en1997_ground_anchors",
        "EN1997 - Other Geotechnical Structures - Ground Anchors",
        "Other Geotechnical Structures - Ground Anchors according to Eurocode 7.",
    )

    # IBC Foundations
    IBC_ISOLATED_FOOTINGS = (
        "ibc_isolated_footings",
        "IBC - Shallow Foundations - Isolated (Spread) Footings",
        "Shallow Foundations - Isolated (Spread) Footings according to IBC Chapter 18.",
    )
    IBC_COMBINED_FOOTINGS = (
        "ibc_combined_footings",
        "IBC - Shallow Foundations - Combined Footings",
        "Shallow Foundations - Combined Footings according to IBC Chapter 18.",
    )
    IBC_STRIP_FOOTINGS = (
        "ibc_strip_footings",
        "IBC - Shallow Foundations - Strip / Continuous Footings",
        "Shallow Foundations - Strip / Continuous Footings according to IBC Chapter 18.",
    )
    IBC_RAFT_FOUNDATIONS = (
        "ibc_raft_foundations",
        "IBC - Shallow Foundations - Raft / Mat Foundations",
        "Shallow Foundations - Raft / Mat Foundations according to IBC Chapter 18.",
    )
    IBC_SLAB_ON_GRADE = (
        "ibc_slab_on_grade",
        "IBC - Shallow Foundations - Slab‑on‑Grade Foundations",
        "Shallow Foundations - Slab‑on‑Grade Foundations according to IBC Chapter 18.",
    )
    IBC_DRIVEN_PILES = (
        "ibc_driven_piles",
        "IBC - Deep Foundations - Driven Piles",
        "Deep Foundations - Driven Piles according to IBC Chapter 18.",
    )
    IBC_DRILLED_SHAFTS = (
        "ibc_drilled_shafts",
        "IBC - Deep Foundations - Drilled Shafts / Caissons",
        "Deep Foundations - Drilled Shafts / Caissons according to IBC Chapter 18.",
    )
    IBC_PIERS = (
        "ibc_piers",
        "IBC - Deep Foundations - Piers",
        "Deep Foundations - Piers according to IBC Chapter 18.",
    )
    IBC_FROST_PROTECTED = (
        "ibc_frost_protected",
        "IBC - Specialized Foundations - Frost‑Protected Foundations",
        "Specialized Foundations - Frost‑Protected Foundations according to IBC Chapter 18.",
    )
    IBC_SOIL_SPECIFIC = (
        "ibc_soil_specific",
        "IBC - Specialized Foundations - Soil‑Specific Foundations (Clay, Sand, Silt, Rock)",
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
        "ABNT NBR 12.721 (Brazil), Área Real Global / Área Construída",
    )
    BOMA_Z65_3 = (
        "boma_z65_3",
        "BOMA Z65.3 / CSA Z249 (Canada), Gross Building Area (GBA)",
    )
    JAPAN_BSA = (
        "japan_bsa",
        "Building Standards Act (Japan), Nobe-yuka-menseki (Total Floor Area)",
    )
    HK_BD = (
        "hk_bd",
        "Buildings Department (Hong Kong), Gross Floor Area (GFA)",
    )
    FRANCE_SDP = (
        "france_sdp",
        "Code de l'urbanisme (France), Surface de Plancher (SDP)",
    )
    DIN_277 = (
        "din_277",
        "DIN 277 (Germany), Brutto-Grundfläche (BGF)",
    )
    DUBAI_RICS = (
        "dubai_rics",
        "Dubai Land Department / RICS (UAE), Gross Floor Area (GFA)",
    )
    CHINA_GBT = (
        "china_gbt",
        "GB/T 50353 (China), Gross Floor Area (GFA) / Jianzhu Mianji",
    )
    IPMS_1 = (
        "ipms_1",
        "IPMS 1 / BOMA (International / USA), Gross Building Area (GBA)",
    )
    ARGENTINA_IRAM = (
        "argentina_iram",
        "IRAM (Argentina), Superficie Cubierta Total",
    )
    INDIA_RERA = (
        "india_rera",
        "IS 3861 / RERA (India), Plinth Area / Super Built-up Area",
    )
    SAUDI_SBC = (
        "saudi_sbc",
        "MOMRA / Saudi Building Code (Saudi Arabia), Total Built-up Area (TBA)",
    )
    PHILIPPINES_NBC = (
        "philippines_nbc",
        "NBC (Philippines), Gross Floor Area (GFA)",
    )
    NEN_2580 = (
        "nen_2580",
        "NEN 2580 (Netherlands), Bruto Vloeroppervlak (BVO)",
    )
    NS_3940 = (
        "ns_3940",
        "NS 3940 (Norway), Bruttoareal (BTA)",
    )
    ONORM_B_1800 = (
        "onorm_b_1800",
        "ÖNORM B 1800 (Austria), Brutto-Grundfläche (BGF)",
    )
    AUSTRALIA_PCA = (
        "australia_pca",
        "Property Council of Australia (Australia), Gross Floor Area (GFA)",
    )
    VIETNAM_QCVN = (
        "vietnam_qcvn",
        "QCVN 03:2012/BXD (Vietnam), Gross Floor Area (GFA) / Dien tich san",
    )
    SPAIN_RD_1020 = (
        "spain_rd_1020",
        "Real Decreto 1020/1993 (Spain), Superficie Construida",
    )
    MEXICO_REGLAMENTO = (
        "mexico_reglamento",
        "Reglamento de Construcciones (Mexico), Superficie de Construcción",
    )
    RICS_UK_TYPE_1 = (
        "rics_uk_type_1",
        "RICS (UK), Type 1: GEA (Gross External Area)",
    )
    RICS_UK_TYPE_2 = (
        "rics_uk_type_2",
        "RICS (UK), Type 2: GIA (Gross Internal Area)",
    )
    SANS_10400 = (
        "sans_10400",
        "SANS 10400 (South Africa), Gross Floor Area (GFA)",
    )
    SFS_5139 = (
        "sfs_5139",
        "SFS 5139 (Finland), Bruttoala (BrlA)",
    )
    SIA_416 = (
        "sia_416",
        "SIA 416 (Switzerland), Bruttogeschossfläche (BGF) / Surface de plancher brute (SPB)",
    )
    INDONESIA_SNI = (
        "indonesia_sni",
        "SNI 03-1728 (Indonesia), Luas Lantai Bangunan (Building Floor Area)",
    )
    RUSSIA_SNIP = (
        "russia_snip",
        "SNiP / SP 54.13330 (Russia), Obshchaya Ploshchad (Total Area)",
    )
    SS_21054 = (
        "ss_21054",
        "SS 21054 (Sweden), Bruttoarea (BTA)",
    )
    TURKEY_TS_01 = (
        "turkey_ts_01",
        "Turkish Standard TS 01 (Turkey), Brüt Alan (Gross Area)",
    )
    UNI_11136 = (
        "uni_11136",
        "UNI 11136 (Italy), Superficie Lorda (SL)",
    )
    URA_SINGAPORE = (
        "ura_singapore",
        "URA (Singapore), Gross Floor Area (GFA)",
    )
