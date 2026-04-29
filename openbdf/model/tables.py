from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from openbdf.model.building_bill_materials_slim import BuildingBillMaterialsSlimRecordBase
from openbdf.model.general_info import ProjectRecordBase


class ProjectRecord(ProjectRecordBase, SQLModel, table=True):
    __tablename__ = "project_record"

    id: Optional[int] = Field(default=None, primary_key=True)
    bill_of_materials: list["BuildingBillMaterialsSlimRecord"] = Relationship(back_populates="project")


class BuildingBillMaterialsSlimRecord(BuildingBillMaterialsSlimRecordBase, SQLModel, table=True):
    __tablename__ = "building_bill_materials_slim_record"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Project
    project_id: int = Field(foreign_key="project_record.id", nullable=False)
    project: ProjectRecord | None = Relationship(back_populates="bill_of_materials")
