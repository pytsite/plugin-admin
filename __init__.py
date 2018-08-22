"""PytSite Admin Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import base_path, render, register_theme, navbar, sidebar
from ._theme import Theme
from ._navbar import NavBar
from ._sidebar import SideBar


def plugin_load():
    """Hook
    """
    from pytsite import lang

    # Resources
    lang.register_package(__name__)


def plugin_load_uwsgi():
    """Hook
    """
    from pytsite import tpl, router
    from plugins import auth_ui, robots_txt
    from . import _controllers, _api

    bp = base_path()

    # 'Miscellaneous' sidebar's section
    sidebar.add_section('misc', 'admin@miscellaneous', 500)

    # Dashboard route
    router.handle(_controllers.Dashboard, bp, 'admin@dashboard', filters=auth_ui.AuthFilter)

    # Tpl globals
    tpl.register_global('admin_base_path', bp)

    # robots.txt rules
    robots_txt.disallow(bp + '/')
