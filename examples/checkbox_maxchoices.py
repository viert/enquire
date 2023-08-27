#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.base import Choice
from enquire.question.checkbox import Checkbox


if __name__ == "__main__":
    questions = [
        Checkbox("instruments", "Your favourite instruments", choices=[
            Choice("1", checked=True),
            Choice("2"),
            Choice("3"),
            Choice("4"),
            Choice("5"),
            Choice("6"),
            Choice("7"),
            Choice("8"),
        ], max_choices_visible=5, wrap=False)
    ]

    answers = prompt(questions)
    print(answers)
