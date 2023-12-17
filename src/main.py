import flet as ft

from app import Routes, views


async def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT

    theme = ft.Theme()
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    page.theme = theme

    async def change_route(route):
        page.views.clear()
        ...
        await page.update_async()

    page.views.append(views.authorization_views.LoginView(page))
    page.on_route_change = change_route

    await page.update_async()


if __name__ == "__main__":
    ft.app(target=main)
