"""PytSite Admin Plugin Controllers
"""

from pytsite import routing as _routing, metatag as _metatag, lang as _lang
from plugins import auth as _auth, auth_ui as _auth_ui
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AdminAccessFilterController(_auth_ui.AuthFilterController):
    """Admin Access Routing Filter
    """

    def exec(self):
        r = super().exec()
        if r:
            return r

        if not _auth.get_current_user().has_permission('admin.use'):
            raise self.forbidden()


class Dashboard(_routing.Controller):
    """Dashboard controller
    """

    def exec(self):
        _metatag.t_set('title', _lang.t('admin@dashboard'))

        return _api.render('')
