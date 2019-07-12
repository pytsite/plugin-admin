"""PytSite Admin Plugin Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing, metatag, lang
from plugins import auth
from . import _api


class Dashboard(routing.Controller):
    """Dashboard controller
    """

    def exec(self):
        metatag.t_set('title', lang.t('admin@dashboard'))

        user = auth.get_current_user()
        if not (user.is_anonymous or user.is_admin) and not _api.sidebar.items[0]:
            raise self.forbidden()

        return _api.render('')
