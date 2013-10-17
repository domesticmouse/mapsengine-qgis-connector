"""Utility methods for OAuth2.

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
import json
import urllib
import urllib2
from qgis.core import QgsMessageLog
from oauth2_token import OAuth2Token
import settings

OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
OAUTH2_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
OAUTH2_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
OAUTH2_REVOKE_URL = 'https://accounts.google.com/o/oauth2/revoke'
OAUTH2_TOKENINFO_URL = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
OAUTH2_AUTH_SCOPES = ('https://www.googleapis.com/auth/mapsengine '
                      'https://www.googleapis.com/auth/userinfo.profile')


def getToken():
  """Read the token parameters from settings and return a token object.

  Returns:
    OAuth2Token instance is succcessful, None if the token is not available.
  """
  token = OAuth2Token()
  token.access_token = settings.read('gmeconnector/ACCESS_TOKEN', object_type=str)
  token.refresh_token = settings.read('gmeconnector/REFRESH_TOKEN', object_type=str)
  token.expires_at = settings.read('gmeconnector/EXPIRES_AT', object_type=str)

  if token.access_token and token.refresh_token and token.expires_at:
    if isTokenValid(token):
      return token
    else:
      return refreshToken(token)
  else:
    return None


def setToken(token):
  """Write the token parameters to settings."""
  settings.write('gmeconnector/ACCESS_TOKEN', token.access_token)
  settings.write('gmeconnector/REFRESH_TOKEN', token.refresh_token)
  settings.write('gmeconnector/EXPIRES_AT', token.expires_at)


def isTokenValid(token):
  """Check if the given token is valid.

  Returns:
    True if the token is valid.
  """
  baseUrl = OAUTH2_TOKENINFO_URL
  params = {'access_token': token.access_token}
  tokenInfoUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))
  req = urllib2.Request(tokenInfoUrl)
  # Make a GET request
  response = makeHttpRequest(req)
  if response:
    response = urllib2.urlopen(req)
    results = json.load(response)
    if results['audience'] == settings.read('gmeconnector/CLIENT_ID'):
      return True
    else:
      return False
  else:
    return False


def revokeToken():
  """Revoke the token from the server."""
  token = getToken()
  if token:
    baseUrl = OAUTH2_REVOKE_URL
    params = {'token': token.access_token}
    revokeUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))
    # Make a GET request
    req = urllib2.Request(revokeUrl)
    makeHttpRequest(req)


def getUserName(token):
  """Query user profile information to get user name.

  Args:
    token: OAuth2Token instance
  Returns:
    str, user name
  """
  baseUrl = OAUTH2_USERINFO_URL
  params = {'access_token': token.access_token}
  userInfoUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))
  # Make a GET request
  req = urllib2.Request(userInfoUrl)
  response = makeHttpRequest(req)
  if response:
    results = json.load(response)
    if results.has_key('name'):
      return results['name']
  return ''


def tradeCodeForToken(code):
  """Exchange authorization code to obtain a token.

  Args:
    code: str, authorization code
  Returns:
    OAuth2Token instance if successful, None if failed.
  """

  tokenUrl = OAUTH2_TOKEN_URL
  params = {'code': code,
            'client_id': settings.read('gmeconnector/CLIENT_ID'),
            'client_secret': settings.read('gmeconnector/CLIENT_SECRET'),
            'redirect_uri': OAUTH2_REDIRECT_URI,
            'grant_type': 'authorization_code'}
  # Make a POST request
  req = urllib2.Request(tokenUrl, urllib.urlencode(params))
  req.add_header('Content-Type', 'application/x-www-form-urlencoded')
  response = makeHttpRequest(req)
  if response:
    results = json.load(response)
    token = OAuth2Token(**results)
    return token
  else:
    return None


def tradeRefreshForToken(refresh_token):
  """Gets a new token using refresh token.

  Args:
    refresh_token: str, refresh token.
  Returns:
    OAuth2Token instance if successful, None if failed.
  """
  tokenUrl = OAUTH2_TOKEN_URL
  params = {'refresh_token': refresh_token,
            'client_id': settings.read('gmeconnector/CLIENT_ID'),
            'client_secret': settings.read('gmeconnector/CLIENT_SECRET'),
            'grant_type': 'refresh_token'}
  # Make a POST request
  req = urllib2.Request(tokenUrl, urllib.urlencode(params))
  req.add_header('Content-Type', 'application/x-www-form-urlencoded')
  response = makeHttpRequest(req)
  if response:
    results = json.load(response)
    token = OAuth2Token(**results)
    # Refresh requests do not come back with refresh_token.
    # Set it to the value of the current refresh_token.
    token.refresh_token = refresh_token
    return token
  else:
    return None


def refreshToken(token):
  """Refreshes the given token.

  Args:
    token: OAuth2Token instance
  Returns:
    a new OAuth2Token instance if successful, None if failed.
  """
  refresh_token = token.refresh_token
  if refresh_token:
    token = tradeRefreshForToken(refresh_token)
    if token:
      setToken(token)
      return token
    else:
      return None


def decodeTitleResponse(title):
  """Parses the title and returns a token if title contains Success.

  Args:
    title: str, title of the page.
  Returns:
    OAuth2Token instance if successful, None if failed.
  """
  if title.startswith('Success'):
    startindex = title.find('code=') + 5
    code = title[startindex:]
    return tradeCodeForToken(code)
  else:
    return None


def buildAuthenticationUri():
  """Creates a URL for authentication.

  Returns;
    str, authentication url.
  """
  baseUrl = OAUTH2_AUTH_URL
  params = {'response_type': 'code',
            'client_id': settings.read('gmeconnector/CLIENT_ID'),
            'scope': OAUTH2_AUTH_SCOPES,
            'state': '123456789',
            'approval_prompt': 'auto',
            'redirect_uri': OAUTH2_REDIRECT_URI}
  authUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))
  return authUrl


def makeHttpRequest(request):
  """Make a http request.

  Args:
    request: urllib2.Request
  Returns:
    server response if successful, None if failed.
  """
  retries = 2
  # Make the request
  while retries > 0:
    try:
      response = urllib2.urlopen(request)
      return response
    except (urllib2.HTTPError, urllib2.URLError) as e:
      errorMsg = 'Error while fetching %s: %s' % (request.get_full_url(), e)
      QgsMessageLog.logMessage(
          errorMsg, 'GMEConnector', QgsMessageLog.CRITICAL)
      retries -= 1
  return None
