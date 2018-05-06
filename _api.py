"""Admin Admin Plugin API Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union, Dict as _Dict
import re as _re
from pytsite import reg as _reg, html as _html, router as _router, http as _http
from plugins import auth as _auth
from . import _error
from ._theme import Theme as _Theme
from ._navbar import NavBar as _NavBar
from ._sidebar import SideBar as _SideBar

navbar = _NavBar()
sidebar = _SideBar()
_themes = {}  # type: _Dict[str, _Theme]
_fallback_theme_name = None  # type: str
_permissions = []


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


def render(content: _Union[str, _html.Element]) -> str:
    """Render admin page with content.
    """
    if not _themes:
        raise _error.NoThemesRegistered()

    theme_name = _reg.get('admin.theme', _fallback_theme_name)
    try:
        theme = _themes[theme_name]
    except KeyError:
        raise _error.ThemeNotRegistered(theme_name)

    current_path = _router.current_path(True)

    if current_path == base_path():
        return theme.render(navbar, sidebar, content)

    if check_permissions(current_path):
        return theme.render(navbar, sidebar, content)

    # Path's permissions is not defined
    raise _http.error.Forbidden()


def define_permissions(path: str, roles: _Union[str, list, tuple], permissions: _Union[str, list, tuple]):
    """Define permissions for a path
    """
    _permissions.append({
        're': _re.compile(path),
        'roles': roles,
        'permissions': permissions,
    })


def check_permissions(path: str) -> bool:
    user = _auth.get_current_user()

    if user.is_anonymous:
        return False

    for item in _permissions:
        if not item['re'].match(path):
            continue

        roles = item['roles']
        perms = item['permissions']

        if roles is not None and roles != '*' and user.has_role(roles):
            return True
        elif perms is not None and perms != '*' and user.has_permission(perms):
            return True
        elif roles == '*' and perms == '*':
            return True

    return False
