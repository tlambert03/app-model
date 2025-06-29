from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel, Field

from app_model.types._base import _BaseModel
from app_model.types._icon import Icon

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Literal, TypeAlias

    ColorGroupName: TypeAlias = Literal["active", "inactive", "disabled"]
    ColorRoleName: TypeAlias = Literal[
        "window"
        "window_text"
        "base"
        "alternate_base"
        "tool_tip_base"
        "tool_tip_text"
        "placeholder_text"
        "text"
        "button"
        "button_text"
        "bright_text"
        "light"
        "midlight"
        "mid"
        "dark"
        "shadow"
        "highlight"
        "accent"
        "highlighted_text"
        "link"
        "link_visited"
        "no_role"
    ]


# TODO: determine what pattern this should follow.
# It needs to be some sort of mapping of icon-key to a path/URL/iconify key, etc.
class ThemeIcons(_BaseModel):
    """Icons used in the theme."""

    down_arrow_svg: str = "fluent:chevron-down-16-filled"
    """Down arrow used to the right of, e.g. ComboBox."""


class ColorGroup(_BaseModel):
    """Qt ColorGroup model."""

    window: str = ""
    """A general background color."""

    window_text: str = ""
    """A general foreground color."""

    base: str = ""
    """Used mostly as the background color for text entry widgets, but can also be used
    for other painting - such as the background of combobox drop down lists and toolbar
    handles. It is usually white or another light color."""

    alternate_base: str = ""
    """Used as the alternate background color in views with alternating row colors."""

    tool_tip_base: str = ""
    """Used as the background color for QToolTip and QWhatsThis. Tool tips use the
    Inactive color group of QPalette, because tool tips are not active windows."""

    tool_tip_text: str = ""
    """Used as the foreground color for QToolTip and QWhatsThis. Tool tips use the
    Inactive color group of QPalette, because tool tips are not active windows."""

    placeholder_text: str = ""
    """Used as the placeholder color for various text input widgets."""

    text: str = ""
    """The foreground color used with Base. This is usually the same as the WindowText,
    in which case it must provide good contrast with Window and Base."""

    button: str = ""
    """The general button background color. This background can be different from Window
    as some styles require a different background color for buttons."""

    button_text: str = ""
    """A foreground color used with the Button color."""

    bright_text: str = ""
    """A text color that is very different from WindowText, and contrasts well with e.g.
    Dark. Typically used for text that needs to be drawn where Text or WindowText would
    give poor contrast, such as on pressed push buttons. Note that text colors can be
    used for things other than just words; text colors are usually used for text, but
    it's quite common to use the text color roles for lines, icons, etc."""

    # These color roles used mostly for 3D bevel and shadow effects.
    # All of these are normally derived from Window, and used in ways that depend on
    # that relationship. For example, buttons depend on it to make the bevels look
    # attractive, and Motif scroll bars depend on Mid to be slightly different from
    # Window.

    light: str = ""
    """Lighter than Button color."""
    midlight: str = ""
    """Between Button and Light."""
    mid: str = ""
    """Between Button and Dark."""
    dark: str = ""
    """Darker than Button."""
    shadow: str = ""
    """A very dark color. By default, the shadow color is Qt::black."""

    # Selected (marked) items have two roles:
    highlight: str = ""
    """A color to indicate a selected item or the current item. By default, the
    highlight color is darkBlue."""
    accent: str = ""  # since Qt 6.6
    """A color that typically contrasts or complements Base, Window and Button colors.
    It usually represents the users' choice of desktop personalisation. Styling of
    interactive components is a typical use case. Unless explicitly set, it defaults to
    Highlight."""
    highlighted_text: str = ""
    """A text color that contrasts with Highlight. By default, the highlighted text
    color is white."""

    # related to hyperlinks:
    link: str = ""
    """A text color used for unvisited hyperlinks. By default, blue"""
    link_visited: str = ""
    """A text color used for already visited hyperlinks. By default, magenta"""

    no_role: str = ""
    """This special role is often used to indicate that a role has not been assigned."""

    def __rich_repr__(self) -> Iterable[tuple[str, Any]]:
        """Rich repr without default values."""
        for key, value in self.model_dump().items():
            if value:
                yield key, value


class Palette(_BaseModel):
    """Qt Palette model.

    In most styles, Active and Inactive look the same.
    """

    active: ColorGroup = Field(default_factory=ColorGroup)
    """Group used for the window that has keyboard focus."""

    inactive: ColorGroup = Field(default_factory=ColorGroup)
    """Group used for other windows."""

    disabled: ColorGroup = Field(default_factory=ColorGroup)
    """Group used for widgets (not windows) that are disabled for some reason."""

    def color(self, group: ColorGroupName, role: ColorRoleName) -> str:
        """Return color for the given role and state."""
        color_group = getattr(self, group)
        color = cast("str", getattr(color_group, role))
        if not color and group != "active":
            # it's possible that disabled should also check in inactive first...
            return self.color("active", role)
        return color


THEME_REGISTRY: dict[str, Theme] = {}


class Theme(BaseModel):
    """Theme model for the application."""

    name: str
    """Name of the theme."""

    palette: Palette = Field(default_factory=Palette)
    """Palette used in the theme."""

    qss_template: str = ""

    standard_icons: ThemeIcons = Field(default_factory=ThemeIcons)
    """Icons used in the theme."""

    extra_icons: Mapping[str, str | Icon | None] = Field(default_factory=dict)
    """Additional icons that can be used in the theme, e.g. for action-defined icons."""

    def model_post_init(self, context: Any, /) -> None:
        """Post-initialization checks."""
        if self.name in THEME_REGISTRY:
            raise ValueError(f"Theme with name '{self.name}' already exists.")
        THEME_REGISTRY[self.name] = self

    def icon_paths(self) -> dict[str, str]:
        color = self.palette.active.dark or None
        icons: dict[str, str] = self.standard_icons.model_dump()

        if self.extra_icons:
            for k, v in self.extra_icons.items():
                if isinstance(v, Icon):
                    if key := (v.dark or v.light or None):
                        icons[k] = key
                elif isinstance(v, str):
                    icons[k] = v

        return {k: _to_posix(v, color=color or None) for k, v in icons.items() if v}


def _to_posix(icn: str, color: str | None = None) -> str:
    """Convert an icon path or key to a POSIX path."""
    if icn.startswith("file://"):
        return Path(icn[7:]).as_posix()
    elif ":" in icn:
        from pyconify import svg_path

        return svg_path(icn, color=color).as_posix()
    else:
        raise NotImplementedError(f"Icon format '{icn}' is not supported. ")


@cache
def _register_builtins() -> None:
    """Register built-in themes."""
    from app_model._themes import _macos  # noqa: F401


def get_theme(name: str) -> Theme:
    """Get a theme by name."""
    _register_builtins()

    if (theme := THEME_REGISTRY.get(name)) is None:
        available_themes = ", ".join(THEME_REGISTRY.keys())
        raise ValueError(
            f"Theme with name '{name}' not found. "
            f"Available themes are: {available_themes}"
        )
    return theme


def get_available_themes() -> list[str]:
    """Get a list of available themes."""
    _register_builtins()
    return list(THEME_REGISTRY.keys())
