#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.radio import Radio


if __name__ == "__main__":
    choices = [f"{x}" for x in range(30)]
    questions = [
        Radio("number", "Pick a number:", choices=choices, max_choices_visible=10, default=18, wrap=False),
    ]

    answers = prompt(questions)
    print(answers)
