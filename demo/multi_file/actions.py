from typing import List

from fonticon_fa6 import FA6S

from app_model.types import Action, KeyBindingRule, KeyCode, KeyMod, MenuRule

from . import functions
from .constants import CommandId, MenuId

ACTIONS: List[Action] = [
    Action(
        id=CommandId.OPEN,
        title="Open",
        icon=FA6S.folder_open,
        callback=functions.open_file,
        menus=[MenuRule(id=MenuId.FILE)],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyO)],
    ),
    Action(
        id=CommandId.CLOSE,
        title="Close",
        icon=FA6S.rectangle_xmark,
        callback=functions.close,
        menus=[MenuRule(id=MenuId.FILE)],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyW)],
    ),
    Action(
        id=CommandId.UNDO,
        title="Undo",
        icon=FA6S.rotate_left,
        callback=functions.undo,
        menus=[MenuRule(id=MenuId.EDIT, group="1_undo_redo")],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyZ)],
    ),
    Action(
        id=CommandId.REDO,
        title="Redo",
        icon=FA6S.rotate_right,
        callback=functions.redo,
        menus=[MenuRule(id=MenuId.EDIT, group="1_undo_redo")],
        keybindings=[
            KeyBindingRule(primary=KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.KeyZ)
        ],
    ),
    Action(
        id=CommandId.CUT,
        title="Cut",
        icon=FA6S.scissors,
        callback=functions.cut,
        menus=[MenuRule(id=MenuId.EDIT, group="3_copypaste")],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyX)],
    ),
    Action(
        id=CommandId.COPY,
        title="Copy",
        icon=FA6S.copy,
        callback=functions.copy,
        menus=[MenuRule(id=MenuId.EDIT, group="3_copypaste")],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyC)],
    ),
    Action(
        id=CommandId.PASTE,
        title="Paste",
        icon=FA6S.paste,
        callback=functions.paste,
        menus=[MenuRule(id=MenuId.EDIT, group="3_copypaste")],
        keybindings=[KeyBindingRule(primary=KeyMod.CtrlCmd | KeyCode.KeyV)],
    ),
]
