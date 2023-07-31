#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.text import Text
from enquire.validation import is_number


if __name__ == "__main__":
    questions = [
        Text("price", "Enter price", default="24", validate=is_number, convert=lambda x, _: float(x)),
    ]

    answers = prompt(questions)
    print(answers)
