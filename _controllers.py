"""PytSite Admin Plugin Controllers
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, metatag as _metatag, lang as _lang
from . import _api


class Dashboard(_routing.Controller):
    """Dashboard controller
    """

    def exec(self):
        _metatag.t_set('title', _lang.t('admin@dashboard'))

        return _api.render('')
