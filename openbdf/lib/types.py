from types import NoneType, UnionType
from typing import Any, Union, get_args, get_origin


def unwrap_optional(annotation: Any) -> tuple[Any, bool]:
    """
    Takes a type annotation and returns the annotation stripped from the Optional if needed and True/False if it was an optional
    This function checks if the annotation is of the form Optional[T] (i.e., Union[T, None]) and returns T and a boolean indicating optionality.
    """
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Union, UnionType) and NoneType in args:
        non_none_args = [arg for arg in args if arg is not NoneType]
        if len(non_none_args) == 1:
            return non_none_args[0], True
    return annotation, False


def get_display_type(type: Any) -> str:
    return getattr(type, "__name__", str(type))
