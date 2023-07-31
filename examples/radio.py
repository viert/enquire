#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.base import Choice, Separator
from enquire.question.radio import Radio
from enquire.question.boolean import Boolean


if __name__ == "__main__":
    questions = [
        Radio("cpu_profile", "Pick RAM size:", choices=[
            Choice("4Gb", 4),
            Choice("8Gb", 8),
            Choice("16Gb", 16),
            Choice("32Gb", 32),
            Choice("64Gb", 64),
            Separator(),
            Choice("Custom", "custom")
        ], default=2),
        Boolean("confirm", "Are you sure?")
    ]

    answers = prompt(questions)
    print(answers)
