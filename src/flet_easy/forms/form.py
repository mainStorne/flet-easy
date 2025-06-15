from collections.abc import Awaitable
from typing import Callable

import flet as ft

from flet_easy.forms.fields import ButtonFieldsy, Fieldsy, FormFieldInvalidError


class Formsy:
    def __init__(
        self,
        valid_hook: Callable[[dict], Awaitable[dict]],
        fields: list[Fieldsy],
        btn_field: ButtonFieldsy,
    ):
        self._valid_hook = valid_hook
        self.fields = fields
        self.btn_field = btn_field
        self.btn_field.on_click = self._validate_form
        self.view = ft.Container(
            ft.Column([field.view for field in self.fields] + [self.btn_field])
        )

    async def _validate_form(self, e):
        context = {}
        try:
            for field in self.fields:
                field.validate()
                context[field.name] = field.value
        except FormFieldInvalidError:
            return
        finally:
            self.view.page.update()

        await self._valid_hook(context)
