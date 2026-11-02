from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBaseIngest
from openbdf.model.general_info import ProjectRecordBaseIngest
from openbdf.model.ingest import make_ingest_model
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import ProjectMaterialDatabaseBaseIngest

# Storage holds drafts as well as complete projects, so every workbook field is
# nullable here. Whether a field is required belongs to the strict models (the *Base
# classes) and to validation, which reads each field's Requirement (E01); a draft is
# a project stored despite those findings. Only the keys that link rows stay NOT NULL.
# The LCA result modules are generated, so their ingest variants are made here, the
# same way the other modules make theirs.
_LCAResultsWideFullBaseIngest = make_ingest_model(LCAResultsWideFullBase)
_LCAResultsTallBaseIngest = make_ingest_model(LCAResultsTallBase)


class LCAResultsWideFullBaseIngest(_LCAResultsWideFullBaseIngest):  # type: ignore[valid-type,misc]
    pass


class LCAResultsTallBaseIngest(_LCAResultsTallBaseIngest):  # type: ignore[valid-type,misc]
    pass


class ProjectRecord(ProjectRecordBaseIngest, SQLModel, table=True):
    __tablename__ = "project_record"

    id: Optional[int] = Field(default=None, primary_key=True)
    bill_of_materials: list["BuildingBillMaterialsSlimRecord"] = Relationship(back_populates="project")
    project_material_database: list["ProjectMaterialDatabaseRecord"] = Relationship(back_populates="project_record")


class BuildingBillMaterialsSlimRecord(BuildingBillMaterialsSlimRecordBaseIngest, SQLModel, table=True):
    __tablename__ = "building_bill_materials_slim_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_id: int = Field(foreign_key="project_record.id", nullable=False)
    project: ProjectRecord | None = Relationship(back_populates="bill_of_materials")

    lca_results_full_record: Optional["LCAResultsWideFullRecord"] = Relationship(
        back_populates="building_bill_materials_slim_record"
    )
    lca_results_tall_full_records: list["LCAResultsTallFullRecord"] = Relationship(
        back_populates="building_bill_materials_slim_record"
    )


class ProjectMaterialDatabaseRecord(ProjectMaterialDatabaseBaseIngest, SQLModel, table=True):
    __tablename__ = "project_material_database"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_record_id: int = Field(foreign_key="project_record.id", nullable=False)
    project_record: ProjectRecord | None = Relationship(back_populates="project_material_database")


class LCAResultsWideFullRecord(LCAResultsWideFullBaseIngest, SQLModel, table=True):
    __tablename__ = "lca_results_full_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecord
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecord | None = Relationship(
        back_populates="lca_results_full_record"
    )


class LCAResultsTallFullRecord(LCAResultsTallBaseIngest, SQLModel, table=True):
    __tablename__ = "lca_results_tall_full_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecord
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecord | None = Relationship(
        back_populates="lca_results_tall_full_records"
    )
