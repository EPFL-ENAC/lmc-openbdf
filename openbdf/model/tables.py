from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from openbdf.model.building_bill_materials_slim import (
    BuildingBillMaterialsSlimRecordBase,
    BuildingBillMaterialsSlimRecordBaseDraft,
)
from openbdf.model.general_info import ProjectRecordBase, ProjectRecordBaseDraft
from openbdf.model.lca_results_full_tall import LCAResultsTallBase
from openbdf.model.lca_results_full_wide import LCAResultsWideFullBase
from openbdf.model.project_material_database import (
    ProjectMaterialDatabaseBase,
    ProjectMaterialDatabaseBaseDraft,
)


class ProjectRecord(ProjectRecordBase, SQLModel, table=True):
    __tablename__ = "project_record"

    id: Optional[int] = Field(default=None, primary_key=True)
    bill_of_materials: list["BuildingBillMaterialsSlimRecord"] = Relationship(back_populates="project")
    project_material_database: list["ProjectMaterialDatabaseRecord"] = Relationship(back_populates="project_record")


class ProjectRecordDraft(ProjectRecordBaseDraft, SQLModel, table=True):
    __tablename__ = "project_record_draft"

    id: Optional[int] = Field(default=None, primary_key=True)
    bill_of_materials: list["BuildingBillMaterialsSlimRecordDraft"] = Relationship(back_populates="project")
    project_material_database: list["ProjectMaterialDatabaseRecordDraft"] = Relationship(
        back_populates="project_record"
    )


class BuildingBillMaterialsSlimRecord(BuildingBillMaterialsSlimRecordBase, SQLModel, table=True):
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


class BuildingBillMaterialsSlimRecordDraft(BuildingBillMaterialsSlimRecordBaseDraft, SQLModel, table=True):  # type: ignore[valid-type,misc]
    __tablename__ = "building_bill_materials_slim_record_draft"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_id: int = Field(foreign_key="project_record_draft.id", nullable=False)
    project: ProjectRecordDraft | None = Relationship(back_populates="bill_of_materials")

    lca_results_full_record: Optional["LCAResultsWideFullRecordDraft"] = Relationship(
        back_populates="building_bill_materials_slim_record"
    )
    lca_results_tall_full_records: list["LCAResultsTallFullRecordDraft"] = Relationship(
        back_populates="building_bill_materials_slim_record"
    )


class ProjectMaterialDatabaseRecord(ProjectMaterialDatabaseBase, SQLModel, table=True):
    __tablename__ = "project_material_database"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_record_id: int = Field(foreign_key="project_record.id", nullable=False)
    project_record: ProjectRecord | None = Relationship(back_populates="project_material_database")


class ProjectMaterialDatabaseRecordDraft(ProjectMaterialDatabaseBaseDraft, SQLModel, table=True):  # type: ignore[valid-type,misc]
    __tablename__ = "project_material_database_draft"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_record_id: int = Field(foreign_key="project_record_draft.id", nullable=False)
    project_record: ProjectRecordDraft | None = Relationship(back_populates="project_material_database")


class LCAResultsWideFullRecord(LCAResultsWideFullBase, SQLModel, table=True):
    __tablename__ = "lca_results_full_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecord
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecord | None = Relationship(
        back_populates="lca_results_full_record"
    )


class LCAResultsWideFullRecordDraft(LCAResultsWideFullBase, SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "lca_results_full_record_draft"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecordDraft
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record_draft.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecordDraft | None = Relationship(
        back_populates="lca_results_full_record"
    )


class LCAResultsTallFullRecord(LCAResultsTallBase, SQLModel, table=True):
    __tablename__ = "lca_results_tall_full_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecord
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecord | None = Relationship(
        back_populates="lca_results_tall_full_records"
    )


class LCAResultsTallFullRecordDraft(LCAResultsTallBase, SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "lca_results_tall_full_record_draft"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to BuildingBillMaterialsSlimRecordDraft
    building_bill_materials_slim_record_id: int = Field(
        foreign_key="building_bill_materials_slim_record_draft.id", nullable=False
    )
    building_bill_materials_slim_record: BuildingBillMaterialsSlimRecordDraft | None = Relationship(
        back_populates="lca_results_tall_full_records"
    )
