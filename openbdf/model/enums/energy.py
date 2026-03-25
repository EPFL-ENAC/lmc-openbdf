from .openbdf_enum import OpenBDFEnum


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
