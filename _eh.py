"""PytSite Admin Plugin Events Handlers
"""
from pytsite import lang as _lang, router as _router, http as _http
from plugins import auth as _auth, hreflang as _hreflang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """'pytsite.router.dispatch' event handler
    """
    if _router.current_path(True).startswith(_api.base_path()):
        c_user = _auth.get_current_user()

        if c_user.is_anonymous:
            r_url = _router.rule_url('auth_web@sign_in', {
                'driver': _auth.get_auth_driver().get_name(),
                '__redirect': _router.current_path(strip_lang=False)
            })
            raise _http.error.Forbidden(response=_http.response.Redirect(r_url))

        if not c_user.has_permission('admin.use'):
            raise _http.error.Forbidden()

        # Alternate languages
        for lng in _lang.langs(False):
            _hreflang.add(lng, _router.url(_router.current_path(), lang=lng))
