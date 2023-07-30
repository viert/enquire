#!/usr/bin/env python
from enquire.prompt import prompt
from enquire.question.text import Text


if __name__ == "__main__":
    questions = [
        Text("name", "Machine name", default="q35"),
    ]

    answers = prompt(questions)
    print(answers)
