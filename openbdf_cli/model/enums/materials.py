from model.enums.openbdf_enum import OpenBDFEnum


class MainStructureType(OpenBDFEnum):
    CONCRETE = ("concrete", "Concrete")
    STEEL = ("steel", "Steel")
    TIMBER = ("timber", "Timber")
    MASONRY = ("masonry", "Masonry")
    OTHER = ("other", "Other")


class OpenBDFMaterialClassification(OpenBDFEnum):
    # Bio-based materials
    WOOD = ("1.1", "Wood", "Bio-based materials")
    BIO_INSULATION = ("1.2", "Bio-based insulation", "Bio-based materials")
    BIO_OTHER = ("1.0", "Other bio-based materials", "Bio-based materials")

    # Fossil-based materials
    PLASTICS = (
        "2.1",
        "Plastics (PC, PE, PP, PU, PVC)",
        "Fossil-based materials",
    )
    FOSSIL_INSULATION = (
        "2.2",
        "Fossil-based insulation",
        "Fossil-based materials",
    )
    FOSSIL_OTHER = (
        "2.0",
        "Other fossil energy materials",
        "Fossil-based materials",
    )

    # Metal materials
    ALUMINUM = ("3.1", "Aluminum", "Metal materials")
    STEEL = ("3.2", "Steel", "Metal materials")
    BRASS_COPPER = ("3.3", "Brass, copper", "Metal materials")
    METAL_OTHER = ("3.0", "Other metal materials", "Metal materials")

    # Non-metallic minerals
    BRICK = ("4.1", "Brick", "Non-metallic minerals")
    CONCRETE = ("4.2", "Concrete", "Non-metallic minerals")
    GLASS = ("4.3", "Glass", "Non-metallic minerals")
    MINERAL_INSULATION = ("4.4", "Mineral insulation", "Non-metallic minerals")
    MINERAL_OTHER = ("4.0", "Other non-metallic minerals", "Non-metallic minerals")

    # Undefined
    UNDEFINED = ("0.0", "Undefined materials", "Undefined materials")


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


class MaterialQuantitiesUnits(OpenBDFEnum):
    PIECE = ("piece", "Piece (pcs)")
    M = ("m", "Length (m)")
    M2 = ("m2", "Area (m²)")
    M3 = ("m3", "Volume (m³)")
    MASS_KG = ("mass_kg", "Mass (kg)")
    kWH = ("kwh", "Energy (kWh)")
