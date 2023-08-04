from typing import Any, Dict
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.validation import Validator
from .base import Question, QuestionType


class Text(Question):

    type = QuestionType.TEXT

    def _interact(self, answers: Dict[str, Any]) -> Any:
        tokens = [
            ("class:qmark", "?"),
            ("class:question", f" {self.message} "),
        ]

        kwargs = {}
        if self.default:
            kwargs["default"] = str(self.default)

        if self.validate:
            kwargs["validator"] = Validator.from_callable(lambda v: self.validate(v, answers))

        answer = prompt(message=tokens, style=self._style, lexer=SimpleLexer("class:answer"), **kwargs)
        return answer
