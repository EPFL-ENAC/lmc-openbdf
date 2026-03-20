from model.enums.openbdf_enum import OpenBDFEnum


class ProjectPhase(OpenBDFEnum):
    STRATEGIC_DEFINITION = ("strategic_definition", "Strategic Definition")
    PRELIMINARY_STUDIES = ("preliminary_studies", "Preliminary Studies")
    CONCEPT_DESIGN = ("concept_design", "Concept Design")
    DEVELOPED_DESIGN = ("developed_design", "Developed Design")
    TECHNICAL_DESIGN = ("technical_design", "Technical Design")
    MANUFACTURING_CONSTRUCTION = (
        "manufacturing_construction",
        "Manufacturing and Construction",
    )
    HANDOVER_COMMISSIONING = (
        "handover_commissioning",
        "Handover and Commissioning",
    )
    OPERATION_MANAGEMENT = (
        "operation_management",
        "Operation and Management",
    )
    END_OF_USE = ("end_of_use", "End of Use, Recycling")


class ConstructionType(OpenBDFEnum):
    NEW_CONSTRUCTION = ("new_construction", "New Construction")
    TENANT_IMPROVEMENT = ("tenant_improvement", "Tenant Improvements")
    MINOR_RENOVATION = (
        "minor_renovation",
        "Minor Renovation (without addition)",
    )
    MAJOR_RENOVATION = (
        "major_renovation",
        "Major Renovation (with addition)",
    )


class ProjectUnits(OpenBDFEnum):
    IMPERIAL = ("imperial", "Imperial Units System (IP, USA)")
    METRIC = ("metric", "Metric, International Units System (SI)")
