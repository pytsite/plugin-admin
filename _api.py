"""Admin Admin Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union, Dict
from pytsite import reg, router, http
from plugins import auth, auth_ui

from . import _error
from ._theme import Theme as _Theme
from ._navbar import NavBar as _NavBar
from ._sidebar import SideBar as _SideBar

navbar = _NavBar()
sidebar = _SideBar()
_themes = {}  # type: Dict[str, _Theme]
_fallback_theme_name = None  # type: str


def base_path() -> str:
    """Get base path of the admin interface.
    """
    return reg.get('admin.base_path', '/admin')


def register_theme(theme: _Theme):
    """Register a theme
    """
    global _themes, _fallback_theme_name

    if theme.name in _themes:
        raise _error.ThemeAlreadyRegistered(theme.name)

    _themes[theme.name] = theme

    if not _fallback_theme_name:
        _fallback_theme_name = theme.name


def render(content: Union[str, htmler.Element]) -> Union[str, http.RedirectResponse]:
    """Render admin page with content.
    """
    if not _themes:
        raise _error.NoThemesRegistered()

    if auth.get_current_user().is_anonymous:
        return http.response.Redirect(auth_ui.sign_in_url(redirect=router.current_url()))

    theme_name = reg.get('admin.theme', _fallback_theme_name)
    try:
        theme = _themes[theme_name]
    except KeyError:
        raise _error.ThemeNotRegistered(theme_name)

    return theme.render(navbar, sidebar, content)
