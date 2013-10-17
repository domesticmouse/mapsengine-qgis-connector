"""Class to create a python token object from JSON.

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
from datetime import datetime, timedelta


class OAuth2Token(object):
  def __init__(self, access_token=None, refresh_token=None,
               expires_in=None, expires_at=None, **kwargs):
    self.access_token = access_token
    self.refresh_token = refresh_token
    self.expires_in = expires_in
    if self.expires_in:
      now = datetime.now()
      self.expires_at = str(now + timedelta(seconds=self.expires_in))
