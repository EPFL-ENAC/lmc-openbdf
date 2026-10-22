from .openbdf_enum import OpenBDFEnum


class Requirement(OpenBDFEnum):
    """
    Obligation level of one OpenBDF field, merging the former Requirements and
    Criticality metadata into a single ladder.
    """

    REQUIRED = (
        "required",
        "Required",
        "MUST. The field must be provided.",
    )
    STRONGLY_RECOMMENDED = (
        "strongly_recommended",
        "Strongly recommended",
        "SHOULD. The field should be provided. A missing value needs justification.",
    )
    RECOMMENDED = (
        "recommended",
        "Recommended",
        "SHOULD, at a lower grade. Missing values reduce data quality.",
    )
    SUGGESTED = (
        "suggested",
        "Suggested",
        "MAY. Provide the field when available.",
    )
    OPTIONAL = (
        "optional",
        "Optional",
        "MAY. Filling the field has no effect on compliance.",
    )
    AUTOMATIC = (
        "automatic",
        "Automatic",
        "Computed by the tool. Do not enter the value manually.",
    )
