# Database ERD

Every table on `SQLModel.metadata` (`openbdf/model/tables.py`), generated with `make erd`.
Shows the first 20 columns of each table, keys first. Regenerate after changing the models.

```mermaid
erDiagram
  building_bill_materials_slim_record {
    INTEGER id PK
    INTEGER project_id FK
    VARCHAR material_id
    VARCHAR material_ref_id
    VARCHAR custom_floor_level
    INTEGER common_floor_level
    INTEGER floor_repetition
    VARCHAR common_above_below_ground
    VARCHAR bec_custom
    VARCHAR custom_bec_description
    VARCHAR bec_openbdf
    VARCHAR custom_element_name
    VARCHAR work_section
    NUMERIC layer_thickness
    VARCHAR common_material_name
    VARCHAR custom_material_name
    VARCHAR lca_dataset_material_name
    VARCHAR lca_database_name
    VARCHAR lca_dataset_link
    VARCHAR material_data_type
    more columns "10 more"
  }
  lca_results_full_record {
    INTEGER id PK
    INTEGER building_bill_materials_slim_record_id FK
    VARCHAR material_id
    NUMERIC gwp_total_a1_a3
    NUMERIC gwp_total_a1
    NUMERIC gwp_total_a2
    NUMERIC gwp_total_a3
    NUMERIC gwp_total_a4
    NUMERIC gwp_total_a5
    NUMERIC gwp_total_a5_1
    NUMERIC gwp_total_a5_2
    NUMERIC gwp_total_a5_3
    NUMERIC gwp_total_a5_4
    NUMERIC gwp_total_b1
    NUMERIC gwp_total_b1_1
    NUMERIC gwp_total_b1_2
    NUMERIC gwp_total_b2
    NUMERIC gwp_total_b3
    NUMERIC gwp_total_b4
    NUMERIC gwp_total_b5
    more columns "592 more"
  }
  lca_results_tall_full_record {
    INTEGER id PK
    INTEGER building_bill_materials_slim_record_id FK
    VARCHAR material_id
    VARCHAR lca_stage_module_submodule
    VARCHAR lca_stage
    VARCHAR lca_module
    VARCHAR lca_submodule
    INTEGER process_year
    VARCHAR material_flow_type
    NUMERIC material_flow_mass_kg
    VARCHAR scenario_label
    NUMERIC gwp_total
    NUMERIC gwp_f
    NUMERIC gwp_b
    NUMERIC gwp_luc
    NUMERIC odp
    NUMERIC ap
    NUMERIC ap_ae
    NUMERIC ep
    NUMERIC ep_af
    more columns "18 more"
  }
  project_material_database {
    INTEGER id PK
    INTEGER project_record_id FK
    VARCHAR material_ref_id
    VARCHAR custom_material_name
    VARCHAR lca_dataset_material_name
    VARCHAR lca_database_name
    VARCHAR declared_unit
    INTEGER bom_row_count
    NUMERIC material_mass_kg
    NUMERIC material_mass_share
    VARCHAR material_data_type
    VARCHAR material_epd_match
    VARCHAR assessor_note
    VARCHAR product_form
    VARCHAR strength_class
    NUMERIC declared_strength
    VARCHAR exposure_class
    VARCHAR cement_type
    VARCHAR reinforcement_steel_grade
    NUMERIC reinforcement_content
    more columns "5 more"
  }
  project_record {
    INTEGER id PK
    VARCHAR project_id
    VARCHAR project_custom_id
    VARCHAR record_type
    VARCHAR project_units
    VARCHAR project_name
    VARCHAR project_description
    VARCHAR project_construction_type
    VARCHAR project_country
    VARCHAR project_city
    VARCHAR project_state
    VARCHAR project_address
    VARCHAR project_owner_name
    BOOLEAN project_sustainability_certification
    VARCHAR project_sustainability_certification_name
    DATE project_sustainability_certification_date
    VARCHAR project_sustainability_certification_id
    DATE project_permit_date
    VARCHAR project_permit_id
    INTEGER project_no_of_buildings
    more columns "171 more"
  }
  building_bill_materials_slim_record ||--o{ lca_results_full_record : "building_bill_materials_slim_record_id"
  building_bill_materials_slim_record ||--o{ lca_results_tall_full_record : "building_bill_materials_slim_record_id"
  project_record ||--o{ building_bill_materials_slim_record : "project_id"
  project_record ||--o{ project_material_database : "project_record_id"
```
