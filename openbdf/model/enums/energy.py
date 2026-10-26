from .openbdf_enum import OpenBDFEnum, enum_attribute
from .references import Reference


class BuildingEnergyClassificationSystem(OpenBDFEnum):
    EU_EPC = (
        "eu_epc",
        "EU EPC",
        "European Union Energy Performance Certificate - mandatory across the EU, grades usually A to G",
    )
    ENERGY_STAR = (
        "energy_star",
        "Energy Star",
        "US Environmental Protection Agency standard - 1-100 score",
    )
    NABERS = (
        "nabers",
        "NABERS",
        "National Australian Built Environment Rating System - widely used in Australia and expanding to the UK",
    )
    HQE = (
        "hqe",
        "HQE",
        "Haute Qualité Environnementale - standard in France",
    )
    DGNB = (
        "dgnb",
        "DGNB",
        "German Sustainable Building Council standard",
    )
    GREEN_STAR = (
        "green_star",
        "Green Star",
        "Standard in Australia, New Zealand, and South Africa",
    )
    GREEN_MARK = (
        "green_mark",
        "Green Mark",
        "Singapore's standard, widely used in Southeast Asia",
    )
    CASBEE = (
        "casbee",
        "CASBEE",
        "Comprehensive Assessment System for Built Environment Efficiency - Japan",
    )
    LEED = (
        "leed",
        "LEED",
        "Leadership in Energy and Environmental Design - heavily used in the Americas and globally",
    )
    BREEAM = (
        "breeam",
        "BREEAM",
        "Building Research Establishment Environmental Assessment Method - heavily used in the UK and globally",
    )
    EDGE = (
        "edge",
        "EDGE",
        "Excellence in Design for Greater Efficiencies - IFC standard, very common in emerging markets",
    )
    WELL = (
        "well",
        "WELL",
        "Often paired with LEED/BREEAM, focuses on human health but intersects with building performance",
    )
    OTHER = (
        "other",
        "Other",
        "Any other building energy certification system not listed above",
    )
    NONE = (
        "none",
        "None",
        "No energy classification or certification for this building",
    )
    reference = enum_attribute(Reference.EN_ISO_52000_1_2017)


class BuildingEnergyCodeSystem(OpenBDFEnum):
    EPBD_EU = ("EPBD (EU)", "EPBD (EU)")
    EN_ISO_52000_1 = ("EN ISO 52000-1", "EN ISO 52000-1")
    IECC_US = ("IECC (US)", "IECC (US)")
    ASHRAE_90_1_US = ("ASHRAE 90.1 (US)", "ASHRAE 90.1 (US)")
    ASHRAE_189_1_US = ("ASHRAE 189.1 (US)", "ASHRAE 189.1 (US)")
    OIB_RICHTLINIE_6_AT = ("OIB-Richtlinie 6 (AT)", "OIB-Richtlinie 6 (AT)")
    GEG_DE = ("GEG (DE)", "GEG (DE)")
    SIA_380_1_CH = ("SIA 380/1 (CH)", "SIA 380/1 (CH)")
    RE2020_FR = ("RE2020 (FR)", "RE2020 (FR)")
    CTE_DB_HE_ES = ("CTE DB-HE (ES)", "CTE DB-HE (ES)")
    BOUWBESLUIT_BENG_NL = ("Bouwbesluit / BENG (NL)", "Bouwbesluit / BENG (NL)")
    PART_L_UK = ("Part L (UK)", "Part L (UK)")
    OTHER_NATIONAL = ("Other national", "Other national")
    UNKNOWN = ("Unknown", "Unknown")
    reference = enum_attribute(Reference.EN_ISO_52000_1_2017)


class OnSiteRenewableAllocationApproach(OpenBDFEnum):
    APPROACH_A = (
        "approach_a",
        "approach_a (full allocation to the building of energy storage components and of all other system parts)",
        "full allocation to the building of energy storage components and of all other system parts",
    )
    APPROACH_B1 = (
        "approach_b1",
        "approach_b1 (full allocation of energy storage components; other system parts allocated in proportion to the share of captured or generated energy used for self-consumption)",
        "full allocation of energy storage components; other system parts allocated in proportion to the share of captured or generated energy used for self-consumption",
    )
    APPROACH_B2 = (
        "approach_b2",
        "approach_b2 (full allocation of energy storage components; components integrated into the building envelope and forming its surface allocated in full, with the remaining embodied emissions allocated in proportion to the share used for self-consumption)",
        "full allocation of energy storage components; components integrated into the building envelope and forming its surface allocated in full, with the remaining embodied emissions allocated in proportion to the share used for self-consumption",
    )
    reference = enum_attribute(Reference.EU2026_52_ANNEX_III)


class EmissionFactorScenario(OpenBDFEnum):
    NOT_APPLICABLE = (
        "not_applicable",
        "Not applicable (no operational energy calculated)",
        "no operational energy calculated",
    )
    NONE = (
        "none",
        "None (no forward-looking factors; the factors of the base Year apply over the whole period)",
        "no forward-looking factors; the factors of the base year apply over the whole period",
    )
    FORWARD_LOOKING = (
        "forward_looking",
        "forward_looking (forward-looking emission factors, justified, consistent and clearly defined for the whole reference study period)",
        "forward-looking emission factors, justified, consistent and clearly defined for the whole reference study period",
    )
    reference = enum_attribute(Reference.EU2026_52_ANNEX_III)


class PrimaryEnergySource(OpenBDFEnum):
    NATURAL_GAS = ("natural_gas", "Natural Gas")
    COAL = ("coal", "Coal")
    OIL = ("oil_petroleum", "Oil/Petroleum")
    NUCLEAR = ("nuclear", "Nuclear Energy")
    SOLAR = ("solar", "Solar Energy (Photovoltaic and Thermal)")
    WIND = ("wind", "Wind Energy")
    HYDRO = ("hydropower", "Hydropower")
    GEOTHERMAL = ("geothermal", "Geothermal Energy")
    AEROTHERMAL = ("aerothermal", "Aerothermal Energy")
    BIOMASS = ("biomass", "Biomass (Wood, Pellets)")
    WASTE_HEAT = ("waste_heat", "Waste Heat")
    reference = enum_attribute(Reference.EN_ISO_52000_1_2017)
