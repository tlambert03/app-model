"""app-model types.

The most important type in this module is [`Action`][app_model.types.Action].
It is the "complete" representation of a command, and comprises:

- [`CommandRule`][app_model.types.CommandRule] - metadata about the command, including
  title, icon, and tooltips, etc.
- [`MenuRule`][app_model.types.MenuRule] - rules defining which menu(s) the command
  should appear in.
- [`KeyBindingRule`][app_model.types.KeyBindingRule] - rules defining which
  keybinding(s) should trigger the command.

Most of the other types defined in this module are in support of these four types.
"""
from ._action import Action
from ._command_rule import CommandRule, ToggleRule
from ._icon import Icon, IconOrDict
from ._keybinding_rule import KeyBindingRule, KeyBindingRuleDict, KeyBindingRuleOrDict
from ._keys import (
    KeyBinding,
    KeyChord,
    KeyCode,
    KeyCombo,
    KeyMod,
    SimpleKeyBinding,
    StandardKeyBinding,
)
from ._menu_rule import (
    MenuItem,
    MenuItemBase,
    MenuOrSubmenu,
    MenuRule,
    MenuRuleDict,
    MenuRuleOrDict,
    SubmenuItem,
)

__all__ = [
    "Action",
    "CommandRule",
    "Icon",
    "IconOrDict",
    "KeyBinding",
    "KeyBindingRule",
    "KeyBindingRuleDict",
    "KeyBindingRuleOrDict",
    "KeyChord",
    "KeyCode",
    "KeyCombo",
    "KeyMod",
    "MenuItem",
    "MenuItemBase",
    "MenuOrSubmenu",
    "MenuRule",
    "MenuRuleDict",
    "MenuRuleOrDict",
    "ScanCode",
    "SimpleKeyBinding",
    "StandardKeyBinding",
    "SubmenuItem",
    "ToggleRule",
]
