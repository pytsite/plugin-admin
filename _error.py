"""PytSite Amdin Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class ThemeNotRegistered(Error):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return "Admin theme '{}' is not registered".format(self._name)


class ThemeAlreadyRegistered(Error):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return "Admin theme '{}' is already registered".format(self._name)


class NoThemesRegistered(Error):
    def __str__(self) -> str:
        return "There is no admin themes registered"
