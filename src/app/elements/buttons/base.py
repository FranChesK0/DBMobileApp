from abc import ABC
from typing import TypeVar, Callable

import flet as ft

from app import Settings

ElevatedButtonType = TypeVar("ElevatedButtonType", bound="BaseElevatedButton")
PopupMenuButtonType = TypeVar("PopupMenuButtonType", bound="BasePopupMenuButton")


class BaseElevatedButton(ABC, ft.ElevatedButton):
    def __init__(self, text: str, on_click: Callable):
        super().__init__(text=text,
                         bgcolor=Settings.SECONDARY_COLOR,
                         color=Settings.ACCENT_COLOR,
                         icon_color=Settings.ACCENT_COLOR,
                         on_click=on_click)


class BasePopupMenuButton(ABC, ft.PopupMenuButton):
    def __init__(self, std_value: str, items: list[ft.PopupMenuItem]):
        super().__init__(
            content=ft.Text(std_value, size=20, weight=ft.FontWeight.BOLD, color=Settings.ACCENT_COLOR),
            items=items
        )
