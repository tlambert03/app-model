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
from typing import TYPE_CHECKING

from ._action import Action
from ._command_rule import CommandRule, ToggleRule
from ._icon import Icon
from ._keybinding_rule import KeyBindingRule
from ._keys import (
    KeyBinding,
    KeyChord,
    KeyCode,
    KeyCombo,
    KeyMod,
    SimpleKeyBinding,
    StandardKeyBinding,
)
from ._menu_rule import MenuItem, MenuItemBase, MenuRule, SubmenuItem

if TYPE_CHECKING:
    from typing import Callable, TypeAlias

    from ._icon import IconOrDict as IconOrDict
    from ._keybinding_rule import KeyBindingRuleDict as KeyBindingRuleDict
    from ._keybinding_rule import KeyBindingRuleOrDict as KeyBindingRuleOrDict
    from ._menu_rule import MenuOrSubmenu as MenuOrSubmenu
    from ._menu_rule import MenuRuleDict as MenuRuleDict
    from ._menu_rule import MenuRuleOrDict as MenuRuleOrDict

    # function that can be called without arguments to dispose of a resource
    DisposeCallable: TypeAlias = Callable[[], None]


__all__ = [
    "Action",
    "CommandRule",
    "Icon",
    "KeyBinding",
    "KeyBindingRule",
    "KeyChord",
    "KeyCode",
    "KeyCombo",
    "KeyMod",
    "MenuItem",
    "MenuItemBase",
    "MenuRule",
    "ScanCode",
    "SimpleKeyBinding",
    "StandardKeyBinding",
    "SubmenuItem",
    "ToggleRule",
]
