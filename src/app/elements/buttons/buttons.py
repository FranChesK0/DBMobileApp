from typing import Callable

import flet as ft

from app.elements.buttons import BaseElevatedButton, BasePopupMenuButton
from database.schemas import SectionDTO


class AuthorizationButton(BaseElevatedButton):
    def __init__(self, text: str, on_click: Callable):
        super().__init__(text, on_click)


class SelectSectionButton(BasePopupMenuButton):
    def __init__(self, std_value: str, on_click: Callable, sections: list[SectionDTO]):
        items = ([ft.PopupMenuItem(text="все", on_click=on_click), ft.PopupMenuItem()] +
                 [ft.PopupMenuItem(text=str(section.id)) for section in sections])
        super().__init__(std_value=std_value, items=items)
