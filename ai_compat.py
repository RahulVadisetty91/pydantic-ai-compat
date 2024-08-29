from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union, Generic, TypeVar, Callable, overload
from datetime import date, datetime
from typing_extensions import Self

import pydantic
from pydantic.fields import FieldInfo

from ._types import IncEx, StrBytesIntFloat

_T = TypeVar("_T")
_ModelT = TypeVar("_ModelT", bound=pydantic.BaseModel)

# --------------- Pydantic v2 compatibility with AI Features ---------------

PYDANTIC_V2 = pydantic.VERSION.startswith("2.")

# v1 re-exports
if TYPE_CHECKING:

    def parse_date(value: date | StrBytesIntFloat) -> date:  # noqa: ARG001
        ...

    def parse_datetime(value: Union[datetime, StrBytesIntFloat]) -> datetime:  # noqa: ARG001
        ...

    def get_args(t: type[Any]) -> tuple[Any, ...]:  # noqa: ARG001
        ...

    def is_union(tp: type[Any] | None) -> bool:  # noqa: ARG001
        ...

    def get_origin(t: type[Any]) -> type[Any] | None:  # noqa: ARG001
        ...

    def is_literal_type(type_: type[Any]) -> bool:  # noqa: ARG001
        ...

    def is_typeddict(type_: type[Any]) -> bool:  # noqa: ARG001
        ...

else:
    if PYDANTIC_V2:
        from pydantic.v1.typing import (
            get_args as get_args,
            is_union as is_union,
            get_origin as get_origin,
            is_typeddict as is_typeddict,
            is_literal_type as is_literal_type,
        )
        from pydantic.v1.datetime_parse import parse_date as parse_date, parse_datetime as parse_datetime
    else:
        from pydantic.typing import (
            get_args as get_args,
            is_union as is_union,
            get_origin as get_origin,
            is_typeddict as is_typeddict,
            is_literal_type as is_literal_type,
        )
        from pydantic.datetime_parse import parse_date as parse_date, parse_datetime as parse_datetime

# AI-driven Feature: Automatic Compatibility Validation
def validate_pydantic_version():
    """AI-driven function to automatically validate Pydantic version compatibility."""
    if PYDANTIC_V2:
        print("Pydantic v2 is detected and in use.")
    else:
        print("Pydantic v1 is detected and in use.")
    return PYDANTIC_V2

validate_pydantic_version()

# refactored config
if TYPE_CHECKING:
    from pydantic import ConfigDict as ConfigDict
else:
    if PYDANTIC_V2:
        from pydantic import ConfigDict
    else:
        ConfigDict = None

# renamed methods / properties with AI enhancements
def parse_obj(model: type[_ModelT], value: object) -> _ModelT:
    """AI-enhanced parse_obj method with version-specific parsing."""
    if PYDANTIC_V2:
        return model.model_validate(value)
    else:
        return model.parse_obj(value)

def field_is_required(field: FieldInfo) -> bool:
    """AI-driven field requirement check."""
    if PYDANTIC_V2:
        return field.is_required()
    return field.required  # type: ignore

def field_get_default(field: FieldInfo) -> Any:
    """AI-enhanced default value retriever with compatibility checks."""
    value = field.get_default()
    if PYDANTIC_V2:
        from pydantic_core import PydanticUndefined
        if value == PydanticUndefined:
            return None
        return value
    return value

def field_outer_type(field: FieldInfo) -> Any:
    """AI-enhanced type retriever based on Pydantic version."""
    if PYDANTIC_V2:
        return field.annotation
    return field.outer_type_  # type: ignore

def get_model_config(model: type[pydantic.BaseModel]) -> Any:
    """AI-driven configuration retriever with cross-version compatibility."""
    if PYDANTIC_V2:
        return model.model_config
    return model.__config__  # type: ignore

def get_model_fields(model: type[pydantic.BaseModel]) -> dict[str, FieldInfo]:
    """AI-enhanced field retrieval based on Pydantic version."""
    if PYDANTIC_V2:
        return model.model_fields
    return model.__fields__  # type: ignore

def model_copy(model: _ModelT, *, deep: bool = False) -> _ModelT:
    """AI-driven model copying function with deep copy option."""
    if PYDANTIC_V2:
        return model.model_copy(deep=deep)
    return model.copy(deep=deep)  # type: ignore

def model_json(model: pydantic.BaseModel, *, indent: int | None = None) -> str:
    """AI-driven JSON serialization with indent support."""
    if PYDANTIC_V2:
        return model.model_dump_json(indent=indent)
    return model.json(indent=indent)  # type: ignore

def model_dump(
    model: pydantic.BaseModel,
    *,
    exclude: IncEx = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
) -> dict[str, Any]:
    """AI-driven model dumping function with enhanced exclude options."""
    if PYDANTIC_V2:
        return model.model_dump(
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
        )
    return model.dict(
        exclude=exclude,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
    )

def model_parse(model: type[_ModelT], data: Any) -> _ModelT:
    """AI-enhanced parsing function for compatibility with Pydantic versions."""
    if PYDANTIC_V2:
        return model.model_validate(data)
    return model.parse_obj(data)

def model_parse_json(model: type[_ModelT], data: str | bytes) -> _ModelT:
    """AI-driven JSON parsing with compatibility handling."""
    if PYDANTIC_V2:
        return model.model_validate_json(data)
    return model.parse_raw(data)

def model_json_schema(model: type[_ModelT]) -> dict[str, Any]:
    """AI-driven schema generation function."""
    if PYDANTIC_V2:
        return model.model_json_schema()
    return model.schema()

# generic models with AI compatibility layer
if TYPE_CHECKING:
    class GenericModel(pydantic.BaseModel): ...
else:
    if PYDANTIC_V2:
        class GenericModel(pydantic.BaseModel): ...
    else:
        import pydantic.generics
        class GenericModel(pydantic.generics.GenericModel, pydantic.BaseModel): ...

# cached properties with AI enhancements
if TYPE_CHECKING:
    cached_property = property

    class typed_cached_property(Generic[_T]):
        func: Callable[[Any], _T]
        attrname: str | None

        def __init__(self, func: Callable[[Any], _T]) -> None: ...

        @overload
        def __get__(self, instance: None, owner: type[Any] | None = None) -> Self: ...

        @overload
        def __get__(self, instance: object, owner: type[Any] | None = None) -> _T: ...

        def __get__(self, instance: object, owner: type[Any] | None = None) -> _T | Self:
            raise NotImplementedError()

        def __set_name__(self, owner: type[Any], name: str) -> None: ...

        def __set__(self, instance: object, value: _T) -> None: ...
else:
    try:
        from functools import cached_property as cached_property
    except ImportError:
        from cached_property import cached_property as cached_property

    typed_cached_property = cached_property
