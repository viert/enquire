from typing import Optional
from .radio import Radio, Choice, WhenFilter, ValidationFunc


class Boolean(Radio):

    def __init__(self,
                 name: str,
                 message: str,
                 *,
                 true: str = "yes",
                 false: str = "no",
                 default: bool = True,
                 when: Optional[WhenFilter] = None,
                 validate: Optional[ValidationFunc] = None,
                 checked_char: Optional[str] = None,
                 unchecked_char: Optional[str] = None):
        choices = [
            Choice(true, True),
            Choice(false, False),
        ]
        super().__init__(
            name,
            message,
            choices=choices,
            default=0 if default else 1,
            validate=validate,
            when=when,
            checked_char=checked_char,
            unchecked_char=unchecked_char
        )
