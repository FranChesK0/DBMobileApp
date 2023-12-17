import asyncio
from typing import TypeVar
from abc import ABC, abstractmethod

import flet as ft

from app import Routes, Settings
from app.elements.buttons import AuthorizationButton

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
        self.animation_running: bool = False

        self.image: ft.Icon = ft.Icon(
            name=icon,
            color=Settings.ACCENT_COLOR,
            scale=ft.Scale(4),
            animate_scale=ft.Animation(900, ft.AnimationCurve.DECELERATE)
        )
        self.login_field: ft.TextField = ft.TextField(
            color=Settings.ACCENT_COLOR,
            border_color=Settings.ACCENT_COLOR,
            cursor_color=Settings.ACCENT_COLOR,
            on_focus=self.start_animation,
            on_blur=self.stop_animation
        )
        self.password_field: ft.TextField = ft.TextField(
            color=Settings.ACCENT_COLOR,
            border_color=Settings.ACCENT_COLOR,
            cursor_color=Settings.ACCENT_COLOR,
            on_focus=self.start_animation,
            on_blur=self.stop_animation,
            password=True
        )
        self.controls = [
            ft.SafeArea(
                minimum=5,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.IconButton(
                                        scale=0.85,
                                        icon=ft.icons.REFRESH_ROUNDED,
                                        icon_color=Settings.ACCENT_COLOR,
                                        on_click=self.clear_fields
                                    )
                                ]
                            )
                        ),
                        ft.Divider(color="transparent"),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, height=200, controls=[self.image]),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                intro,
                                                size=16,
                                                color=Settings.ACCENT_COLOR,
                                                weight=ft.FontWeight.BOLD
                                            )
                                        ]
                                    ),
                                    ft.Divider(height=40, color="transparent"),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Column(
                                                spacing=10,
                                                controls=[
                                                    ft.Text("Логин", color=Settings.ACCENT_COLOR),
                                                    self.login_field
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Column(
                                                spacing=10,
                                                controls=[
                                                    ft.Text("Пароль", color=Settings.ACCENT_COLOR),
                                                    self.password_field
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        controls=[
                                            AuthorizationButton(text="Продолжить", on_click=self.routing)
                                        ]
                                    )
                                ]
                            )
                        ),
                        ft.Divider(color="transparent"),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        footer,
                                        color=Settings.ACCENT_COLOR,
                                        spans=[
                                            ft.TextSpan(
                                                " здесь.",
                                                style=ft.TextStyle(
                                                    italic=True,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=Settings.ACCENT_COLOR
                                                ),
                                                on_click=self.footer_routing
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]

    @abstractmethod
    async def routing(self, e: ft.ControlEvent) -> None:
        raise NotImplementedError

    async def footer_routing(self, e: ft.ControlEvent) -> None:
        await self.page.go_async(self.footer_route_to.value)

    async def clear_fields(self, e: ft.ControlEvent) -> None:
        self.login_field.value = ""
        self.password_field.value = ""
        await self.page.update_async()

    async def start_animation(self, e: ft.ControlEvent) -> None:
        self.animation_running = True
        await self.run_animation()

    async def stop_animation(self, e: ft.ControlEvent) -> None:
        self.animation_running = False
        await self.run_animation()

    async def run_animation(self) -> None:
        if self.animation_running:
            self.image.scale = ft.transform.Scale(4.9)
            await self.image.update_async()
            await asyncio.sleep(0.9)

            self.image.scale = ft.transform.Scale(4)
            await self.image.update_async()
            await asyncio.sleep(0.9)

            await self.run_animation()
        else:
            self.image.scale = ft.transform.Scale(4)
            await self.image.update_async()
