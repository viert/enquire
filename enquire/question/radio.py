from typing import Optional, Any, Dict, List, Tuple
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from .base import Question, Choice, WhenFilter, Converter, ValidationFunc, ARROW_UP, ARROW_DOWN
from .wrappable import Wrappable


class Control(Wrappable):

    prompt: str
    checked_char: str = "\u25c9"
    unchecked_char: str = "\u25ef"

    def __init__(self,
                 prompt: str,
                 choices: List[Choice],
                 active_idx: int,
                 *,
                 checked_char: Optional[str] = None,
                 unchecked_char: Optional[str] = None,
                 max_choices_visible: int = 10,
                 wrap: bool = True):
        super().__init__(
            choices=choices,
            active_idx=active_idx,
            max_choices_visible=max_choices_visible,
            wrap=wrap,
            text=self._get_tokens,
            show_cursor=False,
        )
        self.prompt = prompt

        if checked_char is not None:
            self.checked_char = checked_char
        if unchecked_char is not None:
            self.unchecked_char = unchecked_char

    @property
    def _separator_tokens(self) -> Tuple[str, str]:
        prompt_len = len(self.prompt) + 8
        return "class:separator", "-" * prompt_len

    def _get_prompt(self) -> List[Tuple[str, str]]:
        tokens = [
            ("class:qmark", "?"),
            ("class:question", f" {self.prompt}  "),
            ("class:answer", self.selected.name),
            ("", "\n"),
            self._separator_tokens,
            ("", "\n"),
        ]
        return tokens

    def _get_tokens(self) -> List[Tuple[str, str]]:
        tokens = self._get_prompt()

        choices = self.choices[self.start:self.end]

        for idx, choice in enumerate(choices):
            idx = self.start + idx
            selected = idx == self.idx

            arrow = " "
            if 0 < self.start == idx:
                arrow = ARROW_UP
            elif self.end < len(self.choices) and idx == self.end - 1:
                arrow = ARROW_DOWN

            if hasattr(choice, "render"):
                tokens.extend(choice.render())
            elif selected:
                tokens.append(("class:checkbox-selected", f"{arrow} {self.checked_char} "))
                tokens.append(("class:choice-selected", choice.name))
            elif choice.active:
                tokens.append(("class:checkbox-unselected", f"{arrow} {self.unchecked_char} "))
                tokens.append(("class:choice-unselected", choice.name))
            else:
                tokens.append(("", "   ")),
                tokens.append(("class:choice-unselected", choice.name))
            tokens.append(("", "\n"))
        return tokens


class Radio(Question):

    ctrl: Control
    _max_height: int

    def __init__(self,
                 name: str,
                 message: str,
                 *,
                 choices: List[Choice | str],
                 default: Optional[int] = None,
                 validate: Optional[ValidationFunc] = None,
                 convert: Optional[Converter] = None,
                 when: Optional[WhenFilter] = None,
                 checked_char: Optional[str] = None,
                 unchecked_char: Optional[str] = None,
                 max_choices_visible: int = 10,
                 wrap: bool = True):
        if validate is not None:
            raise NotImplementedError("validate functions are not implemented for Radio yet")
        if len(choices) > max_choices_visible:
            self._max_height = max_choices_visible + 3
        else:
            self._max_height = len(choices) + 2
        super().__init__(
            name,
            message,
            validate=validate,
            convert=convert,
            when=when,
        )

        act_choices = []
        first_active = None

        for idx, choice in enumerate(choices):

            if isinstance(choice, str):
                choice = Choice(choice)

            act_choices.append(choice)

            if first_active is None and choice.active:
                first_active = idx

        if first_active is None:
            raise ValueError("no active choices found")

        if default is not None:
            # raise IndexError in case default is out of bounds
            _ = act_choices[default]
            act_idx = default
        else:
            act_idx = first_active

        self.ctrl = Control(
            message,
            act_choices,
            act_idx,
            checked_char=checked_char,
            unchecked_char=unchecked_char,
            max_choices_visible=max_choices_visible,
            wrap=wrap,
        )

    def _interact(self, answers: Dict[str, Any]) -> Any:
        layout = Layout(HSplit([Window(content=self.ctrl, height=self._max_height)]))
        kb = KeyBindings()

        @kb.add("down", eager=True)
        def cursor_down(_):
            self.ctrl.move_cursor_down()

        @kb.add("up", eager=True)
        def cursor_up(_):
            self.ctrl.move_cursor_up()

        @kb.add("c-c", eager=True)
        def _exit(event: KeyPressEvent):
            event.app.exit()
            raise KeyboardInterrupt()

        @kb.add("enter", eager=True)
        def _pick(event: KeyPressEvent):
            event.app.exit()

        app = Application(layout=layout, key_bindings=kb, style=self._style)
        app.run()
        return self.ctrl.selected.value
