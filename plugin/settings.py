"""Helper methods to read, write and clear settings.

Copyright 2013 Google Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from PyQt4.QtCore import QSettings


def read(key, object_type=str):
  """Reads the given setting key.

  Args:
    key: str, key to look up.
    object_type: convert the value to the given object type.
  Returns:
    setting value if found, None if not found.
  """
  s = QSettings()
  if s.contains(key):
    return s.value(key, type=object_type)
  else:
    return None


def write(key, val):
  """Write the given key value pair to settings.

  Args:
    key: str, settings key
    val: QVariant, value to write.
  """
  s = QSettings()
  s.setValue(key, val)


def clear():
  """Removes the user data from settings."""
  s = QSettings()
  s.remove('gmeconnector/ACCESS_TOKEN')
  s.remove('gmeconnector/REFRESH_TOKEN')
  s.remove('gmeconnector/EXPIRES_AT')
  s.remove('gmeconnector/PROJECTS')
