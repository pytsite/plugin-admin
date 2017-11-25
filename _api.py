"""Admin Admin Plugin API Functions
"""
from pytsite import tpl as _tpl, http as _http, reg as _reg, router as _router, package_info as _package_info
from plugins import assetman as _assetman, widget as _widget, auth as _auth, form as _form
from . import _sidebar

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def base_path() -> str:
    """Get base path of the admin interface.
    """
    return _reg.get('admin.base_path', '/admin')


def render(content: str) -> str:
    """Render admin page with content.
    """
    if not _auth.get_current_user().has_permission('admin.use'):
        raise _http.error.Forbidden()

    return _tpl.render('admin@html', {
        'admin_sidebar': _sidebar.render(),
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'content': content,
        'core_name': _package_info.name('pytsite'),
        'core_url': _package_info.url('pytsite'),
        'core_version': _package_info.version('pytsite'),
        'sidebar_collapsed': _router.request().cookies.get('adminSidebarCollapsed') is not None,
    })


def render_form(frm: _form.Form) -> str:
    """Render a form within the admin page.
    """
    _assetman.preload('admin@css/admin-form.css')
    frm.css += ' admin-form'

    return render(_tpl.render('admin@form', {'form': frm}))
