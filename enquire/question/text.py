from typing import Any, Dict
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import SimpleLexer
from .base import Question, QuestionType


class Text(Question):

    type = QuestionType.TEXT

    def _interact(self, answers: Dict[str, Any]) -> Any:
        tokens = [
            ("class:qmark", "?"),
            ("class:question", f" {self.message}  "),
        ]

        kwargs = {}
        if self.default:
            kwargs["default"] = self.default

        answer = prompt(message=tokens, style=self._style, lexer=SimpleLexer("class:answer"), **kwargs)
        return answer
