from __future__ import annotations

from copy import copy
from typing import Any, Optional

from pydantic import create_model
from sqlmodel import SQLModel


def make_draft_model(
    model_cls: type[SQLModel],
    *,
    base: type[SQLModel] = SQLModel,
    name: str | None = None,
) -> type[SQLModel]:
    field_definitions: dict[str, Any] = {}

    for field_name, field_info in model_cls.model_fields.items():
        field_info = copy(field_info)

        # Make the field not required
        field_info.default = None
        field_info.default_factory = None

        # Keep the original type, but allow omission / None in the draft model
        field_definitions[field_name] = (
            Optional[field_info.annotation],
            field_info,
        )

    return create_model(
        name or f"{model_cls.__name__}Draft",
        __base__=base,
        __module__=model_cls.__module__,
        **field_definitions,
    )
