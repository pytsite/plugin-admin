"""PytSite Admin Plugin Events Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang, router as _router
from plugins import hreflang as _hreflang
from . import _api


def router_dispatch():
    """'pytsite.router.dispatch' event handler
    """
    if _router.current_path(add_lang_prefix=False).startswith(_api.base_path()):
        # Alternate languages
        for lng in _lang.langs(False):
            _hreflang.add(lng, _router.current_url(True, add_lang_prefix=True, lang=lng))
