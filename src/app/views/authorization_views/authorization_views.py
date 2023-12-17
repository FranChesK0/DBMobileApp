import flet as ft

from app import Routes
from app.views.authorization_views import BaseAuthorizationView


class LoginView(BaseAuthorizationView):
    def __init__(self, page: ft.Page):
        super().__init__(page=page,
                         route=Routes.LOGIN,
                         icon=ft.icons.PERSON_2_ROUNDED,
                         intro="Авторизация",
                         footer="Нет аккаунта? Зарегистрируйтесь",
                         footer_route_to=Routes.REGISTER)

    async def routing(self, e: ft.ControlEvent):
        pass


class RegisterView(BaseAuthorizationView):
    def __init__(self, page: ft.Page):
        super().__init__(page=page,
                         route=Routes.REGISTER,
                         icon=ft.icons.LOCK_ROUNDED,
                         intro="Регистрация",
                         footer="Уже есть аккаунт? Войдите",
                         footer_route_to=Routes.LOGIN)

    async def routing(self, e: ft.ControlEvent):
        pass
