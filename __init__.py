"""PytSite Admin Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

# Public API
if _plugman.is_installed(__name__):
    from . import _sidebar as sidebar, _navbar as navbar
    from ._api import render, render_form, base_path
    from ._controllers import AdminAccessFilterController


def plugin_load():
    from pytsite import lang
    from plugins import assetman

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Assetman tasks
    assetman.t_js(__name__)
    assetman.t_css(__name__)
    assetman.t_less(__name__)

    # JS modules
    assetman.js_module('pytsite-admin-lte', __name__ + '@AdminLTE/js/app', True, ['jquery', 'twitter-bootstrap'])


def plugin_load_uwsgi():
    """Hook
    """
    from pytsite import tpl, router
    from plugins import assetman, permissions, robots_txt
    from . import _eh, _controllers

    bp = base_path()

    # Resources
    tpl.register_package(__name__)

    # Assets
    assetman.preload('font-awesome', True, path_prefix=bp)
    assetman.preload('twitter-bootstrap', True, path_prefix=bp)
    assetman.preload('admin@AdminLTE/css/AdminLTE.css', True, path_prefix=bp)
    assetman.preload('admin@AdminLTE/css/skins/skin-blue.css', True, path_prefix=bp)
    assetman.preload('admin@css/custom.css', True, path_prefix=bp)
    assetman.preload('admin@css/admin-form.css', True, path_prefix=bp)
    assetman.preload('admin@js/pytsite-admin.js', True, path_prefix=bp)

    # Permissions
    permissions.define_permission('admin.use', 'admin@use_admin_panel', 'app')

    # Dashboard route
    router.handle(_controllers.Dashboard, bp, 'admin@dashboard', filters=AdminAccessFilterController)

    # Tpl globals
    tpl.register_global('admin_base_path', bp)

    sidebar.add_section('misc', 'admin@miscellaneous', 500)

    # robots.txt rules
    robots_txt.disallow(bp + '/')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)
