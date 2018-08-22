"""PytSite Admin Plugin Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, metatag as _metatag, lang as _lang
from plugins import auth as _auth
from . import _api


class Dashboard(_routing.Controller):
    """Dashboard controller
    """

    def exec(self):
        _metatag.t_set('title', _lang.t('admin@dashboard'))

        user = _auth.get_current_user()
        if not (user.is_anonymous or user.is_admin) and not _api.sidebar.items[0]:
            raise self.forbidden()

        return _api.render('')
