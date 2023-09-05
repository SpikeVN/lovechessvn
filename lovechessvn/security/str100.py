# Copyright (c) 2022-2023 SpikeBonjour
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
STR100: ``str.format()`` allows injected string to access
        a class' internal attributes.

See this: https://pycharm-security.readthedocs.io/en/latest/checks/STR100.html
"""

from collections.abc import Mapping
from string import Formatter


class MagicFormatMapping(Mapping):
    """This class implements a dummy wrapper to fix a bug in the Python
    standard library for string formatting.

    See http://bugs.python.org/issue13598 for information about why
    this is necessary.
    """

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self._last_index = 0

    def __getitem__(self, key):
        if key == "":
            idx = self._last_index
            self._last_index += 1
            try:
                return self._args[idx]
            except LookupError:
                pass
            key = str(idx)
        return self._kwargs[key]

    def __iter__(self):
        return iter(self._kwargs)

    def __len__(self):
        return len(self._kwargs)


# This is a necessary API but it's undocumented and moved around
# between Python releases
try:
    from _string import formatter_field_name_split
except ImportError:

    def formatter_field_name_split(x):
        return x._formatter_field_name_split()


class SafeFormatter(Formatter):
    def get_field(self, field_name, args, kwargs):
        first, rest = formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = safe_getattr(obj, i)
            else:
                obj = obj[i]
        return obj, first


def safe_getattr(obj, attr):
    """
    Safely gets an attribute of an object, avoiding STR100 exploit.
    """
    # Expand the logic here.  For instance on 2.x you will also need
    # to disallow func_globals, on 3.x you will also need to hide
    # things like cr_frame and others.  So ideally have a list of
    # objects that are entirely unsafe to access.
    if attr[:1] == "_":
        raise AttributeError(attr)
    return getattr(obj, attr)


def safe_format(_string, *args, **kwargs):
    """
    Safely formats a string, avoiding STR100 exploit.
    """
    formatter = SafeFormatter()
    kwargs = MagicFormatMapping(args, kwargs)
    return formatter.vformat(_string, args, kwargs)
