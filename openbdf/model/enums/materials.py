from .openbdf_enum import OpenBDFEnum, enum_attribute
from .references import Reference


class MainStructureType(OpenBDFEnum):
    CONCRETE = ("concrete", "Concrete")
    STEEL = ("steel", "Steel")
    TIMBER = ("timber", "Timber")
    MASONRY = ("masonry", "Masonry")
    OTHER = ("other", "Other")


class OpenBDFMaterialClassification(OpenBDFEnum):
    # Bio-based materials
    WOOD = ("1.1", "1.1 Wood", "Bio-based materials")
    BIO_INSULATION = ("1.2", "1.2 Bio-based insulation", "Bio-based materials")
    BIO_OTHER = ("1.0", "1.0 Other bio-based materials", "Bio-based materials")

    # Fossil-based materials
    PLASTICS = (
        "2.1",
        "2.1 Plastics (PC, PE, PP, PVC)",
        "Fossil-based materials",
    )
    FOSSIL_INSULATION = (
        "2.2",
        "2.2 Fossil-based insulation",
        "Fossil-based materials",
    )
    FOSSIL_OTHER = (
        "2.0",
        "2.0 Other fossil energy materials",
        "Fossil-based materials",
    )

    # Metal materials
    ALUMINUM = ("3.1", "3.1 Aluminum", "Metal materials")
    STEEL = ("3.2", "3.2 Steel", "Metal materials")
    BRASS_COPPER = ("3.3", "3.3 Brass, copper", "Metal materials")
    METAL_OTHER = ("3.0", "3.0 Other metal materials", "Metal materials")

    # Non-metallic minerals
    BRICK = ("4.1", "4.1 Brick", "Non-metallic minerals")
    CONCRETE = ("4.2", "4.2 Concrete", "Non-metallic minerals")
    GLASS = ("4.3", "4.3 Glass", "Non-metallic minerals")
    MINERAL_INSULATION = ("4.4", "4.4 Mineral insulation", "Non-metallic minerals")
    MINERAL_OTHER = ("4.0", "4.0 Other non-metallic minerals", "Non-metallic minerals")

    # Undefined
    UNDEFINED = ("0.0", "0.0 Undefined materials", "Undefined materials")
    reference = enum_attribute(Reference.INDICATE_MATERIALS_TAXONOMY)


class Material(OpenBDFEnum):
    ALUMINIUM = ("aluminium", "Aluminium", "e.g., alum alloy")
    BAMBOO = ("bamboo", "Bamboo")
    BRASS_COPPER = ("brass_copper", "Brass, copper")
    CEMENT_MORTAR = ("cement_mortar", "Cement mortar, plaster")
    CERAMICS = ("ceramics", "Ceramics", "e.g., fired clay bricks")
    CONCRETE_REINFORCED = ("concrete_reinforced", "Concrete reinforced")
    CONCRETE_UNREINFORCED = (
        "concrete_unreinforced",
        "Concrete w/o reinforcement",
    )
    EARTH = (
        "earth",
        "Earth",
        "e.g., unfired clay, adobe, rammed earth, etc.",
    )
    INSULATION_PLASTIC = ("insulation_plastic", "EPS or XPS", "Insulation")
    FUNGI = ("fungi", "Fungi", "e.g. Mycelium")
    GLASS = ("glass", "Glass", "Single, double, or triple glazing")
    METALS = ("metals", "Metals", "Iron, steel")
    PLASTICS = ("plastics", "Plastics", "Various: PC, PE, PP, PU, PVC")
    STEEL_REINFORCEMENT = ("steel_reinforcement", "Steel (reinforcement)")
    STONE = ("stone", "Stone", "Granite, limestone, etc.")
    STONE_WOOL = ("stone_wool", "Stone wool", "e.g. insulation")
    STRAW_HEMP = ("straw_hemp", "Straw or hemp", "e.g., strawbale")
    TIMBER = ("timber", "Timber, wood")
    OTHER = ("other", "Other")


class MaterialQuantitiesSource(OpenBDFEnum):
    EXTRAPOLATION = (
        "extrapolation",
        "Extrapolation from Construction Type Land Use Area",
    )
    MANUAL_APPROXIMATION = ("manual_approx", "Manual Approximation")
    BIM_MODEL = ("bim_model", "BIM Model")
    DESIGN_ESTIMATES = (
        "design_estimates",
        "Design Estimates/ Manual Takeoff from Design Documentation",
    )
    CONSTRUCTION_ESTIMATE = (
        "construction_estimate",
        "Construction Estimate/Contractors Bill of Materials",
    )
    AS_BUILT = ("as_built", "As-Built")
    OTHER = ("other", "Other Data Source")
    reference = enum_attribute(Reference.EN15978_2026)


