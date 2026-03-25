from typing import Any


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
    reference_formats: dict[str, Any] | None = None,
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
            "reference_formats": reference_formats or {},
            "example": example,
        }
    }
