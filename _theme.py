"""PytSite Admin Theme
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import html as _html
from . import _navbar, _sidebar


class Theme(_ABC):

    @property
    @_abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @_abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    @_abstractmethod
    def render(self, navbar: _navbar.NavBar, sidebar: _sidebar.SideBar, content: _Union[str, _html.Element]) -> str:
        """Render an admin page
        """
        raise NotImplementedError()
