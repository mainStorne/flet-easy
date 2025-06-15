from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable

import flet as ft


class FormFieldInvalidError(Exception): ...


RuleCallable = Callable[["Fieldsy"], Any]


class Fieldsy(ABC):
    def __init__(
        self,
        name: str,
        view,
        ref: ft.Ref,
        error_text: str = "",
        rules: list[RuleCallable] = [],
    ):
        self.name = name
        self.view = view
        self.error_text = error_text
        self.ref = ref
        self.rules = rules

        super().__init__()

    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def _validate_field(self):
        """Internal Fieldsy validation"""
        ...

    def __required__(self):
        if not self.value:
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""

    def validate(self):
        self._validate_field()
        for rule in self.rules:
            rule(self)


class BaseTypeFieldsy(Fieldsy):
    def __init__(self, name, view, ref, value=None, error_text="", rules=[]):
        self._value = value
        super().__init__(name, view, ref, error_text, rules)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class TextFieldsy(Fieldsy):
    def __init__(self, name, label: str, value=None, error_text="", rules=[], **kwargs):
        ref = ft.Ref[ft.TextField]()
        super().__init__(
            name,
            ft.TextField(
                label=ft.Text(label),
                value=value,
                color=ft.Colors.BLACK,
                ref=ref,
                **kwargs,
            ),
            ref,
            error_text,
            rules,
        )

    def _validate_field(self):
        pass

    @property
    def value(self):
        return self.ref.current.value


@dataclass
class DropDownOption:
    text: str
    key: str


class DropDownFieldsy(Fieldsy):
    def __init__(
        self,
        icon: ft.Icons,
        name: str,
        label: str,
        options: list[DropDownOption],
        value=None,
        error_text="",
    ):
        self._value = value
        ref = ft.Ref[ft.Dropdown]()

        super().__init__(
            name,
            view=ft.Dropdown(
                leading_icon=ft.Icon(icon, color=ft.Colors.BLACK),
                label_style=ft.TextStyle(color=ft.Colors.BLACK),
                text_style=ft.TextStyle(color=ft.Colors.BLACK),
                label_text=label,
                value=value,
                ref=ref,
                on_dropdown_change=self._handle_dropdown_click,
                expand=True,
                options=[
                    ft.DropdownOption(
                        key=option.key,
                        text=option.text,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.WHITE,
                            padding=0,
                            shape=ft.ContinuousRectangleBorder(),
                        ),
                        text_style=ft.TextStyle(color=ft.Colors.BLACK),
                        content=ft.Text(
                            value=option.text, text_align=ft.TextAlign.CENTER
                        ),
                    )
                    for option in options
                ],
            ),
            error_text=error_text,
            ref=ref,
        )

    def _handle_dropdown_click(self, e):
        self.value = int(e.control.value)

    def _validate_field(self):
        if not self.value:
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""


class ButtonFieldsy(ft.Button):
    pass


class NumberFieldsy(BaseTypeFieldsy):
    def __init__(self, name, label: str, value=None, error_text="", rules=[], **kwargs):
        ref = ft.Ref[ft.TextField]()
        super().__init__(
            name,
            ft.TextField(
                label=ft.Text(label),
                value=value,
                color=ft.Colors.BLACK,
                ref=ref,
                **kwargs,
            ),
            ref,
            value,
            error_text,
            rules,
        )

    def _validate_field(self):
        if not self.ref.current.value:
            return
        value = self.ref.current.value
        if not isinstance(value, int) and not value.isdecimal():
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.value = int(value)
            self.ref.current.error_text = ""


class DecimalFieldsy(BaseTypeFieldsy):
    def __init__(self, name, label: str, value=None, error_text="", rules=[], **kwargs):
        ref = ft.Ref[ft.TextField]()
        super().__init__(
            name,
            ft.TextField(
                label=ft.Text(label),
                value=value,
                color=ft.Colors.BLACK,
                ref=ref,
                **kwargs,
            ),
            ref,
            value,
            error_text,
            rules,
        )

    def _validate_field(self):
        if not self.ref.current.value:
            return
        try:
            self.value = Decimal(self.ref.current.value)
        except:  # noqa: E722
            self.ref.current.error_text = self.error_text
            raise FormFieldInvalidError
        else:
            self.ref.current.error_text = ""
