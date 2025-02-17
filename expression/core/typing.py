from __future__ import annotations

from abc import abstractmethod
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_origin,
)

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

_Base = TypeVar("_Base")
_Derived = TypeVar("_Derived")


class SupportsLessThan(Protocol):
    @abstractmethod
    def __lt__(self, __other: Any) -> bool:
        raise NotImplementedError


class SupportsSum(Protocol):
    @abstractmethod
    def __radd__(self, __other: Any) -> Any:
        raise NotImplementedError

    def __add__(self, __other: Any) -> Any:
        raise NotImplementedError


class SupportsGreaterThan(Protocol):
    @abstractmethod
    def __gt__(self, __other: Any) -> bool:
        raise NotImplementedError


class SupportsMatch(Protocol[_T_co]):
    """Pattern matching protocol."""

    @abstractmethod
    def __match__(self, pattern: Any) -> Iterable[_T_co]:
        """Match pattern with value.

        Return a singleton iterable item (e.g `[ value ]`) if pattern
        matches value, else an empty iterable (e.g. `[]`)."""

        raise NotImplementedError


class ModelField:
    """Type mock to avoid taking a hard dependency on pydantic."""

    sub_fields: List[ModelField]

    def validate(self, value: Any, values: Dict[str, str], loc: str) -> Tuple[Any, Any]:
        ...


Validator = Callable[[Any], _T]
GenericValidator = Callable[[Any, ModelField], _T]


class SupportsValidation(Protocol[_T_co]):
    """A type that implements __get_validators__ to be used with
    pydantic."""

    @classmethod
    def __get_validators__(
        cls,
    ) -> Iterator[Union[Validator[_T_co], GenericValidator[_T_co]]]:
        """Yield an iterator of validators."""
        ...


def upcast(type: Type[_Base], expr: _Base) -> _Base:
    """Upcast expression from a `Derived` to `Base`.

    Note: F# `:>` or `upcast`.
    """
    return expr


def downcast(type: Type[_Derived], expr: Any) -> _Derived:
    """Downcast expression `Derived` to `Base`

    Checks at compile time that the type of expression Base is a
    supertype of Derived, and checks at runtime that Base is in fact an
    instance of Derived.

    Note: F# `:?>` or `downcast`.
    """
    assert isinstance(
        expr, type
    ), f"The type of expression {expr} is not a supertype of {type}"
    return cast(_Derived, expr)


def try_downcast(type_: Type[_Derived], expr: Any) -> Optional[_Derived]:
    """Downcast expression `Base` to `Derived`.

    Check that the `Derived` type is a supertype of `Base`.

    NOTE: Supports generic types.

    Returns:
        None if `Derived` is not a supertype of `Base`.
    """
    origin: Optional[Type[_Derived]] = get_origin(type_) or type_
    if origin is not None and isinstance(expr, origin):
        derived = cast(_Derived, expr)
        return derived

    return None


__all__ = [
    "downcast",
    "upcast",
    "try_downcast",
    "GenericValidator",
    "SupportsLessThan",
    "SupportsSum",
    "SupportsGreaterThan",
    "SupportsValidation",
    "SupportsMatch",
    "Validator",
    "GenericValidator",
]
