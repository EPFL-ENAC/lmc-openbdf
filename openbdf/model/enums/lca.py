from .openbdf_enum import OpenBDFEnum


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
        "Raw Material Supply",
        "Extraction and processing of raw materials.",
    )
    A2 = (
        "A2",
        "Transport to manufacturer",
        "Transportation of raw materials to the manufacturer",
    )
    A3 = (
        "A3",
        "Manufacturing",
        "Production of the product itself",
    )
    A4 = (
        "A4",
        "Transport to site",
        "Transportation of the product to the construction site",
    )
    A5 = (
        "A5",
        "Construction/Installation",
        "Installation of the product into the building",
    )
    B1 = (
        "B1",
        "Use",
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
        "Operational Energy Use",
        "Energy consumption related to the building's operation (heating, cooling, lighting)",
    )
    B7 = (
        "B7",
        "Operational Water Use",
        "Water consumption related to the building's operation",
    )
    C1 = (
        "C1",
        "De-construction/Demolition",
        "Dismantling or demolishing the building/product",
    )
    C2 = (
        "C2",
        "Transport",
        "Transporting the waste to processing or disposal sites",
    )
    C3 = (
        "C3",
        "Waste Processing",
        "Processing waste for reuse, recovery, or recycling",
    )
    C4 = (
        "C4",
        "Disposal",
        "Final disposal of waste that cannot be recovered (eg, landfill)",
    )
    D1 = (
        "D1",
        "Reuse, Recovery, and Recycling Potential",
        "Net benefits or loads resulting from reusing or recycling materials (avoided emissions)",
    )
    D2 = (
        "D2",
        "Exported Energy (or Energy Recovery Potential)",
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
    A1 = ("A1", "A1 Raw material supply")
    A1_A3 = ("A1-A3", "A1-A3 Product stage")
    A2 = ("A2", "A2 Transport")
    A3 = ("A3", "A3 Manufacturing")
    A4 = ("A4", "A4 Transport to site")
    A4_A5 = ("A4-A5", "A4-A5 Construction process stage")
    A5 = ("A5", "A5 Construction and installation process")
    A5_1 = ("A5.1", "A5.1")
    A5_2 = ("A5.2", "A5.2")
    A5_3 = ("A5.3", "A5.3")
    A5_4 = ("A5.4", "A5.4")
    B1 = ("B1", "B1 Use")
    B1_1 = ("B1.1", "B1.1")
    B1_2 = ("B1.2", "B1.2")
    B1_B7 = ("B1-B7", "B1-B7 Use stage")
    B2 = ("B2", "B2 Maintenance")
    B3 = ("B3", "B3 Repair")
    B4 = ("B4", "B4 Replacement")
    B5 = ("B5", "B5 Refurbishment")
    B6 = ("B6", "B6 Operational energy use")
    B6_1 = ("B6.1", "B6.1")
    B6_2 = ("B6.2", "B6.2")
    B6_3 = ("B6.3", "B6.3")
    B7 = ("B7", "B7 Operational water use")
    B7_1 = ("B7.1", "B7.1")
    B7_2 = ("B7.2", "B7.2")
    B7_3 = ("B7.3", "B7.3")
    B7_4 = ("B7.4", "B7.4")
    B8 = ("B8", "B8")
    B8_1 = ("B8.1", "B8.1")
    B8_2 = ("B8.2", "B8.2")
    B8_3 = ("B8.3", "B8.3")
    C1 = ("C1", "C1 Deconstruction and demolition")
    C1_C4 = ("C1-C4", "C1-C4 End-of-life stage")
    C2 = ("C2", "C2 Transport")
    C3 = ("C3", "C3 Waste processing")
    C4 = ("C4", "C4 Disposal")
    D1 = ("D1", "D1 Reuse, recovery, and recycling potential")
    D2 = ("D2", "D2 Net benefits beyond the system boundary")
    D = ("D", "D Benefits and loads beyond the system boundary")
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
    ECOINVENT = ("ecoinvent", "ecoinvent")
    OTHER = ("Other", "Other")


class LCADatabaseSystemModel(OpenBDFEnum):
    CUT_OFF = (
        "cut_off",
        "cut off (recycled content approach, ecoinvent cut-off)",
        "recycled content approach, ecoinvent cut-off",
    )
    CUT_OFF_EN15804 = (
        "cut_off_en15804",
        "cut off EN15804 (ecoinvent system model aligned with EN 15804)",
        "ecoinvent system model aligned with EN 15804",
    )
    APOS = (
        "apos",
        "APOS (allocation at the point of substitution)",
        "allocation at the point of substitution",
    )
    CONSEQUENTIAL = (
        "consequential",
        "consequential (marginal, market-driven modelling)",
        "marginal, market-driven modelling",
    )


class DataWeightingBasis(OpenBDFEnum):
    GWP_FOSSIL_A1_A3 = (
        "gwp_fossil_a1_a3",
        "gwp fossil a1 a3 (shares weighted by fossil global warming potential of modules A1 to A3)",
        "shares weighted by fossil global warming potential of modules A1 to A3",
    )
    MASS = (
        "mass",
        "mass (shares weighted by mass)",
        "shares weighted by mass",
    )
    NOT_COMPUTED = (
        "not_computed",
        "not computed (shares not weighted)",
        "shares not weighted",
    )


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


class LCATemporalApproach(OpenBDFEnum):
    STATIC = ("static", "Static (impacts not distributed over time)")
    DYNAMIC = ("dynamic", "Dynamic (impacts distributed over time)")
    PROBABILISTIC = ("probabilistic", "Probabilistic")
    PROSPECTIVE = ("prospective", "Prospective")


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


class LimitValueScopeReduction(OpenBDFEnum):
    NONE = (
        "none",
        "none (nothing left out, the result is a complete assessment)",
        "nothing left out, the result is a complete assessment",
    )
    LIFE_CYCLE_STAGES = (
        "life_cycle_stages",
        "life_cycle_stages (parts of life-cycle stages left out)",
        "parts of life-cycle stages left out",
    )
    SCOPE_OF_BUILDING_COMPONENTS = (
        "scope_of_building_components",
        "scope_of_building_components (parts of the scope of building components left out)",
        "parts of the scope of building components left out",
    )
    BOTH = (
        "both",
        "both (parts of life-cycle stages and parts of the scope of building components left out)",
        "parts of life-cycle stages and parts of the scope of building components left out",
    )


class LCIAMethodology(OpenBDFEnum):
    EN_15804_A2 = (
        "EN15804_A2_EF3.0",
        "EN15804_A2_EF3.0",
        "EN 15804+A2 (EF 3.0) - Current EU standard for environmental product declarations.",
    )
    EN_15804_A1 = (
        "EN15804_A1_CML2001",
        "EN15804_A1_CML2001",
        "EN 15804+A1 (CML 2001) - Older EU standard for environmental product declarations.",
    )
    TRACI_2_1 = (
        "TRACI_2.1",
        "TRACI_2.1",
        "Standard for North America/LEED (The Tool for Reduction and Assessment of Chemical and Other Environmental Impacts).",
    )
    RECIPE_2016 = (
        "ReCiPe_2016",
        "ReCiPe_2016",
        "A harmonized life cycle impact assessment method at midpoint and endpoint level.",
    )
    IPCC_AR6 = (
        "IPCC_AR6",
        "IPCC_AR6",
        "Intergovernmental Panel on Climate Change Sixth Assessment Report.",
    )
    OTHER = (
        "Other",
        "Other",
        "Other non-specified LCIA methodology.",
    )
