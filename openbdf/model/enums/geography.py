from .openbdf_enum import OpenBDFEnum


class ClimateZone(OpenBDFEnum):
    ASHRAE169_1A = ("ASHRAE169_1A", "ASHRAE169_1A")
    ASHRAE169_2A = ("ASHRAE169_2A", "ASHRAE169_2A")
    ASHRAE169_2B = ("ASHRAE169_2B", "ASHRAE169_2B")
    ASHRAE169_3A = ("ASHRAE169_3A", "ASHRAE169_3A")
    ASHRAE169_3B = ("ASHRAE169_3B", "ASHRAE169_3B")
    ASHRAE169_3C = ("ASHRAE169_3C", "ASHRAE169_3C")
    ASHRAE169_4A = ("ASHRAE169_4A", "ASHRAE169_4A")
    ASHRAE169_4B = ("ASHRAE169_4B", "ASHRAE169_4B")
    ASHRAE169_4C = ("ASHRAE169_4C", "ASHRAE169_4C")
    ASHRAE169_5A = ("ASHRAE169_5A", "ASHRAE169_5A")
    ASHRAE169_5B = ("ASHRAE169_5B", "ASHRAE169_5B")
    ASHRAE169_5C = ("ASHRAE169_5C", "ASHRAE169_5C")
    ASHRAE169_6A = ("ASHRAE169_6A", "ASHRAE169_6A")
    ASHRAE169_6B = ("ASHRAE169_6B", "ASHRAE169_6B")
    ASHRAE169_7 = ("ASHRAE169_7", "ASHRAE169_7")
    ASHRAE169_8 = ("ASHRAE169_8", "ASHRAE169_8")
    IECC_1A = ("IECC_1A", "IECC_1A")
    IECC_2A = ("IECC_2A", "IECC_2A")
    IECC_2B = ("IECC_2B", "IECC_2B")
    IECC_3A = ("IECC_3A", "IECC_3A")
    IECC_3B = ("IECC_3B", "IECC_3B")
    IECC_3C = ("IECC_3C", "IECC_3C")
    IECC_4A = ("IECC_4A", "IECC_4A")
    IECC_4B = ("IECC_4B", "IECC_4B")
    IECC_4C = ("IECC_4C", "IECC_4C")
    IECC_5A = ("IECC_5A", "IECC_5A")
    IECC_5B = ("IECC_5B", "IECC_5B")
    IECC_5C = ("IECC_5C", "IECC_5C")
    IECC_6A = ("IECC_6A", "IECC_6A")
    IECC_6B = ("IECC_6B", "IECC_6B")
    IECC_7 = ("IECC_7", "IECC_7")
    IECC_8 = ("IECC_8", "IECC_8")
    KOPPEN_GEIGER_AF = ("KoppenGeiger_Af", "KoppenGeiger_Af")
    KOPPEN_GEIGER_AM = ("KoppenGeiger_Am", "KoppenGeiger_Am")
    KOPPEN_GEIGER_AW = ("KoppenGeiger_Aw", "KoppenGeiger_Aw")
    KOPPEN_GEIGER_BWH = ("KoppenGeiger_BWh", "KoppenGeiger_BWh")
    KOPPEN_GEIGER_BWK = ("KoppenGeiger_BWk", "KoppenGeiger_BWk")
    KOPPEN_GEIGER_BSH = ("KoppenGeiger_BSh", "KoppenGeiger_BSh")
    KOPPEN_GEIGER_BSK = ("KoppenGeiger_BSk", "KoppenGeiger_BSk")
    KOPPEN_GEIGER_CSA = ("KoppenGeiger_Csa", "KoppenGeiger_Csa")
    KOPPEN_GEIGER_CSB = ("KoppenGeiger_Csb", "KoppenGeiger_Csb")
    KOPPEN_GEIGER_CSC = ("KoppenGeiger_Csc", "KoppenGeiger_Csc")
    KOPPEN_GEIGER_CWA = ("KoppenGeiger_Cwa", "KoppenGeiger_Cwa")
    KOPPEN_GEIGER_CWB = ("KoppenGeiger_Cwb", "KoppenGeiger_Cwb")
    KOPPEN_GEIGER_CWC = ("KoppenGeiger_Cwc", "KoppenGeiger_Cwc")
    KOPPEN_GEIGER_CFA = ("KoppenGeiger_Cfa", "KoppenGeiger_Cfa")
    KOPPEN_GEIGER_CFB = ("KoppenGeiger_Cfb", "KoppenGeiger_Cfb")
    KOPPEN_GEIGER_CFC = ("KoppenGeiger_Cfc", "KoppenGeiger_Cfc")
    KOPPEN_GEIGER_DSA = ("KoppenGeiger_Dsa", "KoppenGeiger_Dsa")
    KOPPEN_GEIGER_DSB = ("KoppenGeiger_Dsb", "KoppenGeiger_Dsb")
    KOPPEN_GEIGER_DSC = ("KoppenGeiger_Dsc", "KoppenGeiger_Dsc")
    KOPPEN_GEIGER_DSD = ("KoppenGeiger_Dsd", "KoppenGeiger_Dsd")
    KOPPEN_GEIGER_DWA = ("KoppenGeiger_Dwa", "KoppenGeiger_Dwa")
    KOPPEN_GEIGER_DWB = ("KoppenGeiger_Dwb", "KoppenGeiger_Dwb")
    KOPPEN_GEIGER_DWC = ("KoppenGeiger_Dwc", "KoppenGeiger_Dwc")
    KOPPEN_GEIGER_DWD = ("KoppenGeiger_Dwd", "KoppenGeiger_Dwd")
    KOPPEN_GEIGER_DFA = ("KoppenGeiger_Dfa", "KoppenGeiger_Dfa")
    KOPPEN_GEIGER_DFB = ("KoppenGeiger_Dfb", "KoppenGeiger_Dfb")
    KOPPEN_GEIGER_DFC = ("KoppenGeiger_Dfc", "KoppenGeiger_Dfc")
    KOPPEN_GEIGER_DFD = ("KoppenGeiger_Dfd", "KoppenGeiger_Dfd")
    KOPPEN_GEIGER_ET = ("KoppenGeiger_ET", "KoppenGeiger_ET")
    KOPPEN_GEIGER_EF = ("KoppenGeiger_EF", "KoppenGeiger_EF")
    OTHER_NATIONAL = ("Other_National", "Other_National")
    UNKNOWN = ("Unknown", "Unknown")


