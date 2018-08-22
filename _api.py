"""Admin Admin Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union, Dict as _Dict
from pytsite import reg as _reg, html as _html, router as _router, http as _http
from plugins import auth as _auth, auth_ui as _auth_ui

from . import _error
from ._theme import Theme as _Theme
from ._navbar import NavBar as _NavBar
from ._sidebar import SideBar as _SideBar

navbar = _NavBar()
sidebar = _SideBar()
_themes = {}  # type: _Dict[str, _Theme]
_fallback_theme_name = None  # type: str


def base_path() -> str:
    """Get base path of the admin interface.
    """
    return _reg.get('admin.base_path', '/admin')


def register_theme(theme: _Theme):
    """Register a theme
    """
    global _themes, _fallback_theme_name

    if theme.name in _themes:
        raise _error.ThemeAlreadyRegistered(theme.name)

    _themes[theme.name] = theme

    if not _fallback_theme_name:
        _fallback_theme_name = theme.name


def render(content: _Union[str, _html.Element]) -> _Union[str, _http.RedirectResponse]:
    """Render admin page with content.
    """
    if not _themes:
        raise _error.NoThemesRegistered()

    if _auth.get_current_user().is_anonymous:
        return _http.response.Redirect(_auth_ui.sign_in_url(redirect=_router.current_url()))

    theme_name = _reg.get('admin.theme', _fallback_theme_name)
    try:
        theme = _themes[theme_name]
    except KeyError:
        raise _error.ThemeNotRegistered(theme_name)

    return theme.render(navbar, sidebar, content)
