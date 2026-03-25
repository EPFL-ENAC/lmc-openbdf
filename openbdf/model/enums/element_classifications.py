from .openbdf_enum import OpenBDFEnum


class OpenBDFBuildingElementClassification(OpenBDFEnum):
    # --- TIER 1 ---
    TREATMENT_DEMOLITION_FACILITATING = (
        "0",
        "Treatment and demolition works & Facilitating works",
    )
    SUB_STRUCTURE = ("1", "Sub-structure")
    SUPER_STRUCTURE = ("2", "Super structure")
    FINISHES = ("3", "Finishes")
    FFE = ("4", "FF&E")
    BUILDING_SERVICES_MEP = ("5", "Building Services/ MEP")
    PRE_FABRICATED_UNITS = ("6", "Pre-fabricated buildings and units")
    WORKS_TO_EXISTING = ("7", "Works to existing buildings")
    EXTERNAL_WORKS = ("8", "External works")

    # --- TIER 2 ---
    TREATMENT_DEMOLITION_FACILITATING_01 = (
        "0.1",
        "Treatment and demolition works & Facilitating works",
        None,
        TREATMENT_DEMOLITION_FACILITATING,
    )
    FOUNDATIONS_PILING_11 = (
        "1.1",
        "Foundations and piling",
        None,
        SUB_STRUCTURE,
    )
    BASEMENT_RETAINING_12 = (
        "1.2",
        "Basement retaining walls and lowest slab",
        None,
        SUB_STRUCTURE,
    )
    FRAME_21 = ("2.1", "Frame", None, SUPER_STRUCTURE)
    UPPER_FLOORS_22 = ("2.2", "Upper floors", None, SUPER_STRUCTURE)
    ROOF_23 = ("2.3", "Roof", None, SUPER_STRUCTURE)
    STAIRS_RAMPS_24 = (
        "2.4",
        "Stairs, ramps and safety guarding",
        None,
        SUPER_STRUCTURE,
    )
    EXTERNAL_ENVELOPE_25 = (
        "2.5",
        "External envelope including roof finishes",
        None,
        SUPER_STRUCTURE,
    )
    WINDOWS_EXT_DOORS_26 = (
        "2.6",
        "Windows and ext doors",
        None,
        SUPER_STRUCTURE,
    )
    INTERNAL_WALLS_27 = ("2.7", "Internal walls", None, SUPER_STRUCTURE)
    INTERNAL_DOORS_28 = ("2.8", "Internal doors", None, SUPER_STRUCTURE)
    WALL_FINISHES_31 = ("3.1", "Wall finishes", None, FINISHES)
    FLOOR_FINISHES_32 = ("3.2", "Floor finishes", None, FINISHES)
    CEILING_FINISHES_33 = ("3.3", "Ceiling finishes", None, FINISHES)
    GENERAL_FFE_41 = ("4.1", "General FF&E", None, FFE)
    KITCHEN_EQUIPMENT_42 = ("4.2", "Kitchen equipment", None, FFE)
    SPECIAL_EQUIPMENT_43 = ("4.3", "Special equipment", None, FFE)
    LOOSE_FFE_44 = ("4.4", "Loose FF&E", None, FFE)
    IT_45 = ("4.5", "IT", None, FFE)
    AUDIO_VISUAL_46 = ("4.6", "Audio and visual", None, FFE)
    PUBLIC_HEALTH_51 = ("5.1", "Public Health", None, BUILDING_SERVICES_MEP)
    HVAC_52 = (
        "5.2",
        "Heating, Ventilation and Cooling (HVAC)",
        None,
        BUILDING_SERVICES_MEP,
    )
    ELECTRICAL_INSTALLATIONS_53 = (
        "5.3",
        "Electrical installations",
        None,
        BUILDING_SERVICES_MEP,
    )
    RENEWABLE_ENERGY_54 = (
        "5.4",
        "On site renewable energy generation",
        None,
        BUILDING_SERVICES_MEP,
    )
    SPECIAL_SYSTEMS_55 = (
        "5.5",
        "Systems including Life safety, Fuel, Lift, Waste, and Builders work",
        None,
        BUILDING_SERVICES_MEP,
    )
    PREFAB_UNITS_60 = (
        "6.0",
        "Pre-fabricated buildings and building units",
        None,
        PRE_FABRICATED_UNITS,
    )
    ALTERATIONS_71 = ("7.1", "Alterations", None, WORKS_TO_EXISTING)
    REPAIRS_RENOVATION_72 = (
        "7.2",
        "Repairs, Cleaning and Renovation",
        None,
        WORKS_TO_EXISTING,
    )
    DAMP_PROOFING_73 = (
        "7.3",
        "Damp-proof courses/fungus and beetle eradication",
        None,
        WORKS_TO_EXISTING,
    )
    EXTERNAL_SURFACES_81 = (
        "8.1",
        "Roads, paths, pavings, surfaces, Fencing, railings, walls, External fixtures",
        None,
        EXTERNAL_WORKS,
    )
    LANDSCAPE_PLANTING_82 = (
        "8.2",
        "Soft landscape, planting, irrigation",
        None,
        EXTERNAL_WORKS,
    )
    EXTERNAL_SERVICES_83 = (
        "8.3",
        "External drainage, External services, Minor building works",
        None,
        EXTERNAL_WORKS,
    )

    # --- TIER 3 ---
    TOXIC_DEMOLITION_011 = (
        "0.1.1",
        "Toxic/contaminated material treatment & Demolition works",
        None,
        TREATMENT_DEMOLITION_FACILITATING_01,
    )
    FACILITATING_WORKS_012 = (
        "0.1.2",
        "Facilitating works",
        None,
        TREATMENT_DEMOLITION_FACILITATING_01,
    )
    FOUNDATIONS_PILING_111 = (
        "1.1.1",
        "Foundations and piling",
        None,
        FOUNDATIONS_PILING_11,
    )
    LOWEST_SLAB_121 = (
        "1.2.1",
        "Lowest slab",
        None,
        BASEMENT_RETAINING_12,
    )
    SUSPENDED_SLABS_122 = (
        "1.2.2",
        "Suspended slabs",
        None,
        BASEMENT_RETAINING_12,
    )
    BASEMENT_WALLS_123 = (
        "1.2.3",
        "Basement retaining walls",
        None,
        BASEMENT_RETAINING_12,
    )
    FRAME_VERTICAL_211 = (
        "2.1.1",
        "Frame (vertical) - columns/ structural walls & braces",
        None,
        FRAME_21,
    )
    FRAME_HORIZONTAL_212 = (
        "2.1.2",
        "Frame (Horizontal) - beams, joists & braces",
        None,
        FRAME_21,
    )
    UPPER_FLOOR_STRUCTURAL_221 = (
        "2.2.1",
        "Upper floor - structural slabs",
        None,
        UPPER_FLOORS_22,
    )
    UPPER_FLOOR_NON_STRUCTURAL_222 = (
        "2.2.2",
        "Upper floor - non-structural slabs",
        None,
        UPPER_FLOORS_22,
    )
    ROOF_STRUCTURAL_231 = (
        "2.3.1",
        "Roof - structural slabs",
        None,
        ROOF_23,
    )
    STAIRS_241 = ("2.4.1", "Stairs", None, STAIRS_RAMPS_24)
    RAMPS_242 = ("2.4.2", "Ramps", None, STAIRS_RAMPS_24)
    SAFETY_ACCESS_LADDERS_243 = (
        "2.4.3",
        "Safety and access ladders, chutes, slides and guarding",
        None,
        STAIRS_RAMPS_24,
    )
    OPAQUE_ENVELOPE_251 = (
        "2.5.1",
        "External - opaque envelope",
        None,
        EXTERNAL_ENVELOPE_25,
    )
    FULL_HEIGHT_GLAZING_252 = (
        "2.5.2",
        "External - full height glazing systems",
        None,
        EXTERNAL_ENVELOPE_25,
    )
    ROOF_FINISHES_COVERINGS_253 = (
        "2.5.3",
        "External - roof finishes/coverings",
        None,
        EXTERNAL_ENVELOPE_25,
    )
    EXTERNAL_SAFETY_SYSTEMS_254 = (
        "2.5.4",
        "External - safety systems",
        None,
        EXTERNAL_ENVELOPE_25,
    )
    WINDOWS_VERTICAL_261 = ("2.6.1", "Windows - vertical", None, WINDOWS_EXT_DOORS_26)
    WINDOWS_ROOF_262 = (
        "2.6.2",
        "Windows - roof or horizontal",
        None,
        WINDOWS_EXT_DOORS_26,
    )
    EXTERNAL_DOORS_263 = ("2.6.3", "External doors", None, WINDOWS_EXT_DOORS_26)
    INTERNAL_WALLS_SOLID_271 = ("2.7.1", "Internal walls - solid", None, INTERNAL_WALLS_27)
    INTERNAL_WALLS_GLAZED_272 = (
        "2.7.2",
        "Internal walls - non-structural glazed walls, windows and vision panels",
        None,
        INTERNAL_WALLS_27,
    )
    RAISED_FLOORS_321 = (
        "3.2.1",
        "Raised access floor or specialist sprung floors",
        None,
        FLOOR_FINISHES_32,
    )
    NON_STRUCTURAL_SCREED_322 = ("3.2.2", "Non-structural screed", None, FLOOR_FINISHES_32)
    FLOOR_FINISHES_FINAL_323 = ("3.2.3", "Floor finishes", None, FLOOR_FINISHES_32)
    SANITARYWARE_511 = ("5.1.1", "Sanitaryware", None, PUBLIC_HEALTH_51)
    COLD_WATER_512 = ("5.1.2", "Cold water systems", None, PUBLIC_HEALTH_51)
    DRAINAGE_RAINWATER_513 = (
        "5.1.3",
        "Drainage and rainwater",
        None,
        PUBLIC_HEALTH_51,
    )
    SPACE_HEATING_HOT_WATER_521 = (
        "5.2.1",
        "Space heating and hot water",
        None,
        HVAC_52,
    )
    COOLING_INSTALLATIONS_522 = (
        "5.2.2",
        "Dedicated cooling installations",
        None,
        HVAC_52,
    )
    AIR_MOVEMENT_523 = ("5.2.3", "Air movement", None, HVAC_52)
    VENT_TERMINALS_DUCTWORK_524 = (
        "5.2.4",
        "Ventilation air terminals, ductwork and fire safety",
        None,
        HVAC_52,
    )
    LIGHTING_531 = ("5.3.1", "Lighting", None, ELECTRICAL_INSTALLATIONS_53)
    ELECTRICAL_POWER_COMM_532 = (
        "5.3.2",
        "Electrical services for power, communications, security, IT and fire detection",
        None,
        ELECTRICAL_INSTALLATIONS_53,
    )
    RENEWABLE_GENERATION_541 = (
        "5.4.1",
        "On site renewable energy generation",
        None,
        RENEWABLE_ENERGY_54,
    )
    LIFE_SAFETY_551 = ("5.5.1", "Life safety", None, SPECIAL_SYSTEMS_55)
    FUEL_INSTALLATIONS_552 = ("5.5.2", "Fuel installations", None, SPECIAL_SYSTEMS_55)
    LIFT_CONVEYOR_553 = (
        "5.5.3",
        "Lift and conveyor installations",
        None,
        SPECIAL_SYSTEMS_55,
    )
    WASTE_DISPOSAL_554 = (
        "5.5.4",
        "Specialised and communal waste disposal",
        None,
        SPECIAL_SYSTEMS_55,
    )
    SPECIALIST_MAINTENANCE_555 = (
        "5.5.5",
        "Specialist installations & maintenance",
        None,
        SPECIAL_SYSTEMS_55,
    )
    BUILDERS_WORK_SERVICES_556 = (
        "5.5.6",
        "Builders work in connection with services",
        None,
        SPECIAL_SYSTEMS_55,
    )
    ROADS_PATHS_PAVING_811 = (
        "8.1.1",
        "Roads, paths, pavings, surfaces",
        None,
        EXTERNAL_SURFACES_81,
    )
    FENCING_RAILING_WALLS_812 = (
        "8.1.2",
        "Fencing, railings, walls",
        None,
        EXTERNAL_SURFACES_81,
    )
    EXTERNAL_FIXTURES_813 = (
        "8.1.3",
        "External fixtures",
        None,
        EXTERNAL_SURFACES_81,
    )
    EXTERNAL_DRAINAGE_831 = (
        "8.3.1",
        "External drainage",
        None,
        EXTERNAL_SERVICES_83,
    )
    EXTERNAL_SERVICES_DIST_832 = (
        "8.3.2",
        "External services",
        None,
        EXTERNAL_SERVICES_83,
    )
    MINOR_BUILDING_WORKS_833 = (
        "8.3.3",
        "Minor building works, ancillary",
        None,
        EXTERNAL_SERVICES_83,
    )

    # --- TIER 4 ---
    TOXIC_TREATMENT_0111 = (
        "0.1.1.1",
        "Toxic/contaminated material treatment",
        "Removal and disposal of any hazardous materials (eg asbestos), including any material from existing services installations or tanks or removal of toxic chemicals. Environmental treatment or removal of contaminated ground. Eradication of plant growth.",
        TOXIC_DEMOLITION_011,
    )
    DEMOLITION_WORKS_0112 = (
        "0.1.1.2",
        "Demolition works",
        "Demolition in this context is anything that covers a more extensive scope of works than alterations. Removal/deconstruction/demolition of existing structure, envelope, fabric, fittings and services of an existing building such as required to create clear site conditions for new asset. Removing and disposing of complete building or structure including services, fittings and finishes.",
        TOXIC_DEMOLITION_011,
    )
    TEMPORARY_SUPPORTS_0121 = (
        "0.1.2.1",
        "Temporary supports",
        "Temporary fencing, provision of support to unstable structures but not forming part of the ardpanent works. Does not include supports for facade retention, which is included below. Any removal or disposal also included.",
        FACILITATING_WORKS_012,
    )
    FACADE_RETENTION_0122 = (
        "0.1.2.2",
        "Facade retention",
        "Works related to facade retention. Includes addition and removal of any dedicated, facade supports required. May include ardpanent additions such as dead, raking, flying or box shores, wall plates, needles, brackets, blockings, wedges, dog-irons or other similar metal work. Foundations to any shores.",
        FACILITATING_WORKS_012,
    )
    SPECIALIST_GROUNDWORKS_0123 = (
        "0.1.2.3",
        "Specialist groundworks",
        "Site de-watering and pumping. Soil stabilisation, site formation and slope treatment including erosion control, specialist site surface clearance not included in 8.1 Site Preparation below (clearing, grubbing, topsoil stripping, tree felling, minor earthwork removals). Gas venting.",
        FACILITATING_WORKS_012,
    )
    TEMPORARY_DIVERSION_0124 = (
        "0.1.2.4",
        "Temporary diversion works",
        "Temporary surface drainage, temporary protection, diversion and relocation of public utilities. Include works required to divert and re-instate for new asset/clear ground condition.",
        FACILITATING_WORKS_012,
    )
    EXTRAORDINARY_INVESTIGATIONS_0125 = (
        "0.1.2.5",
        "Extraordinary site investigations",
        "Archaeological investigations, wildlife mitigation measures (relocation to new habitat/protection/barriers).",
        FACILITATING_WORKS_012,
    )
    SITE_PREPARATION_0126 = (
        "0.1.2.6",
        "Site preparation works",
        "Covers getting the whole site to formation level, including the building footprint. Earthworks required to create new paths and roadways (including any disposal required). Disposal or management of surface/groundwater. General (non-specialist) vegetaion removel, tree felling, tree protection, extraction and disposal of old piles. Breaking out and disposal of existing sub-structures, hard surfacing, drainage systems, utilities networks. Filling of dis-used manholes, shafts and pits. Removal of underground storage tanks.",
        FACILITATING_WORKS_012,
    )
    FOUNDATIONS_PILING_1110 = (
        "1.1.1.0",
        "Foundations and piling",
        "Strips, rafts, piling, pile caps and underpinning. Foundations up to top of lowest floor slabs (inc insulation and waterproofing). Include breaking out of hard surfaces, excavations required, disposal and earthwork support. (Any vertical supports for basements included below.) Includes drainage and services within the building footprint to the point of the first junction or manhole outside of this area.",
        FOUNDATIONS_PILING_111,
    )
    LOWEST_SLAB_1210 = (
        "1.2.1.0",
        "Lowest slab",
        "Entire lowest floor assembly below the underside of screed or lowest floor slab. Can be ground bearing or suspended. To include any structural screed and underslab waterproofing and insulation. Formation of sumps, pits, chambers, tanks, swimming pool base integral to the lowest floor construction. Non-structural items including screed, insulation/DPM above slab,",
        LOWEST_SLAB_121,
    )
    SUSPENDED_SLABS_1220 = (
        "1.2.2.0",
        "Suspended slabs",
        "Slabs within the basement box. Can include a slab that forms the entrance to the building where the ground is sloping. For the purposes of this measurement the ground slab is the highest one you can enter the building from. Entrance slab and those suspended below are included in this category, while those above are included in the upper floor slabs.",
        SUSPENDED_SLABS_122,
    )
    BASEMENT_WALLS_1230 = (
        "1.2.3.0",
        "Basement retaining walls",
        "Basement retaining walls (inc. vertical retaining structure, insulation and waterproofing external to the wall). To include lift pit lateral supports and any ardpanent, vertical retaining structures within building envelope.",
        BASEMENT_WALLS_123,
    )
    FRAME_VERTICAL_2110 = (
        "2.1.1.0",
        "Frame (vertical)  - columns/ structural walls & braces",
        "Structural vertical framed elements including columns, structural walls or braces that are supporting a floor or roof (inc. connections, formwork, ardpanent structural casing and any fire proofing). Core and shear walls are included here.",
        FRAME_VERTICAL_211,
    )
    FRAME_HORIZONTAL_2120 = (
        "2.1.2.0",
        "Frame (Horizontal) - beams, joists & braces",
        "Horizontal structural framed elements including beams, joists or braces (inc. connections and any fire proofing). Will include any structural framing for roof (e.g. where pitched) and external or internal wall assembly (e.g. secondary framing, lintels or wind posts without which architectural wall elements would fail). Note: monolithic beam structures cast with the structural slab are included in 2.2.1.",
        FRAME_HORIZONTAL_212,
    )
    UPPER_FLOOR_STRUCTURAL_2210 = (
        "2.2.1.0",
        "Upper floor - structural slabs",
        "Horizontal structural slabs above the lowest and suspended slabs. Including monolithic horizontal beams or joists (inc. connections, formwork, ardpanent structural casing and any fire proofing).",
        UPPER_FLOOR_STRUCTURAL_221,
    )
    UPPER_FLOOR_NON_STRUCTURAL_2220 = (
        "2.2.2.0",
        "Upper floor - non-structural slabs",
        "Horizontal, non-structural slabs above the lowest and suspended slabs (inc. any slab to slab connections, fire proofing and ardpanent formwork or lining that is integral to the system). Structural support or enclosures for tanks or pools (above lowest slab level). Includes: Mezzanine structures, Structural slabs to corridors or bridges (internal or external), Maintenance routes or interstitial plant floor, Structure to support tiered seating, internal galleries.",
        UPPER_FLOOR_NON_STRUCTURAL_222,
    )
    ROOF_STRUCTURAL_2310 = (
        "2.3.1.0",
        "Roof - structural slabs",
        "Includes roof structural slab that forms primary support to roof or thermal enclosure/weather protection to an internal space below. This would include terraces, inset balconies, bolt on balcony structures or podium landscaping (inc. formwork, structural screed, ardpanent structural casing and any fire proofing). Insulation, weather protection, rainwater goods/drainage and final finish to roof included in 2.5 below.",
        ROOF_STRUCTURAL_231,
    )
    STAIRS_2410 = (
        "2.4.1.0",
        "Stairs",
        "Stairs flights excluding any final finishes but inc any fire proofing. Include connections, but ensure not to double count horizontal slab or structure. Include the structural element of any balustrade. Architectural balustrade linings included in internal assemblies and finishes. Where stairs are external but connected to it and required for the escape strategy of the asset, include them within the building calculation. If part of the external works, including them in category 8.",
        STAIRS_241,
    )
    RAMPS_2420 = (
        "2.4.2.0",
        "Ramps",
        "Ramps lengths excluding any final finishes but inc any fire proofing. Include connections, but ensure not to double count horizontal slab or structure. Include the structural element of any balustrade. Architectural balustrade linings included in internal assemblies and finishes. Where ramps are external but connected to it and required for the escape strategy of the asset, include them within this category. If part of the external works, including them in category 8.",
        RAMPS_242,
    )
    LADDERS_CHUTES_2430 = (
        "2.4.3.0",
        "Safety and access ladders, chutes, slides and guarding",
        "Internal and external vertical access ladders for fire escape, access or maintenance. Chute or slide linings within structural and boarded enclosures. Including finishes and fixings. Internal/external balcony and/or roof guarding including structure and finishes where this is not part of the thermal line of the building. Includes juliette balcony guarding.",
        SAFETY_ACCESS_LADDERS_243,
    )
    OPAQUE_ENVELOPE_2510 = (
        "2.5.1.0",
        "External - opaque envelope",
        "External wall build up outside to inside, including final internal boarding, excluding specialist internal linings and final finishes. Including: all fixings and bracketry to connect back to primary and SFS package; ties, DPMs, cavity trays, closers, fire barriers and reveals; external shading, canopies, shutters, not part of the window/glazing/door system; architectural boarding and finishes to balcony guarding; louvred or grille assemblies; roller shutters; external rainwater goods; insulated underside of returns; parapets and railings; chimneys/green walls.",
        OPAQUE_ENVELOPE_251,
    )
    FULL_HEIGHT_GLAZING_2520 = (
        "2.5.2.0",
        "External - full height glazing systems",
        "Floor to ceiling curtain walling or untised/framed construction or structural glazing. Including glazed units, gaskets, framing, bracketry and connections back to structure. Where same system includes solid or insulated spandrel panels include these here. Include films, blinds, insect protection that are integral to glazing system. Include any photovoltaic material integral to the thermal and weather protection of the building. If energy-generation is building mounted but not part of the thermal envelope include in MEP below. Include glazed shop fronts where these are full height. Where external doors are integrated into glazed screens and cannot be separated, please see note in external doors below.",
        FULL_HEIGHT_GLAZING_252,
    )
    ROOF_FINISHES_2530 = (
        "2.5.3.0",
        "External - roof finishes/coverings",
        "Solid roof finishes above structure including non-structural screeds for falls, waterproofing, insulation and final finish including green rooves. Where eaves hang out over external walls those are included. Finishes to balconies and terraces about structure where these form part of the thermal line are included here. Include external rainwater goods and rainwater drainage equipment/ guttering that might runs horizontally to falls externally over roof assemblies. Access or AOV hatches that form part of the thermal roofline.",
        ROOF_FINISHES_COVERINGS_253,
    )
    EXTERNAL_SAFETY_2540 = (
        "2.5.4.0",
        "External - safety systems",
        "Including fall protection/safety equipment for cleaning and maintenance operatives (e.g. handrails, latchways, cradle systems). For powered equipment include all parts of the system, but power distribution is included in MEP below.",
        EXTERNAL_SAFETY_SYSTEMS_254,
    )
    WINDOWS_VERTICAL_2610 = (
        "2.6.1.0",
        "Windows - vertical",
        "Windows that are punched into a solid wall construction and are part of the thermal building line. Including vertical dormer windows. Include films, blinds, shutters insect protection that are integral to glazing system and not separately building mounted. Including cills.",
        WINDOWS_VERTICAL_261,
    )
    WINDOWS_ROOF_2620 = (
        "2.6.2.0",
        "Windows - roof or horizontal",
        "Rooflights and structural glazed rooves that form the thermal and weather protection as part of a roof construction. Including frame, trims, thresholds, ironmongery, closers. Include films, blinds, shutters, insect protection that are integral to system and not separately building mounted. For automatic opening include all parts of the system, but power distribution is included in MEP below.",
        WINDOWS_ROOF_262,
    )
    EXTERNAL_DOORS_2630 = (
        "2.6.3.0",
        "External doors",
        "External doors that form part of the thermal building line whether solid, glazed or revolving. Fanlights or sidelights integral to the door system are included. Including frame, trims, thresholds, ironmongery, closers. Include films, blinds, shutters, insect protection that are integral to door system and not separately building mounted. For automatic doors include all parts of the system, but power distribution is included in MEP below.",
        EXTERNAL_DOORS_263,
    )
    INTERNAL_WALLS_SOLID_2710 = (
        "2.7.1.0",
        "Internal walls  -solid",
        "Non-structural/non-loadbearing internal wall assemblies including studs from floor to ceiling and boarding. Includes: unfinished boarded linings to structural walls, internal boarding to balcony walls and stair/ramp balustrades, insulation, internal cubicle systems, internal planters, internal green walls, deflection heads.",
        INTERNAL_WALLS_SOLID_271,
    )
    INTERNAL_WALLS_GLAZED_2720 = (
        "2.7.2.0",
        "Internal walls  - non-structural glazed walls, windows and vision panels",
        "Non-structural/non-loadbearing internal glazed wall assemblies. Includes: framing and fixings, integral blinds, films, punched windows in solid walls. Where internal doors are integrated into glazed screens and cannot be separated, please see note in internal doors below.",
        INTERNAL_WALLS_GLAZED_272,
    )
    INTERNAL_DOORS_2800 = (
        "2.8.0.0",
        "Internal doors",
        "Internal doors inc. movable walls, sliding, folding doors, fire shutters and doors in glazed screens. Fanlights or sidelights integral to the door system are included. Including framing, trims, thresholds, fixings, vision panels, ironmongery, hinges, closers, hooks, fire/acoustic seals, integral blinds and films.",
        INTERNAL_DOORS_28,
    )
    WALL_FINISHES_3100 = (
        "3.1.0.0",
        "Wall finishes",
        "Internal wall finishes and specialist architectural linings applied/sprayed/painted over general boarding or structural elements. Include: taping, skim coats and plastering, final wall finish, skirtings, trims, adhesive/framing, fire protection, tiled finishes, vertical acoustic panelling, wall protection.",
        WALL_FINISHES_31,
    )
    RAISED_FLOORS_3210 = (
        "3.2.1.0",
        "Raised access floor or specialist sprung floors",
        "Raised access/floating floors, specialist sprung floors. Including internal and any external areas under cover and cavity barriers in any floor voids. Include the concrete dust sealer in this category.",
        RAISED_FLOORS_321,
    )
    NON_STRUCTURAL_SCREED_3220 = (
        "3.2.2.0",
        "Non-structural screed",
        "Non-structural screed or insulation to make up floor to tinal finish. Including internal and any external areas under cover.",
        NON_STRUCTURAL_SCREED_322,
    )
    FLOOR_FINISHES_3230 = (
        "3.2.3.0",
        "Floor finishes",
        "Internal floor finishes above structure. Including internal and any external areas under cover, internal stairs (risers and treads) and/or ramps within the designated footprint. Final architectural finish including tiles, sheet flooring, painting, sealing, adhesive fixings, boarding, mats and matwells. Tiled linings to swimming pools included here. Line markings in internal car parks/sports halls, etc.",
        FLOOR_FINISHES_FINAL_323,
    )
    CEILING_FINISHES_3300 = (
        "3.3.0.0",
        "Ceiling finishes",
        "Internal ceiling finishes and specialist architectural linings applied/sprayed/ mounted/hung/painted from horizontal structural elements (slabs and beams). Include: boarding, insulation, taping, skim coats and plastering, final finish and any trims, adhesive/framing/fixing, access hatches, fire protection and cavity barriers in ceiling voids, acoustic panelling/systems.",
        CEILING_FINISHES_33,
    )
    GENERAL_FFE_4100 = (
        "4.1.0.0",
        "General FF&E",
        "Fittings that are part of the building fabric and loose items. Built in counters, desks, drawers, cupboards, kitchen units, storage, lockers, seating, mirrors, fireplace/hearth, statutory safety signage. Blinds/curtains, bird/insect/animal control, bins, chairs, tables, desks, rugs, lamps, wayfinding signage, whiteboards, loose fire fighting equipment, decorative art, planting, vending machines. Includes items that do not involve plumbing like shower screens, hand dryers, hooks.",
        GENERAL_FFE_41,
    )
    KITCHEN_EQUIPMENT_4200 = (
        "4.2.0.0",
        "Kitchen equipment",
        "Including plug-in and fixed appliances and white goods, cookers, fridge, freezer, dishwasher.",
        KITCHEN_EQUIPMENT_42,
    )
    SPECIAL_EQUIPMENT_4300 = (
        "4.3.0.0",
        "Special equipment",
        "Equipment that would be required only related to a specialist use including sports, leisure, entertainment, theatrical, medical, research or laboratory functions. Fixed accessibility equipment like hoists. Specialist gas terminals/taps.",
        SPECIAL_EQUIPMENT_43,
    )
    LOOSE_FFE_4400 = (
        "4.4.0.0",
        "Loose FF&E",
        "Loose (usually client supply) fittings, furniture and equipment (that would not fall out of the building if turned upside down). Including specialist theatrical equipment.",
        LOOSE_FFE_44,
    )
    IT_4500 = (
        "4.5.0.0",
        "IT",
        "Loose (usually client supply) IT items including computers CRAH units. Telephones and WiFi. Cabling contained below in MEP electrical.",
        IT_45,
    )
    AUDIO_VISUAL_4600 = (
        "4.6.0.0",
        "Audio and visual",
        "Audio/visual equipment (usually client supply) including screens, mics, speakers, projection systems. Cabling contained below in MEP electrical.",
        AUDIO_VISUAL_46,
    )
    SANITARYWARE_5110 = (
        "5.1.1.0",
        "Sanitaryware",
        "Sanitaryware - any appliance that is ardpanently plumbed into the washing or toilet areas. Including toilet, cistern, shower tray, bath, taps, controls, shower heads, basin units, sink, instant hot water heater, washing machine, dishwasher, autoclave.",
        SANITARYWARE_511,
    )
    COLD_WATER_SYSTEMS_5121 = (
        "5.1.2.1",
        "Cold water systems",
        "Thermostat, thermal meters, cold water meters, pumps/booster set, other meters, pipework, pipe insulation, support/hanger, frost protection and trace heating equipment.",
        COLD_WATER_512,
    )
    COLD_WATER_STORAGE_5122 = (
        "5.1.2.2",
        "Cold water storage",
        "Storage tank, CAT 5 system, Treatment and filtration system for wholesome water.",
        COLD_WATER_512,
    )
    SURFACE_FOUL_DRAINAGE_5131 = (
        "5.1.3.1",
        "Surface water/rainwater/foul water drainage",
        "Piping, insulation, support, rainwater storage tank, attenuation, outlets, pumps, downpipes), sewage piping, condensate piping, insulation, support, cistern, traps, pump, drain.",
        DRAINAGE_RAINWATER_513,
    )
    WATER_REUSE_5132 = (
        "5.1.3.2",
        "Water reuse systems",
        "Grey water/rain water harvesting storage tank, pipework and treatment equipment inside the building line.",
        DRAINAGE_RAINWATER_513,
    )
    HEAT_GENERATION_5211 = (
        "5.2.1.1",
        "Heat & Hot water generation equipment",
        "Gas/electric boiler, air/water/ground heat pumps, chiller, local water heater, wood burning stove, biomass boiler, solar thermal. Communal heating systems where housed within the building footprint until it gets to the meter. Plate heat exchanger and hot water generation equipment (e.g. calorifier).",
        SPACE_HEATING_HOT_WATER_521,
    )
    HEAT_DISTRIBUTION_5212 = (
        "5.2.1.2",
        "Heat & hot water distribution, control, ancillaries, emitters, exchangers/ terminal units",
        "Electric radiator, wet radiator, underfloor heating, etc. heat interface unit, plate heat exchanger, pumps, mechanical switchboard, pressurisation unit, dosing pot, BC box, dehumidifier, vibration mounts, thermostat, thermal meters, hot water meter, pipework, pipe insulation, support/hanger, frost protection and trace heating equipment.",
        SPACE_HEATING_HOT_WATER_521,
    )
    HEAT_STORAGE_5213 = (
        "5.2.1.3",
        "Heat storage equipment",
        "Hot water store, buffer vessel, expansion vessel.",
        SPACE_HEATING_HOT_WATER_521,
    )
    COOLING_GENERATION_5221 = (
        "5.2.2.1",
        "Cooling generation equipment",
        "Cooling tower, fan coil units.",
        COOLING_INSTALLATIONS_522,
    )
    COOLING_DISTRIBUTION_5222 = (
        "5.2.2.2",
        "Cooling emitter, exchangers/ terminal units, ancillaries and control, distribution, storage",
        "Cold water store, buffer vessel, expansion vessel for cooling, pumps, mechanical switchboard, pressurisation unit, dosing pot, BC box, dehumidifier, vibration mounts, thermostat, thermal meters, cold water meter, pipework, pipe insulation, support/hanger, frost protection and trace heating equipment.",
        COOLING_INSTALLATIONS_522,
    )
    AIR_MOVEMENT_5230 = (
        "5.2.3.0",
        "Air movement",
        "Fans, MVHR, AHU, ceiling fans, Kitchen ventilation, air curtains.",
        AIR_MOVEMENT_523,
    )
    AIR_TERMINALS_5241 = (
        "5.2.4.1",
        "Air terminals",
        "Diffusers, grilles, VAV, Louvre, CAV, etc.",
        VENT_TERMINALS_DUCTWORK_524,
    )
    DUCTWORK_5242 = (
        "5.2.4.2",
        "Ductwork & ancilleries",
        "Ductwork, insulation, support, fire rated ductwork, support.",
        VENT_TERMINALS_DUCTWORK_524,
    )
    VENT_SAFETY_CONTROLS_5243 = (
        "5.2.4.3",
        "Control dampers, attenuation and fIre safety related to ventilation equipment",
        "VAV damper, volume control damper, fire damper, fume and smoke extraction. Motorised fire smoke damper, stair case pressurisation, fire rated fans, pressure relief dampers, controls, louvres, gas extract. Also including acoustic attenuation.",
        VENT_TERMINALS_DUCTWORK_524,
    )
    INTERNAL_LIGHTING_5311 = (
        "5.3.1.1",
        "Internal lighting",
        "Internal light fixtures, outlet, junction box, socket, light control, cable, switch.",
        LIGHTING_531,
    )
    EXTERNAL_LIGHTING_5312 = (
        "5.3.1.2",
        "External lighting (building mounted)",
        "Lamps/ poles/ supports etc that are building mounted. External light fixtures, outlet, junction box, socket, light control, cable, switch.",
        LIGHTING_531,
    )
    EMERGENCY_LIGHTING_5313 = (
        "5.3.1.3",
        "Emergency lighting",
        "Emergency lights, controls, cable, switch.",
        LIGHTING_531,
    )
    OTHER_LIGHTING_5314 = (
        "5.3.1.4",
        "Other lighting",
        "Task lighting, stage/entertainment lighting, retail display lighting, architectural lighting including associated light fixture, outlet, junction box, socket, light control, cable, switch.",
        LIGHTING_531,
    )
    ELECTRICAL_POWER_5321 = (
        "5.3.2.1",
        "Electrical power",
        "Includes internal and building mounted installations. Power cable, cable trays containment, panel board/ distribution, back up equipment, busbar, transformer, sockets/ switches, floor boxes, sensors. It includes high voltage, low voltage, small power, containment.",
        ELECTRICAL_POWER_COMM_532,
    )
    ELV_SECURITY_COMM_5322 = (
        "5.3.2.2",
        "ELV/ Communications/Security",
        "ELV: Low, medium and high voltage systems; Security: CCTV equipment, security sensors and alarm; Communications and audio visual equipment",
        ELECTRICAL_POWER_COMM_532,
    )
    IT_DATA_5323 = (
        "5.3.2.3",
        "IT & Data",
        "IT equipment: anything related to data, e.g. wifi equipment, server, backbone and structured cabling (cat6, etc.), computers, printers, data cabinets, patch panels, etc.",
        ELECTRICAL_POWER_COMM_532,
    )
    BMS_5324 = (
        "5.3.2.4",
        "BMS",
        "BMS/controllers on fan coils, outstation, main controller system with computer (headend), cabling required, control valves, sensors for temperature statistics, etc.",
        ELECTRICAL_POWER_COMM_532,
    )
    BACKUP_GENERATION_5325 = (
        "5.3.2.5",
        "Electricity back up generation",
        "UPS back up generation, battery supply, stand by generators within the building line.",
        ELECTRICAL_POWER_COMM_532,
    )
    FIRE_DETECTION_5326 = (
        "5.3.2.6",
        "Fire detection & alarm",
        "Fire alarm systems including detection, cabling, fire fighting panel and final call unit.",
        ELECTRICAL_POWER_COMM_532,
    )
    RENEWABLE_ELECTRICAL_5411 = (
        "5.4.1.1",
        "Renewable energy - electrical generation onsite and building mounted",
        "Solar PV panel, inverter, wind turbine, water turbine building mounted or within building footprint.",
        RENEWABLE_GENERATION_541,
    )
    RENEWABLE_STORAGE_5412 = (
        "5.4.1.2",
        "Renewable energy - storage onsite",
        "battery within building footprint.",
        RENEWABLE_GENERATION_541,
    )
    SPRINKLER_SYSTEM_5511 = (
        "5.5.1.1",
        "Sprinkler system",
        "Pipes, heads, valves, tank, hose, pumps.",
        LIFE_SAFETY_551,
    )
    FIRE_FIGHTING_SYSTEMS_5512 = (
        "5.5.1.2",
        "Fire fighting systems",
        "Dry and wet riser, hydrant, within designated building footprint, AOV controls/ sensors, fire suppression system.",
        LIFE_SAFETY_551,
    )
    LIGHTNING_PROTECTION_5513 = (
        "5.5.1.3",
        "Lightning protection/earth bonding",
        "Lightning conductor, earth rods.",
        LIFE_SAFETY_551,
    )
    FUEL_INSTALLATIONS_5520 = (
        "5.5.2.0",
        "Fuel installations",
        "All fuel supplies other than electric, anything pumped or pressurised. Gas equipment: connection, Gas meter, pressure regulator, pipes, valves; Fuel storage tank on site, dry stores; Augers",
        FUEL_INSTALLATIONS_552,
    )
    LIFT_PLATFORM_5531 = (
        "5.5.3.1",
        "Lift, stair lift, lifting platform",
        "To include the systems, but power to the system included in Electrical Installations.",
        LIFT_CONVEYOR_553,
    )
    ESCALATORS_WALKWAYS_5532 = (
        "5.5.3.2",
        "Escalators and moving walkways",
        "To include the systems, but power to the system included in Electrical Installations.",
        LIFT_CONVEYOR_553,
    )
    WASTE_DISPOSAL_5540 = (
        "5.5.4.0",
        "Specialised and communal waste disposal",
        "Refuse, incinerators and any systems for specialist/ communal waste streams and disposal installation.",
        WASTE_DISPOSAL_554,
    )
    SPECIALIST_MAINTENANCE_INSTALLS_5550 = (
        "5.5.5.0",
        "Specialist installations & maintenance",
        "Equipment that is specialist but not fixed (labs, cold rooms, hospitals, museums, religious buildings). Maintenance equipment, Powered building signage, laboratory gases, carbon capture, central vacuum systems, etc.",
        SPECIALIST_MAINTENANCE_555,
    )
    BUILDERS_WORK_MEP_5560 = (
        "5.5.6.0",
        "Builders work in connection with services",
        "Sleeves, fire stopping to protect penetrations (not within ducts/systems), access platform, step overs, plinths.",
        BUILDERS_WORK_SERVICES_556,
    )
    PREFAB_VOLUMETRIC_6000 = (
        "6.0.0.0",
        "Pre-fabricated buildings and building units",
        "Only include Category 1 MMC (volumetric off-site) in this category and only report total emissions at concept stage. Following this, the pre-fabricated volumetric elements must be broken downs into their constituent building elements.",
        PREFAB_UNITS_60,
    )
    ALTERATIONS_GENERAL_7100 = (
        "7.1.0.0",
        "Alterations",
        "Minor removal/alteration/cutting back of minor portion of existing structure, envelope, fabric, fittings and services of an existing building. Deemed minor enough not to report under demolitions above.",
        ALTERATIONS_71,
    )
    REPAIRS_RENOVATION_WORKS_7200 = (
        "7.2.0.0",
        "Repairs, Cleaning and General Renovation works",
        "Materials and processes required for repairs to retained items (masonry, concrete, metal, timber, plastic repairs). Removal of stains, soots, growths, vegetation, bird droppings and similar.",
        REPAIRS_RENOVATION_72,
    )
    DAMP_FUNGUS_ERADICATION_7300 = (
        "7.3.0.0",
        "Damp-proof courses/fungus and beetle eradication",
        "Injecting or installation of chemical/mortar/mechanical damp-proof courses. Opening up works and cutting out or chemical treatment of infested existing building material.",
        DAMP_PROOFING_73,
    )
    ROADS_PATHS_SURFACES_8110 = (
        "8.1.1.0",
        "Roads, paths, pavings, surfaces",
        "Preparation of sub-base works, blinding, in-situ concrete, kerbs, macadam, masonry paving, gravel, surfaces for playgrounds/sports. Drainage management (cat's eyes, tree grilles, traffic calming). Steps and ramps outside building line.",
        ROADS_PATHS_PAVING_811,
    )
    FENCING_RAILING_WALLS_8120 = (
        "8.1.2.0",
        "Fencing, railings, walls",
        "Timber, metal, concrete, masonry fencing, railing, gates, walls that are external and not part of the building thermal envelope. Includes retaining walls not part of the building, gabions, and associated substructures.",
        FENCING_RAILING_WALLS_812,
    )
    EXTERNAL_FIXTURES_8130 = (
        "8.1.3.0",
        "External fixtures",
        "Site street furniture, gates, turnstiles, bollards, seats, litter bins, cycle stands, directional signage, flag poles, playground equipment, shelters, sculptures, ornamental water features.",
        EXTERNAL_FIXTURES_813,
    )
    SOFT_LANDSCAPE_8200 = (
        "8.2.0.0",
        "Soft landscape, planting, irrigation",
        "Seeding and turfing, preparing soil, hedges, shrubs, trees, reed beds. Irrigation systems including pipelines, storage tanks, controls. Sub-structure for tree pits in hard landscape areas.",
        LANDSCAPE_PLANTING_82,
    )
    EXTERNAL_DRAINAGE_8310 = (
        "8.3.1.0",
        "External drainage",
        "Foul water/surface water/land drainage from first manhole beyond the building. Including trenches, pipelines, gullies, pumping stations, soakaways, cesspools, petrol interceptors, and SUDS (not planted).",
        EXTERNAL_DRAINAGE_831,
    )
    EXTERNAL_SERVICES_WORKS_8320 = (
        "8.3.2.0",
        "External services",
        "Piped water supply, high/low voltage electricity distribution from undertaker, natural gas supply/LPG distribution, telecommunications/IT connections from provider, external fuel storage, external site/street lighting, external security/CCTV.",
        EXTERNAL_SERVICES_DIST_832,
    )
    MINOR_BUILDING_WORKS_8330 = (
        "8.3.3.0",
        "Minor building works, ancillary",
        "Refurbishment/alteration to existing separate external small ancillary buildings (boiler houses, sub-stations, guard huts, bicycle stores). Small repairs to fencing/walls/barriers. Under-pinning to existing external walls.",
        MINOR_BUILDING_WORKS_833,
    )
