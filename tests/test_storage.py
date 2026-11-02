"""Storage holds drafts too: requirement is validation's business, not the schema's."""

import pytest
from pydantic import ValidationError

from openbdf.model import tables
from openbdf.model.general_info import ProjectRecordBase

TABLES = (
    tables.ProjectRecord,
    tables.BuildingBillMaterialsSlimRecord,
    tables.ProjectMaterialDatabaseRecord,
    tables.LCAResultsWideFullRecord,
    tables.LCAResultsTallFullRecord,
)


@pytest.mark.parametrize("table", TABLES, ids=lambda t: t.__tablename__)
def test_only_the_keys_that_link_rows_are_not_null(table):
    not_null = {c.name for c in table.__table__.columns if not c.nullable}
    keys = {c.name for c in table.__table__.columns if c.primary_key or c.foreign_keys}
    assert not_null == keys


def test_a_draft_without_a_required_field_can_be_stored():
    # project_country is Requirement.REQUIRED: a draft may still lack it.
    assert tables.ProjectRecord(project_name="Draft").project_country is None


def test_the_strict_model_still_requires_it():
    with pytest.raises(ValidationError, match="project_country"):
        ProjectRecordBase.model_validate({"project_name": "Complete"})
