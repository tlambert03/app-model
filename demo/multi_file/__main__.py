import pathlib
import sys

from .app import MyApp

sys.path.append(str(pathlib.Path(__file__).parent.parent))

app = MyApp()

if "--flet" in sys.argv:
    import flet as ft

    from app_model.backends.flet import flet_model_main

    def main(page: ft.Page) -> None:
        flet_model_main(app).init_page(page)
        page.add(ft.Text("Body!"))

    ft.app(target=main)
else:
    from qtpy.QtWidgets import QApplication

    from app_model.backends.qt import QModelMainWindow

    qapp = QApplication.instance() or QApplication([])

    main_window = QModelMainWindow(app=app)
    # This will build a menu bar based on these menus
    main_window.setModelMenuBar([app.MenuId.FILE, app.MenuId.EDIT])

    main_window.show()
    qapp.exec_()
