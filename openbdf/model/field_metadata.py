from typing import Any

from openbdf.model.enums.references import Reference, ReferenceAlignment


def openbdf_field_metadata(
    *,
    group: str | None = None,
    sub_group: str | None = None,
    attribute_name: str,
    field_code: str,
    description: str,
    constraint: str | None = None,
    units: str | None = None,
    requirements: str | None = None,
    criticality: str = "SHOULD",
    reference: Reference | None = None,
    reference_alignment: ReferenceAlignment | None = None,
    example: str | None = None,
) -> dict[str, Any]:
    return {
        "json_schema_extra": {
            "group": group,
            "sub_group": sub_group,
            "attribute_name": attribute_name,
            "field_code": field_code,
            "description": description,
            "constraint": constraint,
            "units": units,
            "requirements": requirements,
            "criticality": criticality,
            "reference": reference.display_name if reference else None,
            "reference_alignment": reference_alignment.display_name if reference_alignment else None,
            "example": example,
        }
    }
