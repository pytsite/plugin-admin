"""PytSite Admin Plugin Events Handlers
"""
from pytsite import lang as _lang, router as _router
from plugins import hreflang as _hreflang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """'pytsite.router.dispatch' event handler
    """
    if _router.current_path(True).startswith(_api.base_path()):
        # Alternate languages
        for lng in _lang.langs(False):
            _hreflang.add(lng, _router.url(_router.current_path(), lang=lng))
