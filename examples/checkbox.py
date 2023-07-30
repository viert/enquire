#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.base import Choice, Separator
from enquire.question.checkbox import Checkbox


if __name__ == "__main__":
    questions = [
        Checkbox("instruments", "Your favourite instruments", choices=[
            Choice("guitar", checked=True),
            Choice("bass"),
            Choice("drums"),
            Choice("keyboards"),
        ])
    ]

    answers = prompt(questions)
    print(answers)
