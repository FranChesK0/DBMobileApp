from typing import TypeVar
from abc import ABC, abstractmethod

import flet as ft

from app.routes import Routes
from app.settings import Settings

AuthorizationViewType = TypeVar("AuthorizationViewType", bound="BaseAuthorizationView")


class BaseAuthorizationView(ABC, ft.View):
    def __init__(self,
                 page: ft.Page,
                 route: Routes,
                 icon: str,
                 intro: str,
                 footer: str,
                 footer_route_to: Routes):
        super().__init__(bgcolor=Settings.MAIN_COLOR)
        self.page: ft.Page = page
        self.route: Routes = route
        self.footer_route_to: Routes = footer_route_to

    @abstractmethod
    async def routing(self, e: ft.ControlEvent):
        raise NotImplementedError

    async def footer_routing_to(self, e: ft.ControlEvent):
        self.page.go_async(self.footer_route_to)
