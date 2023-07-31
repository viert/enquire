from typing import Optional, List, Callable, Dict, Any, TypeVar, Tuple
from abc import ABC
from enum import Enum, auto
from prompt_toolkit.styles import Style
from enquire.validation import ValidationFunc

# Converter accepts the current answers dict and the current raw answer given
# and must return a converted value that will later be passed to the answers dict
Converter = TypeVar("Converter", bound=Callable[[Any, Dict[str, Any]], Any])

# WhenFilter accepts the current answers dict and must return True if the current
# question should be asked or False otherwise
WhenFilter = TypeVar("WhenFilter", bound=Callable[[Dict[str, Any]], bool])


class Choice:

    name: str
    value: Any
    active: bool
    checked: bool

    def __init__(self, name: str, value: Optional[Any] = None, active: bool = True, checked: bool = False):
        self.name = name
        self.value = value if value is not None else name
        self.active = active
        self.checked = checked


class Separator(Choice):

    def __init__(self, value: Optional[str] = None):
        if value is None:
            value = "-" * 15
        super().__init__(value, value, active=False)

    def render(self) -> List[Tuple[str, str]]:
        return [("class:separator", self.value)]


class QuestionType(Enum):

    TEXT = auto()
    LIST = auto()


class Question(ABC):

    type: QuestionType
    name: str
    message: str
    default: Optional[Any] = None
    validate: Optional[ValidationFunc] = None
    convert: Optional[Converter] = None
    when: Optional[WhenFilter] = None
    _style: Optional[Style] = None

    def __init__(self,
                 name: str,
                 message: str,
                 *,
                 default: Optional[Any] = None,
                 validate: Optional[ValidationFunc] = None,
                 convert: Optional[Converter] = None,
                 when: Optional[WhenFilter] = None) -> None:
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
            if not self.validate or self.validate(raw_answer, answers):
                break
        return self._apply_convertor(raw_answer, answers)

    def _apply_convertor(self, raw_answer: Any, answers: Dict[str, Any]) -> Any:
        return self.convert(raw_answer, answers) if self.convert else raw_answer

    def _interact(self, answers: Dict[str, Any]) -> Any: ...


BaseQuestion = TypeVar("BaseQuestion", bound=Question)
