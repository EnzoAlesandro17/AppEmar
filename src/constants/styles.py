"""
styles.py — Paleta de colores y stylesheet Qt (QSS) para la app PySide6.

Uso:
    from src.constants.styles import build_stylesheet

    ventana.setStyleSheet(build_stylesheet(dark=False))

Los valores de color son los mismos tokens del design system interno
(ver https://github.com/EnzoAlesandro17/design-system), solo que ahí
todavía no hay una versión para PySide/Qt — así que el QSS se arma acá,
pero cualquier cambio de paleta se decide primero en el repo del design
system, no acá.
"""

COLORS_LIGHT = {
    "primary": "#2E5FC7",
    "text_primary": "#323332",
    "bg_secondary": "#F0F0F0",
    "bg_primary": "#FFFFFF",
    "primary_soft": "#E6F0FF",
    "text_secondary": "#6B7280",
    "border": "#CBD1D9",
    "surface": "#FFFFFF",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#8B5CF6",
    "action_secondary": "#06B6D4",
}

COLORS_DARK = {
    "primary": "#3878EC",
    "text_primary": "#E6E6E6",
    "bg_secondary": "#1E1E1E",
    "bg_primary": "#121212",
    "primary_soft": "#1D2D5C",
    "text_secondary": "#9CA3AF",
    "border": "#2A2A2A",
    "surface": "#242424",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#8B5CF6",
    "action_secondary": "#06B6D4",
}

FONT_FAMILY = "Segoe UI"  # fallback: Qt usa la del sistema si no existe

FONT_SIZE_TITLE = 16
FONT_SIZE_SUBTITLE = 12
FONT_SIZE_BODY = 10
FONT_SIZE_SMALL = 9

# La barra superior siempre usa el azul oscuro del modo claro, sin importar
# el tema activo (no tiene sentido que la marca "salte" de color al
# alternar claro/oscuro).
HEADER_COLOR = COLORS_LIGHT["primary"]


def build_stylesheet(dark: bool = False) -> str:
    """Arma el QSS completo de la app a partir de la paleta clara u oscura."""
    c = COLORS_DARK if dark else COLORS_LIGHT

    return f"""
    QWidget {{
        background-color: {c["bg_primary"]};
        color: {c["text_primary"]};
        font-family: "{FONT_FAMILY}";
        font-size: {FONT_SIZE_BODY}pt;
    }}

    QLabel#titleLabel {{
        font-size: {FONT_SIZE_TITLE}pt;
        font-weight: bold;
    }}

    QLineEdit {{
        background-color: {c["bg_primary"]};
        color: {c["text_primary"]};
        border: 1px solid {c["border"]};
        border-radius: 4px;
        padding: 6px;
    }}
    QLineEdit:focus {{
        border: 1px solid {c["primary"]};
    }}

    QPushButton#primaryButton {{
        background-color: {c["primary"]};
        color: #FFFFFF;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 10px 16px;
    }}
    QPushButton#primaryButton:hover {{
        background-color: {c["primary_soft"]};
        color: {c["text_primary"]};
    }}

    QPushButton#secondaryButton {{
        background-color: {c["bg_secondary"]};
        color: {c["text_primary"]};
        font-weight: bold;
        border: 1px solid {c["border"]};
        border-radius: 4px;
        padding: 10px 16px;
    }}
    QPushButton#secondaryButton:hover {{
        background-color: {c["primary_soft"]};
    }}

    QWidget#headerBar {{
        background-color: {HEADER_COLOR};
    }}
    QLabel#headerTitle {{
        color: #FFFFFF;
        font-size: {FONT_SIZE_SUBTITLE}pt;
        font-weight: bold;
        background: transparent;
    }}

    QPushButton#themeToggleButton {{
        background: transparent;
        border: none;
        color: #FFFFFF;
        font-size: {FONT_SIZE_BODY}pt;
    }}

    QPushButton#avatarButton {{
        background-color: #FFFFFF;
        color: {HEADER_COLOR};
        border: none;
        border-radius: 18px;
        font-weight: bold;
    }}
    QPushButton#avatarButton::menu-indicator {{
        image: none;
        width: 0px;
    }}
    """
