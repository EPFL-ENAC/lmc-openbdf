from .openbdf_enum import OpenBDFEnum


class ASHRAEClimateZone(OpenBDFEnum):
    ZONE_1A = ("1a", "1A (Very Hot - Humid)")
    ZONE_2A = ("2a", "2A (Hot - Humid)")
    ZONE_2B = ("2b", "2B (Hot - Dry)")
    ZONE_3A = ("3a", "3A (Warm - Humid)")
    ZONE_3B = ("3b", "3B (Warm - Dry)")
    ZONE_3C = ("3c", "3C (Warm - Marine)")
    ZONE_4A = ("4a", "4A (Mixed - Humid)")
    ZONE_4B = ("4b", "4B (Mixed - Dry)")
    ZONE_4C = ("4c", "4C (Mixed - Marine)")


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
