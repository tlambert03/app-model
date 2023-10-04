from app_model import Application

from .actions import ACTIONS
from .constants import MenuId


class MyApp(Application):
    MenuId = MenuId

    def __init__(self) -> None:
        super().__init__("my_application")

        # ACTIONS is a list of Action objects.
        for action in ACTIONS:
            self.register_action(action)
