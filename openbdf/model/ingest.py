from __future__ import annotations

from copy import copy
from typing import Any, Optional, TypeVar, cast

from pydantic import create_model
from sqlmodel import SQLModel

ModelT = TypeVar("ModelT", bound=SQLModel)


def make_ingest_model(
    model_cls: type[ModelT],
    *,
    name: str | None = None,
) -> type[ModelT]:
    """
    Build a subclass of model_cls whose fields are all optional, so a record can be
    built from the values a contributor actually supplied.

    The field metadata is kept, because the converters read field_code from it. The
    constraints are dropped, because the strict model owns them and applies them
    when it validates the ingest record.
    """
    field_definitions: dict[str, Any] = {}

    for field_name, field_info in model_cls.model_fields.items():
        field_info = copy(field_info)
        field_info.default = None
        field_info.default_factory = None
        field_info.metadata = []
        field_definitions[field_name] = (Optional[field_info.annotation], field_info)

    return cast(
        type[ModelT],
        create_model(
            name or f"{model_cls.__name__}Ingest",
            __base__=model_cls,
            __module__=model_cls.__module__,
            **field_definitions,
        ),
    )