class ExtendedDefaultDataBasis(OpenBDFEnum):
    OUTERMOST_REGION = (
        "outermost_region",
        "Outermost region",
        "an outermost region within the meaning of Article 349 TFEU",
    )
    DATA_GAP = (
        "data_gap",
        "Data gap (default values used to fill data gaps where no other type of data is available)",
        "default values used to fill data gaps where no other type of data is available",
    )
    SIMPLIFIED_CALCULATION = (
        "simplified_calculation",
        "Simplified Calculation (default values used where it is necessary to simplify the calculation)",
        "default values used where it is necessary to simplify the calculation",
    )
    OTHER = (
        "other",
        "Other (stated in the assessor note)",
        "stated in the assessor note",
    )


class FEMASeismicActivity(OpenBDFEnum):
    SDC_A = (
        "SDC A",
        "Minor",
        "Minor expected ground shaking.",
    )
    SDC_B = (
        "SDC B",
        "Moderate",
        "Moderate expected ground shaking for standard buildings.",
    )
    SDC_C = (
        "SDC C",
        "Moderate to Severe",
        "Moderate to severe expected ground shaking for standard buildings, and moderate for higher-risk buildings.",
    )
    SDC_D = (
        "SDC D",
        "Severe and Destructive",
        "Severe and destructive expected ground shaking, often associated with poorer soil conditions but not near major faults.",
    )
    SDC_E = (
        "SDC E",
        "Severe Near Faults",
        "Severe expected ground shaking in areas near major active faults.",
    )
    SDC_F = (
        "SDC F",
        "Severe High-Risk",
        "Severe expected ground shaking in areas near major active faults for high-risk buildings.",
    )


class SoilType(OpenBDFEnum):
    SEDIMENTARY_FOLIATED_ROCK = (
        "sedimentary_foliated_rock",
        "Sedimentary or Foliated Rock",
        "Stable rock formations, often characterized by layered or planar structures.",
    )
    SANDY_GRAVEL = (
        "sandy_gravel",
        "Sandy Gravel",
        "A mixture of gravel and sand with high load-bearing capacity.",
    )
    SAND = (
        "sand",
        "Sand",
        "Granular material composed of finely divided rock and mineral particles.",
    )
    SILTY_SAND = (
        "silty_sand",
        "Silty Sand",
        "Sand containing a significant portion of silt particles, affecting drainage.",
    )
    CLAY = (
        "clay",
        "Clay",
        "Fine-grained natural soil material that is plastic when wet.",
    )
    SOFT_CLAY = (
        "soft_clay",
        "Soft Clay",
        "Clay with high water content and lower shear strength compared to standard clay.",
    )
