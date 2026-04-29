from .openbdf_enum import OpenBDFEnum


class LCIModelingApproach_ISO14040_44(OpenBDFEnum):
    PROCESS_BASED = (
        "process_based",
        "Process-based",
        "Calculates impacts by summing individual process steps.",
    )
    IO_BASED = (
        "io_based",
        "I-O based",
        "Input-Output based modeling using economic data.",
    )
    HYBRID_BASED = (
        "hybrid_based",
        "Hybrid-based",
        "Combines both process-based and I-O based methodologies.",
    )
    OTHER = (
        "other",
        "Other",
        "Alternative LCA modeling methodology.",
    )


class LifeCycleStage_ISO14040_43(OpenBDFEnum):
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


class BiogenicCarbonAccounting(OpenBDFEnum):
    ZERO_ZERO = ("0/0", "0/0", "Neutral accounting (no sequestration/no emission)")
    MINUS_ONE_PLUS_ONE = (
        "-1/+1",
        "-1/+1",
        "Credit at start / burden at end of life",
    )
    DYNAMIC_LCA = ("dynamic_lca", "Dynamic LCA")
    TON_YEAR = (
        "ton_year",
        "Ton-Year Accounting or Discounting Method",
    )
    OTHER = ("other", "Other")


class LCATemporalApproach(OpenBDFEnum):
    STATIC = ("static", "Static")
    DYNAMIC = ("dynamic", "Dynamic")
    PROBABILISTIC = ("probabilistic", "Probabilistic")
    PROSPECTIVE = ("prospective", "Prospective")


class LCIAMethodology(OpenBDFEnum):
    EN_15804_A2 = (
        "en_15804_a2",
        "EN 15804+A2 (EF 3.0) - Current EU standard",
        "Current EU standard for environmental product declarations.",
    )
    EN_15804_A1 = (
        "en_15804_a1",
        "EN 15804+A1 (CML 2001) - Older EU standard",
        "Older EU standard for environmental product declarations.",
    )
    TRACI_2_1 = (
        "traci_2_1",
        "TRACI 2.1 - Standard for North America/LEED",
        "Standard for North America/LEED (The Tool for Reduction and Assessment of Chemical and Other Environmental Impacts).",
    )
    RECIPE_2016 = (
        "recipe_2016",
        "ReCiPe 2016",
        "A harmonized life cycle impact assessment method at midpoint and endpoint level.",
    )
    IPCC_AR6 = (
        "ipcc_ar6",
        "IPCC AR6 (2021)",
        "Intergovernmental Panel on Climate Change Sixth Assessment Report.",
    )
    OTHER = (
        "other",
        "Other",
        "Other non-specified LCIA methodology.",
    )
