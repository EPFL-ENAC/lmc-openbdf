import json

from sqlmodel import Session, SQLModel, create_engine, select

from openbdf.model.enums.lca import LCAStageOrModuleOrSubModule
from openbdf.model.tables import LCAResultsTallFullRecord


def test_enum_column_round_trips_the_value_used_by_the_json_payload():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(
            LCAResultsTallFullRecord(
                material_id="M001",
                building_bill_materials_slim_record_id=1,
                lca_stage_module_submodule=LCAStageOrModuleOrSubModule.A1,
            )
        )
        session.commit()

    with Session(engine) as session:
        stored = session.exec(select(LCAResultsTallFullRecord)).one()

    assert stored.lca_stage_module_submodule is LCAStageOrModuleOrSubModule.A1
    assert json.loads(stored.model_dump_json())["lca_stage_module_submodule"] == "A1"


def test_every_enum_column_maps_on_enum_values():
    for table in SQLModel.metadata.tables.values():
        for column in table.columns:
            enum_cls = getattr(column.type, "enum_class", None)
            if enum_cls is not None:
                assert column.type.enums == [member.value for member in enum_cls], column.name
