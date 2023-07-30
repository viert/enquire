from typing import Optional, List, Callable, Dict, Any, TypeVar
from abc import ABC
from enum import Enum, auto
from prompt_toolkit.styles import Style

# Validator accepts the current answers dict and the current raw answer given
# and must return True if validation has passed and False otherwise
Validator = TypeVar("Validator", bound=Callable[[Dict[str, Any], Any], bool])

# Converter accepts the current answers dict and the current raw answer given
# and must return a converted value that will later be passed to the answers dict
Converter = TypeVar("Converter", bound=Callable[[Dict[str, Any], Any], Any])

# WhenFilter accepts the current answers dict and must return True if the current
# question should be asked or False otherwise
WhenFilter = TypeVar("WhenFilter", bound=Callable[[Dict[str, Any]], bool])


class Choice:

    name: str
    value: Any
    active: bool

    def __init__(self, name: str, value: Optional[Any] = None, active: bool = True):
        self.name = name
        self.value = value if value is not None else name
        self.active = active


class Separator(Choice):

    def __init__(self, value: Optional[str] = None):
        if value is None:
            value = "-" * 15
        super().__init__(value, "__separator__", active=False)


class QuestionType(Enum):

    TEXT = auto()
    LIST = auto()


class Question(ABC):

    type: QuestionType
    name: str
    message: str
    default: Optional[Any] = None
    validate: Optional[Validator] = None
    convert: Optional[Converter] = None
    when: Optional[Callable[[Dict[str, Any]], bool]] = None
    _style: Optional[Style] = None

    def __init__(self,
                 name: str,
                 message: str,
                 *,
                 default: Optional[Any] = None,
                 validate: Optional[Callable[[List[Any]], bool]] = None,
                 convert: Optional[Callable[[Any], Any]] = None,
                 when: Optional[Callable[[Dict[str, Any]], bool]] = None) -> None:
        self.name = name
        self.message = message
        self.default = default
        self.validate = validate
        self.convert = convert
        self.when = when

    def set_style(self, style: Style):
        self._style = style

    def ask(self, answers: Dict[str, Any]) -> Any:
        while True:
            raw_answer = self._interact(answers)
            if not self.validate or self.validate(answers, raw_answer):
                break
        answer = self.convert(answers, raw_answer) if self.convert else raw_answer
        return answer

    def _interact(self, answers: Dict[str, Any]) -> Any: ...


BaseQuestion = TypeVar("BaseQuestion", bound=Question)
