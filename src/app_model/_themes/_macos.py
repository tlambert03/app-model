from app_model.types._theme import ColorGroup, Palette, Theme

# Define the QSS template
MACOS_QSS_TEMPLATE = """
/* --------------------------------------- */

QLineEdit, QAbstractSpinBox, QPushButton, QComboBox {{
    border: 0.5px solid {mid};
    placeholder-text-color: {placeholder_text};
}}


/* --------------------------------------- */

/* border-gradient */

QPushButton, QComboBox {{
    height: 20px;
    background-color: {button};
    border-radius: 6px;
    padding: 0px 8px;
    border-top-color: #848484;
    border-bottom-color: #272727;
    selection-background-color: {highlight};
    color: {button_text};
}}

QPushButton::pressed {{
    background-color: #7B7B7B;
}}

/* --------------------------------------- */


QComboBox {{
    padding-left: 8px;
}}

QComboBox::drop-down:button {{
    border-radius:4px;
    margin: 1.5px;
    width: 14px;
    background-color: none;
}}

QComboBox::down-arrow {{
    image: url({down_arrow_svg});
    margin-right: 4px;
}}

/* --------------------------------------- */

QSlider::add-page {{
    background-color: #474747;
}}

QSlider::groove, QSlider::add-page {{
    border: 0px;
    border-radius: 2px;
}}

QSlider::groove::horizontal {{
    height: 4px;
}}

QSlider::groove::vertical {{
    width: 4px;
}}

QSlider::groove {{
    background: {highlight};
}}

QSlider::handle {{
    background: #9A9493;
    border: 0.5px solid {mid};
    width: 18px;
    margin: -8px 0;
    border-radius: 10px;
}}

/* --------------------------------------- */

QTabWidget::pane {{
    background: {light};
    border: 1px solid #464646;
    border-radius: 4px;
    margin-top: -12px;
}}

QTabBar::tab {{
    background: {button};
    padding: 4px;
    border-radius: 4px;
}}

/* --------------------------------------- */
QToolButton:hover {{
    background-color: {mid};
}}

QToolBar {{
    background: {window};
    spacing: 3px; /* spacing between items in the tool bar */
    border: none; /* disables native style on macos */
}}

QToolBar::handle {{
    background: {midlight};
    width: 4px;
    margin: 2px;
}}
"""


MACOS_LIGHT = Theme(
    name="macos-light",
    qss_template=MACOS_QSS_TEMPLATE,
    palette=Palette(
        active=ColorGroup(
            window="#ececec",
            window_text="#000000",
            base="#ffffff",
            alternate_base="#f5f5f5",
            tool_tip_base="#ffffff",
            tool_tip_text="#000000",
            placeholder_text="#000000",
            text="#000000",
            button="#ececec",
            button_text="#000000",
            bright_text="#ffffff",
            light="#ffffff",
            midlight="#f5f5f5",
            mid="#a9a9a9",
            dark="#bfbfbf",
            shadow="#000000",
            highlight="#a5cdff",
            accent="#0a60ff",
            highlighted_text="#000000",
            link="#094fd1",
            link_visited="#ff00ff",
            no_role="#000000",
        ),
        inactive=ColorGroup(
            highlight="#d4d4d4",
            link="#0000ff",
        ),
        disabled=ColorGroup(
            base="#ececec",
            highlight="#d4d4d4",
            link="#0000ff",
        ),
    ),
)

MACOS_DARK = Theme(
    name="macos-dark",
    qss_template=MACOS_QSS_TEMPLATE,
    palette=Palette(
        active=ColorGroup(
            window="#323232",
            window_text="#ffffff",
            base="#171717",
            alternate_base="#989898",
            tool_tip_base="#ffffff",
            tool_tip_text="#000000",
            placeholder_text="#595959",
            text="#ffffff",
            # button="#323232", # from Qt
            button="#656565",  # measured
            button_text="#ffffff",
            # bright_text="#373737", # from Qt
            bright_text="#E7E7E7",  # measured
            light="#373737",
            midlight="#343434",
            mid="#242424",
            dark="#bfbfbf",
            shadow="#000000",
            # highlight="#314f78",
            highlight="#007AFF",  # default macos blue
            accent="#0a60ff",
            highlighted_text="#ffffff",
            link="#3586ff",
            link_visited="#ff00ff",
            no_role="#000000",
        ),
        inactive=ColorGroup(
            button_text="#000000",
            highlight="#363636",
            link="#0000ff",
        ),
        disabled=ColorGroup(
            base="#323232",
            highlight="#363636",
            link="#0000ff",
        ),
    ),
)
