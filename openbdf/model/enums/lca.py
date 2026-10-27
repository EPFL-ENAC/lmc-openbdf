from .openbdf_enum import OpenBDFEnum, enum_attribute
from .references import Reference


class LCIModelingApproach(OpenBDFEnum):
    PROCESS_BASED = (
        "process_based",
        "Process-based (Typically bottom-up, highly specific data)",
        "Calculates impacts by summing individual process steps.",
    )
    IO_BASED = (
        "io_based",
        "Environmentally Extended Input-Output (EEIO) (Top-down, based on economic sector averages)",
        "Input-Output based modeling using economic data.",
    )
    HYBRID_BASED = (
        "hybrid_based",
        "Hybrid (A mix of process data and IO data)",
        "Combines both process-based and I-O based methodologies.",
    )
    OTHER = (
        "other",
        "Other",
        "Alternative LCA modeling methodology.",
    )
    reference = enum_attribute(Reference.ISO_14040_2006_ISO_14044_2006)


class LifeCycleSystemBoundary(OpenBDFEnum):
    CRADLE_TO_GATE = (
        "cradle_to_gate",
        "Cradle to Gate (A1–A3)",
        "Covers modules A1–A3.",
    )
    CRADLE_TO_GATE_WITH_OPTIONS = (
        "cradle_to_gate_options",
        "Cradle to Gate with Options (A1–A3 + others)",
        "Covers modules A1–A3 plus others.",
    )
    CRADLE_TO_GRAVE = (
        "cradle_to_grave",
        "Cradle to Grave (A1–C4)",
        "Covers modules A1–C4.",
    )
    CRADLE_TO_GRAVE_MODULE_D = (
        "cradle_to_grave_d",
        "Cradle to Grave + Module D",
        "Covers modules A1–C4 and includes module D.",
    )
    GATE_TO_GATE = (
        "gate_to_gate",
        "Gate to Gate",
        "Focuses specifically on the production stage processes.",
    )
    UNKNOWN = ("unknown", "Unknown")
    reference = enum_attribute(Reference.EN15978_2026_EU2026_52_ANNEX_III)


class LifeCycleStage_ISO14040_44(OpenBDFEnum):
    A1_A3 = (
        "a1_a3",
        "Product Stage",
        "Raw material supply, transport, and manufacturing",
    )
    A4_A5 = ("a4_a5", "Construction Process Stage", "Transport to site and installation")
    B1_B7 = (
        "b1_b7",
        "Use Stage",
        "Maintenance, repair, replacement, and operational energy/water",
    )
    C1_C4 = (
        "c1_c4",
        "End-of-Life Stage",
        "De-construction, transport, waste processing, and disposal",
    )
    D = ("d", "Benefits and Loads Beyond Boundary", "Reuse, recovery, and recycling potential")


class LifeCycleModule_ISO14040_44(OpenBDFEnum):
    A1 = (
        "A1",
        "Extraction and upstream production",
        "Extraction and processing of raw materials.",
    )
    A2 = (
        "A2",
        "Transport to factory",
        "Transportation of raw materials to the manufacturer",
    )
    A3 = (
        "A3",
        "Manufacturing",
        "Production of the product itself",
    )
    A4 = (
        "A4",
        "Transport to and from site",
        "Transportation of the product to the construction site",
    )
    A5 = (
        "A5",
        "Construction installation process",
        "Installation of the product into the building",
    )
    B1 = (
        "B1",
        "Installed products in use",
        "Environmental impacts arising from the product in use (eg, release of substances)",
    )
    B2 = (
        "B2",
        "Maintenance",
        "Actions to maintain the product's functional quality (cleaning, painting)",
    )
    B3 = (
        "B3",
        "Repair",
        "Corrective actions to return the product to a functional state",
    )
    B4 = (
        "B4",
        "Replacement",
        "Replacing the product or parts of it at the end of its service life",
    )
    B5 = (
        "B5",
        "Refurbishment",
        "Major changes to restore or improve performance",
    )
    B6 = (
        "B6",
        "Operational energy use",
        "Energy consumption related to the building's operation (heating, cooling, lighting)",
    )
    B7 = (
        "B7",
        "Operational water use",
        "Water consumption related to the building's operation",
    )
    C1 = (
        "C1",
        "Deconstruction",
        "Dismantling or demolishing the building/product",
    )
    C2 = (
        "C2",
        "Transport to waste processing or disposal",
        "Transporting the waste to processing or disposal sites",
    )
    C3 = (
        "C3",
        "Waste processing for reuse, recovery or recycling",
        "Processing waste for reuse, recovery, or recycling",
    )
    C4 = (
        "C4",
        "Disposal of waste",
        "Final disposal of waste that cannot be recovered (eg, landfill)",
    )
    D1 = (
        "D1",
        "Reuse, recycling and energy recovery resulting from the net flows of materials exiting the system boundary",
        "Net benefits or loads resulting from reusing or recycling materials (avoided emissions)",
    )
    D2 = (
        "D2",
        "Potential benefits and loads from exported utilities (for example, electrical energy, thermal energy, potable water)",
        None,
    )

    @classmethod
    def to_module(cls, stage: LifeCycleStage_ISO14040_44) -> list["LifeCycleModule_ISO14040_44"]:
        mapping = {
            LifeCycleStage_ISO14040_44.A1_A3: [cls.A1, cls.A2, cls.A3],
            LifeCycleStage_ISO14040_44.A4_A5: [cls.A4, cls.A5],
            LifeCycleStage_ISO14040_44.B1_B7: [cls.B1, cls.B2, cls.B3, cls.B4, cls.B5, cls.B6, cls.B7],
            LifeCycleStage_ISO14040_44.C1_C4: [cls.C1, cls.C2, cls.C3, cls.C4],
            LifeCycleStage_ISO14040_44.D: [cls.D1, cls.D2],
        }
        return mapping.get(stage, [])


