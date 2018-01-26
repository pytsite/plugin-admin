"""PytSite Admin Plugin Sidebar API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union, Tuple as _Tuple
from pytsite import util as _util, lang as _lang, events as _events, router as _router
from . import _api


class SideBar:
    def __init__(self):
        self._sections = []
        self._menus = {}
        self._last_section_weight = 0

    def get_section(self, sid: str) -> dict:
        """Get a section
        """
        if sid not in self._menus:
            return {}

        for s in self._sections:
            if s['sid'] == sid:
                return s

    def add_section(self, sid: str, title: str, weight: int = 0, sort_items_by: str = 'weight'):
        """Add a section
        """
        if self.get_section(sid):
            raise KeyError("Section '{}' is already defined".format(sid))

        if not weight:
            weight = self._last_section_weight + 100

        self._last_section_weight = weight
        self._sections.append({
            'sid': sid,
            'title': title,
            'weight': weight,
            'sort_items_by': sort_items_by,
        })

        self._menus[sid] = []
        self._sections = _util.weight_sort(self._sections)

    def get_menu(self, sid: str, mid: str) -> dict:
        """Get a menu of a section
        """
        section = self.get_section(sid)
        if not section:
            raise KeyError("Section '{}' is not defined".format(sid))

        for m in self._menus[sid]:
            if m['mid'] == mid:
                return m

    def add_menu(self, sid: str, mid: str, title: str, path: str = '#', icon: str = None, label: str = None,
                 label_class: str = 'primary', weight: int = 0, roles: _Union[str, list, tuple] = ('admin', 'dev'),
                 permissions: _Union[str, list, tuple] = None, replace=False):
        """Add a menu to a section
        """
        # Check if the section exists
        section = self.get_section(sid)
        if not section:
            raise KeyError("Section '{}' is not defined.".format(sid))

        # Replace menu if it is necessary
        if self.get_menu(sid, mid):
            if replace:
                self.del_menu(sid, mid)
            else:
                raise KeyError("Menu '{}' already defined in section '{}'.".format(mid, sid))

        # Sanitize path
        if not path.startswith('/'):
            path = '/' + path
        if path.endswith('/'):
            path = path[:-1]

        # Prepare data structure
        menu_data = {
            'sid': sid,
            'mid': mid,
            'title': title,
            'path': path,
            'icon': icon,
            'label': label,
            'label_class': label_class,
            'weight': weight,
            'children': [],
        }

        # Add data to permissions store
        _api.add_path_permissions(path, roles, permissions)

        _events.fire('admin@sidebar_add_menu', menu_data=menu_data)
        _events.fire('admin@sidebar_add_menu.{}.{}'.format(sid, mid), menu_data=menu_data)

        self._menus[sid].append(menu_data)

        # Sort menu items
        # Sorting by weight performs at this point
        # Sorting by title will be performed every time when menu is being rendered
        if section['sort_items_by'] == 'weight':
            self._menus[sid] = _util.weight_sort(self._menus[sid])

    def del_menu(self, sid: str, mid: str):
        """Delete a menu from a section
        """
        section = self.get_section(sid)
        if not section:
            raise KeyError("Section '{}' is not defined.".format(sid))

        replace = []
        for m in self._menus[sid]:
            if m['mid'] != mid:
                replace.append(m)

        self._menus[sid] = replace

    @property
    def items(self) -> _Tuple[list, dict]:
        current_path = _router.current_path()
        base_path = _api.base_path()
        menus = {}

        for section in self._sections:
            # Permission to view menu
            menus[section['sid']] = []
            for menu in self._menus[section['sid']].copy():
                if _api.check_path_permissions(menu['path']):
                    menu['active'] = bool(current_path != base_path and menu['path'].endswith(current_path))
                    menus[section['sid']].append(menu)

            # Sort items by translated title
            if section['sort_items_by'] == 'title':
                menus[section['sid']] = sorted(menus[section['sid']], key=lambda x: _lang.t(x['title']))

        # Remove empty sections
        sections = [s for s in self._sections if len(menus[s['sid']])]

        return sections, menus
