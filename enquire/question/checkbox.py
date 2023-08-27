from typing import Optional, Any, Dict, List, Tuple
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from .wrappable import Wrappable

from .base import Question, Choice, WhenFilter, Converter, ValidationFunc, ARROW_DOWN, ARROW_UP


class Control(Wrappable):

    prompt: str
    checked_char: str = "\u2611"
    unchecked_char: str = "\u2610"

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

            token_class = "selected" if selected else "unselected"
            char = self.checked_char if choice.checked else self.unchecked_char
            if hasattr(choice, "render"):
                tokens.extend(choice.render())
            elif choice.active:
                tokens.append((f"class:checkbox-{token_class}", f"{arrow} {char} "))
                tokens.append((f"class:choice-{token_class}", choice.name))
            else:
                tokens.append(("", f"{arrow}  ")),
                tokens.append(("class:choice-unselected", choice.name))
            tokens.append(("", "\n"))
        return tokens

    def toggle(self):
        self.choices[self.idx].checked = not self.choices[self.idx].checked

    @property
    def values(self) -> List[Any]:
        return [choice.value for choice in self.choices if choice.checked]


class Checkbox(Question):

    ctrl: Control
    convert_each: bool
    _max_height: int

    def __init__(self,
                 name: str,
                 message: str,
                 *,
                 choices: List[Choice | str],
                 validate: Optional[ValidationFunc] = None,
                 convert: Optional[Converter] = None,
                 convert_each: bool = True,
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

        self.convert_each = convert_each

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

        self.ctrl = Control(
            message,
            act_choices,
            first_active,
            checked_char=checked_char,
            unchecked_char=unchecked_char,
            wrap=wrap,
            max_choices_visible=max_choices_visible,
        )

    def _apply_convertor(self, raw_answer: List[Any], answers: Dict[str, Any]) -> Any:
        if not self.convert:
            return raw_answer
        if self.convert_each:
            return [self.convert(answer) for answer in raw_answer]
        else:
            return self.convert(raw_answer)

    def _interact(self, answers: Dict[str, Any]) -> List[Any]:
        layout = Layout(HSplit([Window(content=self.ctrl, height=self._max_height)]))
        kb = KeyBindings()

        @kb.add("down", eager=True)
        def cursor_down(_):
            self.ctrl.move_cursor_down()

        @kb.add("up", eager=True)
        def cursor_up(_):
            self.ctrl.move_cursor_up()

        @kb.add("space", eager=True)
        def toggle(_):
            self.ctrl.toggle()

        @kb.add("c-c", eager=True)
        def _exit(event: KeyPressEvent):
            event.app.exit()
            raise KeyboardInterrupt()

        @kb.add("enter", eager=True)
        def _pick(event: KeyPressEvent):
            event.app.exit()

        app = Application(layout=layout, key_bindings=kb, style=self._style)
        app.run()
        return self.ctrl.values