class LCAStageOrModuleOrSubModule(OpenBDFEnum):
    # Members follow the TypeDefinitions sheet order, which interleaves modules and their stage ranges,
    # so parent categories are linked after the class body.
    reference = enum_attribute(Reference.EN15978_2026_EN15804_A2_5_2_EU2026_52_ANNEX_III)
    A1 = ("A1", f"A1 {LifeCycleModule_ISO14040_44.A1.display_name}")
    A1_A3 = ("A1-A3", f"A1-A3 {LifeCycleStage_ISO14040_44.A1_A3.display_name}")
    A2 = ("A2", f"A2 {LifeCycleModule_ISO14040_44.A2.display_name}")
    A3 = ("A3", f"A3 {LifeCycleModule_ISO14040_44.A3.display_name}")
    A4 = ("A4", f"A4 {LifeCycleModule_ISO14040_44.A4.display_name}")
    A4_A5 = ("A4-A5", f"A4-A5 {LifeCycleStage_ISO14040_44.A4_A5.display_name}")
    A5 = ("A5", f"A5 {LifeCycleModule_ISO14040_44.A5.display_name}")
    A5_1 = ("A5.1", "A5.1 Pre-construction demolition")
    A5_2 = ("A5.2", "A5.2 Construction activities")
    A5_3 = ("A5.3", "A5.3 Waste and waste management")
    A5_4 = ("A5.4", "A5.4 Worker transport")
    B1 = ("B1", f"B1 {LifeCycleModule_ISO14040_44.B1.display_name}")
    B1_1 = ("B1.1", "B1.1 Emissions from materials and carbonation")
    B1_2 = ("B1.2", "B1.2 Fugitive emissions of refrigerants")
    B1_B7 = ("B1-B7", f"B1-B7 {LifeCycleStage_ISO14040_44.B1_B7.display_name}")
    B2 = ("B2", f"B2 {LifeCycleModule_ISO14040_44.B2.display_name}")
    B3 = ("B3", f"B3 {LifeCycleModule_ISO14040_44.B3.display_name}")
    B4 = ("B4", f"B4 {LifeCycleModule_ISO14040_44.B4.display_name}")
    B5 = ("B5", f"B5 {LifeCycleModule_ISO14040_44.B5.display_name}")
    B6 = ("B6", f"B6 {LifeCycleModule_ISO14040_44.B6.display_name}")
    B6_1 = ("B6.1", "B6.1 Regulated building-integrated systems (services)")
    B6_2 = ("B6.2", "B6.2 Non-regulated building-integrated systems (services)")
    B6_3 = ("B6.3", "B6.3 Other energy use related to building user activities")
    B7 = ("B7", f"B7 {LifeCycleModule_ISO14040_44.B7.display_name}")
    B7_1 = (
        "B7.1",
        "B7.1 Essential building-integrated systems (toilets, showers, bathrooms, heating, cooling, ventilation, humidification, and irrigation)",
    )
    B7_2 = ("B7.2", "B7.2 Other building-integrated systems (swimming pools, saunas etc.)")
    B7_3 = ("B7.3", "B7.3 Non-building-integrated systems (for example, dishwashers, washing machines, etc.)")
    B7_4 = ("B7.4", "B7.4")
    B8 = ("B8", "B8 Building-integrated users' activities, not covered by B1-B7")
    B8_1 = ("B8.1", "B8.1 Transport of persons to and from the building")
    B8_2 = ("B8.2", "B8.2 Charging of electric vehicles within the building site")
    B8_3 = (
        "B8.3",
        "B8.3 Others, such as use of “consumables” like paper for offices, or furniture and equipment not fixed to the building",
    )
    C1 = ("C1", f"C1 {LifeCycleModule_ISO14040_44.C1.display_name}")
    C1_C4 = ("C1-C4", f"C1-C4 {LifeCycleStage_ISO14040_44.C1_C4.display_name}")
    C2 = ("C2", f"C2 {LifeCycleModule_ISO14040_44.C2.display_name}")
    C3 = ("C3", f"C3 {LifeCycleModule_ISO14040_44.C3.display_name}")
    C4 = ("C4", f"C4 {LifeCycleModule_ISO14040_44.C4.display_name}")
    D1 = ("D1", f"D1 {LifeCycleModule_ISO14040_44.D1.display_name}")
    D2 = ("D2", f"D2 {LifeCycleModule_ISO14040_44.D2.display_name}")
    D = ("D", f"D {LifeCycleStage_ISO14040_44.D.display_name}")
    D_D2 = ("D-D2", "D-D2 Beyond the system boundary")


