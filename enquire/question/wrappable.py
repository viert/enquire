from typing import List
from prompt_toolkit.layout.controls import FormattedTextControl
from .base import Choice


class Wrappable(FormattedTextControl):

    idx: int
    choices: List[Choice]
    max_choices_visible: int

    start: int
    end: int
    wrap: bool

    def __init__(self,
                 *,
                 choices: List[Choice],
                 active_idx: int,
                 max_choices_visible: int = 10,
                 wrap: bool = True,
                 **kwargs) -> None:
        self.choices = choices
        self.idx = active_idx
        self.max_choices_visible = max_choices_visible
        self.wrap = wrap
        super().__init__(**kwargs)

        if self.max_choices_visible >= len(choices):
            self.start = 0
            self.end = len(choices)
        else:
            self.start = max(0, active_idx - max_choices_visible + 1)
            self.end = self.start + max_choices_visible

    @property
    def selected(self) -> Choice:
        return self.choices[self.idx]

    def adjust_win(self):
        if self.idx < self.start:
            self.start = self.idx
            self.end = self.start + self.max_choices_visible
        elif self.idx >= self.end:
            self.end = self.idx + 1
            self.start = self.end - self.max_choices_visible

    def move_cursor_down(self) -> None:
        idx = self.idx
        while True:
            idx += 1
            if idx >= len(self.choices):
                if self.wrap:
                    idx = 0
                else:
                    idx -= 1
            if self.choices[idx].active:
                break
            if idx == self.idx:
                break
        self.idx = idx
        self.adjust_win()

    def move_cursor_up(self) -> None:
        idx = self.idx
        while True:
            idx -= 1
            if idx < 0:
                if self.wrap:
                    idx = len(self.choices) - 1
                else:
                    idx += 1
            if self.choices[idx].active:
                break
            if idx == self.idx:
                break
        self.idx = idx
        self.adjust_win()

