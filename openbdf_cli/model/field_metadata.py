from typing import Any, Optional


def openbdf_field_metadata(
    *,
    group: Optional[str] = None,
    sub_group: Optional[str] = None,
    attribute_name: str,
    field_code: str,
    description: str,
    constraint: Optional[str] = None,
    units: Optional[str] = None,
    requirements: Optional[str] = None,
    reference_formats: Optional[dict[str, Any]] = None,
    example: Optional[str] = None,
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