for _child, _parent in (
    ("A1", "A1_A3"),
    ("A2", "A1_A3"),
    ("A3", "A1_A3"),
    ("A4", "A4_A5"),
    ("A5", "A4_A5"),
    ("A5_1", "A5"),
    ("A5_2", "A5"),
    ("A5_3", "A5"),
    ("A5_4", "A5"),
    ("B1", "B1_B7"),
    ("B1_1", "B1"),
    ("B1_2", "B1"),
    ("B2", "B1_B7"),
    ("B3", "B1_B7"),
    ("B4", "B1_B7"),
    ("B5", "B1_B7"),
    ("B6", "B1_B7"),
    ("B6_1", "B6"),
    ("B6_2", "B6"),
    ("B6_3", "B6"),
    ("B7", "B1_B7"),
    ("B7_1", "B7"),
    ("B7_2", "B7"),
    ("B7_3", "B7"),
    ("B7_4", "B7"),
    ("B8", "B1_B7"),
    ("B8_1", "B8"),
    ("B8_2", "B8"),
    ("B8_3", "B8"),
    ("C1", "C1_C4"),
    ("C2", "C1_C4"),
    ("C3", "C1_C4"),
    ("C4", "C1_C4"),
    ("D", "D_D2"),
    ("D1", "D_D2"),
    ("D2", "D_D2"),
):
    getattr(LCAStageOrModuleOrSubModule, _child).parent_category = getattr(LCAStageOrModuleOrSubModule, _parent)


class LCADatabase(OpenBDFEnum):
    OKOBAUDAT_20_23_050 = ("OKOBAUDAT_20.23.050", "OKOBAUDAT_20.23.050")
    OKOBAUDAT_20_24_070 = ("OKOBAUDAT_20.24.070", "OKOBAUDAT_20.24.070")
    HABITAT2030_BIGTEN = ("habitat2030_BIGTEN", "habitat2030_BIGTEN")
    IBU_DATA = ("IBU_Data", "IBU_Data")
    EC3 = ("EC3", "EC3")
    ECOINVENT = ("ecoinvent", "Ecoinvent")
    OTHER = ("Other", "Other")
    reference = enum_attribute(Reference.EN_15941_2024)


