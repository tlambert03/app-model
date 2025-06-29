from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING, cast

from qtpy.QtGui import QColor, QGuiApplication, QPalette
from qtpy.QtWidgets import QApplication

from app_model.types._theme import ColorGroup, Palette, Theme

if TYPE_CHECKING:
    from app_model.types._theme import ColorRoleName


def _to_snake_case(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def _to_camel_case(s: str) -> str:
    return "".join(word.title() for word in s.split("_"))


def qpalette_to_palette(qpalette: QPalette, palette_type: type[Palette]) -> Palette:
    """Convert a QPalette to app_model.Palette."""
    CG = QPalette.ColorGroup
    CR = QPalette.ColorRole

    data = defaultdict[str, dict](dict)
    for group in (CG.Active, CG.Inactive, CG.Disabled):
        group_name = group.name.lower()
        for role in CR:
            if role == CR.NColorRoles:
                continue
            role_name = _to_snake_case(role.name)
            color = qpalette.color(group, role).name()
            if group == CG.Active or (data["active"][role_name] != color):
                data[group_name][role_name] = color

    return palette_type(
        active=ColorGroup(**data["active"]),
        inactive=ColorGroup(**data["inactive"]),
        disabled=ColorGroup(**data["disabled"]),
    )


def palette_to_qpalette(palette: Palette) -> QPalette:
    """Convert an app_model.Palette to QPalette."""
    qpalette = QGuiApplication.palette()
    for group in ("active", "inactive", "disabled"):
        qgroup = getattr(qpalette.ColorGroup, group.capitalize())
        for field_ in ColorGroup.model_fields:
            role_name = cast("ColorRoleName", field_)
            try:
                qrole = getattr(qpalette.ColorRole, _to_camel_case(role_name))
            except AttributeError:
                continue
            color = palette.color(group, role_name)
            qpalette.setColor(qgroup, qrole, QColor(color))
    return qpalette


def theme_to_qss(theme: Theme) -> str:
    """Convert a app_model.Theme to a QSS string."""
    active_palette = theme.palette.active
    icon_paths = theme.icon_paths()
    qss = theme.qss_template.format(**active_palette.model_dump(), **icon_paths)
    for key, value in icon_paths.items():
        qss += f"""
QToolBar QToolButton#action-{key} {{
    qproperty-icon: url({value});
}}
        """
    return qss


def apply_palette_to_qapp(palette: Palette, app: QApplication) -> None:
    """Apply app_model.Palette to a QApplication instance."""
    app.setPalette(palette_to_qpalette(palette))


def apply_theme_to_qapp(theme: Theme, app: QApplication | None = None) -> None:
    """Apply app_model.Theme to a QApplication instance."""
    if app is None:
        _app = QApplication.instance()
        if _app is None:  # pragma: no cover
            raise RuntimeError(
                "No QApplication instance found. Please create one first."
            )
        if not isinstance(_app, QApplication):  # pragma: no cover
            raise TypeError(f"Expected a QApplication instance, got {type(_app)}")
        app = _app

    app.setStyleSheet(theme_to_qss(theme))
    apply_palette_to_qapp(theme.palette, app)

    # TODO: connect signals to update the theme dynamically if needed
