from __future__ import annotations

from typing import Union

import flet as ft

from app_model import Application


class flet_model_main:
    """QMainWindow with app-model support."""

    def __init__(self, app: Union[str, Application]) -> None:
        self.app = Application.get_or_create(app) if isinstance(app, str) else app

    def init_page(self, page: ft.Page) -> None:
        page.appbar = self.appbar(page)

    def appbar(self, page: ft.Page) -> ft.AppBar:
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        return ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item",
                            checked=False,
                            on_click=check_item_clicked,
                        ),
                    ]
                ),
            ],
        )