class LCADatabaseSystemModel(OpenBDFEnum):
    CUT_OFF = (
        "cut_off",
        "Cut off (recycled content approach, ecoinvent cut-off)",
        "recycled content approach, ecoinvent cut-off",
    )
    CUT_OFF_EN15804 = (
        "cut_off_en15804",
        "Cut off EN15804 (ecoinvent system model aligned with EN 15804)",
        "ecoinvent system model aligned with EN 15804",
    )
    APOS = (
        "apos",
        "APOS (allocation at the point of substitution)",
        "allocation at the point of substitution",
    )
    CONSEQUENTIAL = (
        "consequential",
        "Consequential (marginal, market-driven modelling)",
        "marginal, market-driven modelling",
    )
    UNKNOWN = ("unknown", "Unknown")
    reference = enum_attribute(Reference.EN15804_A2_ECOINVENT_SYSTEM_MODELS)


class DataWeightingBasis(OpenBDFEnum):
    GWP_FOSSIL_A1_A3 = (
        "gwp_fossil_a1_a3",
        "GWP fossil a1 a3 (shares weighted by fossil global warming potential of modules A1 to A3)",
        "shares weighted by fossil global warming potential of modules A1 to A3",
    )
    MASS = (
        "mass",
        "Mass (shares weighted by mass)",
        "shares weighted by mass",
    )
    NOT_COMPUTED = (
        "not_computed",
        "Not computed (shares not weighted)",
        "shares not weighted",
    )
    reference = enum_attribute(Reference.GBDI)


class BiogenicCarbonAccounting(OpenBDFEnum):
    ZERO_ZERO = ("0/0", "0/0 (biogenic carbon not counted)", "Neutral accounting (no sequestration/no emission)")
    MINUS_ONE_PLUS_ONE = (
        "-1/+1",
        "-1/+1 (uptake counted as negative and release as positive)",
        "Credit at start / burden at end of life",
    )
    DYNAMIC_LCA = ("dynamic_lca", "Dynamic LCA")
    TON_YEAR = (
        "ton_year",
        "Ton-Year Accounting or Discounting Method",
    )
    OTHER = ("other", "Other")
    reference = enum_attribute(Reference.EN15804_A2_EN15978_2026)


class LCATemporalApproach(OpenBDFEnum):
    STATIC = ("static", "Static (impacts not distributed over time)")
    DYNAMIC = ("dynamic", "Dynamic (impacts distributed over time)")
    PROBABILISTIC = ("probabilistic", "Probabilistic")
    PROSPECTIVE = ("prospective", "Prospective")
    reference = enum_attribute(Reference.EN15978_2026)


class AssessmentType_EN15978(OpenBDFEnum):
    TYPE_1 = ("Type 1 - early building model, concept design", "Type 1 - early building model, concept design")
    TYPE_2 = (
        "Type 2 - building model, building permit design",
        "Type 2 - building model, building permit design",
    )
    TYPE_3 = ("Type 3 - as designed building model", "Type 3 - as designed building model")
    TYPE_4 = (
        "Type 4 - fully detailed as designed or as built model",
        "Type 4 - fully detailed as designed or as built model",
    )
    UNKNOWN = ("unknown", "Unknown")
    reference = enum_attribute(Reference.EN15978_2026)


class LimitValueScopeReduction(OpenBDFEnum):
    NONE = (
        "none",
        "None (nothing left out, the result is a complete assessment)",
        "nothing left out, the result is a complete assessment",
    )
    LIFE_CYCLE_STAGES = (
        "life_cycle_stages",
        "Life cycle stages",
        "parts of life-cycle stages left out",
    )
    SCOPE_OF_BUILDING_COMPONENTS = (
        "scope_of_building_components",
        "Scope of building components",
        "parts of the scope of building components left out",
    )
    BOTH = (
        "both",
        "Both (parts of life-cycle stages and parts of the scope of building components left out)",
        "parts of life-cycle stages and parts of the scope of building components left out",
    )
    reference = enum_attribute(Reference.EU2026_52_ANNEX_III)


class LCIAMethodology(OpenBDFEnum):
    EN_15804_2012_A1_2013 = ("EN 15804:2012+A1:2013", "EN 15804:2012+A1:2013")
    EN_15804_2012_A2_2019 = ("EN 15804:2012+A2:2019", "EN 15804:2012+A2:2019")
    EN_15978_2026 = ("EN 15978:2026", "EN 15978:2026")
    US_EPA_TRACI_2_1 = ("US EPA TRACI 2.1", "US EPA TRACI 2.1")
    OTHER = ("Other", "Other")
    reference = enum_attribute(Reference.EN15804_A2_TRACI_RECIPE_2016_IPCC_AR6)
