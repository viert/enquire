from typing import Dict, Any, TypeVar, Callable
from re import Pattern


ValidationFunc = TypeVar("ValidationFunc", bound=Callable[[Any, Dict[str, Any]], bool])


def is_int(current: Any, _: Dict[str, Any]) -> bool:
    try:
        _ = int(current)
    except ValueError:
        return False
    return True


def is_number(current: Any, _: Dict[str, Any]) -> bool:
    try:
        _ = float(current)
    except ValueError:
        return False
    return True


def is_match(pattern: Pattern) -> ValidationFunc:
    return lambda c, _: pattern.search(c) is not None


def is_fullmatch(pattern: Pattern) -> ValidationFunc:
    return lambda c, _: pattern.fullmatch(c) is not None


def is_not_empty(current: str, _: Dict[str, Any]) -> bool:
    return current != ""
