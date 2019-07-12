"""PytSite Admin Theme
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union
from abc import ABC, abstractmethod
from . import _navbar, _sidebar


class Theme(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def render(self, navbar: _navbar.NavBar, sidebar: _sidebar.SideBar, content: Union[str, htmler.Element]) -> str:
        """Render an admin page
        """
        raise NotImplementedError()
