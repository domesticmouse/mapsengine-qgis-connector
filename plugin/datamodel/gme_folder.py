"""Class to create a python Folder object from JSON.

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
import gme_item


class Folder(object):
  """Google Maps Engine Folder.

  Properties are documented at
  https://developers.google.com/maps-engine/documentation/reference/v1/
  """

  def __init__(self, name=None, key=None, contents=None, **kwargs):
    self.name = name
    self.key = key
    if contents:
      self.contents = [gme_item.Item(**x) for x in contents]
    else:
      self.contents = []
