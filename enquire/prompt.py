from typing import List, Dict, Any, Optional
from prompt_toolkit.styles import Style

from .question.base import BaseQuestion
from .style import DEFAULT_STYLE


def prompt(questions: List[BaseQuestion], style: Optional[Style] = None) -> Dict[str, Any]:
    if style is None:
        style = DEFAULT_STYLE

    answers = {}

    for question in questions:
        question.set_style(style)
        if question.when and not question.when(answers):
            continue
        answer = question.ask(answers)
        answers[question.name] = answer

    return answers
