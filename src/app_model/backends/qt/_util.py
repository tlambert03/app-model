from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtGui import QIcon

if TYPE_CHECKING:
    from typing import Literal

    from app_model.types import Icon


def to_qicon(icon: Icon, theme: Literal["dark", "light"] = "dark") -> QIcon:
    """Create QIcon from Icon."""
    from superqt import fonticon

    return fonticon.icon(icn) if (icn := getattr(icon, theme, "")) else QIcon()