class MaterialQuantitiesUnits(OpenBDFEnum):
    PIECE = ("piece", "Piece (pcs)")
    M = ("m", "Length (m)")
    M2 = ("m2", "Area (m²)")
    M3 = ("m3", "Volume (m³)")
    MASS_KG = ("mass_kg", "Mass (kg)")
    kWH = ("kwh", "Energy (kWh)")


class ReplacementCountMethod(OpenBDFEnum):
    INTEGER = (
        "integer",
        "Integer (whole replacements only)",
        "whole replacements only",
    )
    DECIMAL = (
        "decimal",
        "Decimal (fractional replacements allowed)",
        "fractional replacements allowed",
    )
    UNKNOWN = (
        "unknown",
        "Unknown (rule not declared)",
        "rule not declared",
    )
    reference = enum_attribute(Reference.EU2026_52_ANNEX_III)


class MaterialDataType(OpenBDFEnum):
    CPR_DOPC = (
        "cpr_dopc",
        "Cpr dopc (declaration of performance and conformity under the Construction Products Regulation)",
        "declaration of performance and conformity under the Construction Products Regulation",
    )
    ECODESIGN = (
        "ecodesign",
        "Ecodesign (data issued under ecodesign or energy labelling legislation)",
        "data issued under ecodesign or energy labelling legislation",
    )
    PROJECT_SPECIFIC = (
        "project_specific",
        "Project specific (assessment of this project, not issued under those rules)",
        "assessment of this project, not issued under those rules",
    )
    PRODUCT_SPECIFIC = (
        "product_specific",
        "Product specific (assessment of this product, not issued under those rules)",
        "assessment of this product, not issued under those rules",
    )
    PRODUCT_GROUP_AVERAGE = (
        "product_group_average",
        "Product group average (sectoral or industry average)",
        "sectoral or industry average",
    )
    GENERIC = (
        "generic",
        "Generic (background database value)",
        "background database value",
    )
    DEFAULT_VALUE = (
        "default_value",
        "Default value (conservative national default)",
        "conservative national default",
    )
    reference = enum_attribute(Reference.EU2026_52_ANNEX_III)


class MaterialEPDMatch(OpenBDFEnum):
    IDENTICAL = (
        "identical",
        "Identical (the declaration describes this product)",
        "the declaration describes this product",
    )
    SAME_PRODUCT_GROUP = (
        "same_product_group",
        "Same product group (a sectoral average covering it)",
        "a sectoral average covering it",
    )
    PROXY_TECHNOLOGICAL = (
        "proxy_technological",
        "Proxy technological (a different product used as a stand-in)",
        "a different product used as a stand-in",
    )
    PROXY_GEOGRAPHICAL = (
        "proxy_geographical",
        "Proxy geographical (the same product, another region)",
        "the same product, another region",
    )
    PROXY_TEMPORAL = (
        "proxy_temporal",
        "Proxy temporal (the same product, outside the validity of its declaration)",
        "the same product, outside the validity of its declaration",
    )
    REFERENCE_ONLY = (
        "reference_only",
        "Reference only (a broad reference, not a match)",
        "a broad reference, not a match",
    )
    UNKNOWN = (
        "unknown",
        "Unknown (the relationship cannot be established)",
        "the relationship cannot be established",
    )
    reference = enum_attribute(Reference.EN_15941_2024)


class DeclaredUnit(OpenBDFEnum):
    KG = ("kg", "kg")
    T = ("t", "t")
    M3 = ("m3", "m3")
    M2 = ("m2", "m2")
    M = ("m", "m")
    PIECE = ("piece", "piece")
    L = ("L", "L")
    reference = enum_attribute(Reference.EN15804_A2)


class MaterialFlowType(OpenBDFEnum):
    PROCESS = (
        "process",
        "Process (an activity without a material flow)",
        "an activity without a material flow",
    )
    MATERIAL_IN = (
        "material_in",
        "Material in (material entering the building)",
        "material entering the building",
    )
    MATERIAL_OUT = (
        "material_out",
        "Material out (material leaving the building)",
        "material leaving the building",
    )
    MATERIAL_LOSS_IN = (
        "material_loss_in",
        "Material loss in (losses during installation)",
        "losses during installation",
    )
    MATERIAL_LOSS_OUT = (
        "material_loss_out",
        "Material loss out (losses during removal)",
        "losses during removal",
    )
    TRANSPORT_TO_SITE = (
        "transport_to_site",
        "Transport to site (delivery of the product)",
        "delivery of the product",
    )
    TRANSPORT_END_OF_LIFE = (
        "transport_end_of_life",
        "Transport end of life (removal from site)",
        "removal from site",
    )
    ENERGY_IN = (
        "energy_in",
        "Energy in (energy consumed by the process)",
        "energy consumed by the process",
    )
    reference = enum_attribute(Reference.EN15804_A2_ISO_14044_2006)
