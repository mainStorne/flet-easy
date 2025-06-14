from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, TypeVar

import flet as ft


class FormFieldInvalidError(Exception): ...


class Fieldsy(ABC):
    def __init__(self, name: str, view, ref: ft.Ref, value=None, error_text: str = ""):
        self.name = name
        self.view = view
        self.value: None | Any = value
        self.error_text = error_text
        self.ref = ref

        super().__init__()

    @abstractmethod
    def validate(self): ...


class TextFieldsy:
    def validate(self):
        if not self.ref.current.value:
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""
            self.value = self.ref.current.value


@dataclass
class DropDownOption:
    text: str
    key: str


DropDownOptions = TypeVar("DropDownOptions", bound=list[DropDownOption])


class DropDownFieldsy(Fieldsy):
    def _handle_dropdown_click(self, e):
        self.value = int(e.control.value)

    def validate(self):
        if not self.value:
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""


class ButtonFieldsy(ft.Button):
    pass


class NumberFieldsy:
    def validate(self):
        if not isinstance(self.ref.current.value, int) and not self.ref.current.value.isdecimal():
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""
            self.value = int(self.ref.current.value)


class DecimalFieldsy:
    def validate(self):
        try:
            self.value = Decimal(self.ref.current.value)
        except:  # noqa: E722
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.value = ""
