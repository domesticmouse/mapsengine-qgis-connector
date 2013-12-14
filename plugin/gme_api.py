"""Class for using the Google Maps Engine API from QGIS.

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
from qgis.gui import QgsMessageBar
from datamodel import gme_layer
from datamodel import gme_map
from datamodel import gme_maplist

GME_API_VERSION = 'v1'
GME_API_BASE_URI = 'https://www.googleapis.com/mapsengine'
GME_API_UPLOAD_URI = 'https://www.googleapis.com/upload/mapsengine'


class GoogleMapsEngineAPI(object):
  """QGIS wrapper for the Google Maps Engine API."""

  def __init__(self, iface):
    """Class constructor.

    Args:
      iface: QgsInterface instance.
    """
    # Save the reference to iface to we can send messages to the QgsMessageBar
    self.iface = iface

  def makeGoogleMapsEngineRequest(self, requestUrl, access_token, data=None,
                                  content_type=None):
    """Make a http request and fetch data from the requested url.

    Args:
      requestUrl: str, url to send the request.
      access_token: str, oauth2 access token.
      data: str, data to send with the request.
      content_type: str, the MIME type of the request.
    Returns:
      server response if successful, None if failed
    """

    if data:
      req = urllib2.Request(str(requestUrl), data=data)
    else:
      req = urllib2.Request(str(requestUrl), data=None)

    # Add header
    req.add_header('Authorization', 'Bearer %s' % access_token)
    if not content_type:
      req.add_header('Content-Type', 'application/json')
    else:
      req.add_header('Content-Type', 'application/octet-stream')
      req.add_header('Content-Length', len(data))

    retries = 2
    # Make the request
    while retries > 0:
      try:
        response = urllib2.urlopen(req)
        return response
      except (urllib2.HTTPError, urllib2.URLError) as e:
        errorMsg = 'Error while fetching %s: %s' % (requestUrl, e)
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', errorMsg,
            level=QgsMessageBar.CRITICAL, duration=3)
        QgsMessageLog.logMessage(
            errorMsg, 'GMEConnector', QgsMessageLog.CRITICAL)
        retries -= 1
    return None

  def getProjects(self, token):
    """Get all projects readable by the user.

    Args:
      token: OAuth2Token object, authentication token.
    Returns:
      decoded response if successful, None if failed.
    """
    requestUrl = '%s/%s/%s' % (GME_API_BASE_URI, GME_API_VERSION, 'projects')
    results = self.makeGoogleMapsEngineRequest(requestUrl, token.access_token)
    if results:
      return json.load(results)
    else:
      return None

  def getMapsByProjectId(self, projectId, token, nextPageToken=None):
    """Get all maps readable by the user for the given project.

    Args:
      projectId: str, id of the maps engine project.
      token: OAuth2Token object, authentication token.
      nextPageToken: str, next page token.
    Returns:
      decoded response if successful, None if failed.
    """
    baseUrl = '%s/%s/%s' % (GME_API_BASE_URI, GME_API_VERSION, 'maps')
    params = {'projectId': projectId}
    if nextPageToken:
      params['pageToken'] = nextPageToken
    requestUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))
    results = self.makeGoogleMapsEngineRequest(requestUrl, token.access_token)
    maps = []
    if results:
      mapList = gme_maplist.MapList(**json.load(results))
      maps.extend(mapList.maps)
      if mapList.nextPageToken:
        # recursive fetch to get maps in subsequent pages
        maps.extend(
            self.getMapsByProjectId(projectId, token, mapList.nextPageToken))

    return maps

  def getMapById(self, mapId, token):
    """Get a map object for a particular map.

    Args:
      mapId: str, the id of the map.
      token: OAuth2Token object, authentication token.
    Returns:
      gme_map.Map object if successful, None if failed.
    """
    requestUrl = '%s/%s/%s/%s' % (GME_API_BASE_URI, GME_API_VERSION,
                                  'maps', mapId)
    results = self.makeGoogleMapsEngineRequest(requestUrl, token.access_token)
    if results:
      gmeMap = gme_map.Map(**json.load(results))
      return gmeMap
    else:
      return None

  def getLayerById(self, layerId, token):
    """Get a layer object for a particular layer.

    Args:
      layerId: str, the id of the layer.
      token: OAuth2Token object, authentication token.
    Returns:
      gme_layer.Layer object if successful, None if failed.
    """
    requestUrl = '%s/%s/%s/%s' % (GME_API_BASE_URI, GME_API_VERSION,
                                  'layers', layerId)
    results = self.makeGoogleMapsEngineRequest(requestUrl, token.access_token)
    if results:
      gmeLayer = gme_layer.Layer(**json.load(results))
      return gmeLayer
    else:
      return None

  def postCreateAsset(self, data_type, data, token):
    """Create a maps engine asset.

    Args:
      data_type: str, type of asset to create, either 'tables' or 'rasters'.
      data: dict, data to send with the request.
      token: OAuth2Token object, authentication token.
    Returns:
      asset id of the newly created asset if successful, None if failed.
    """
    if data_type not in ['tables', 'rasters']:
      errorMsg = 'Unsupported data type %s.' % data_type
      QgsMessageLog.logMessage(
          errorMsg, 'GMEConnector', QgsMessageLog.CRITICAL)
      return

    requestUrl = '%s/%s/%s/%s' % (GME_API_BASE_URI, GME_API_VERSION,
                               data_type, 'upload')
    results = self.makeGoogleMapsEngineRequest(
        requestUrl, token.access_token, data=json.dumps(data))
    if results:
      assetCreationResponse = json.load(results)
      if assetCreationResponse.has_key('id'):
        return assetCreationResponse['id']
      else:
        return None
    else:
      return None

  def postUploadFile(self, assetId, data_type, fileName, content, token):
    """Upload the given file to maps engine.

    Args:
      assetId: str, id of the maps engine asset.
      data_type: str, type of file to upload, either 'tables' or 'rasters'.
      fileName: str, name of the file to upload.
      content: str, content of the file to be uploaded.
      token: OAuth2Token object, authentication token.
    Returns:
      response from the server.
    """
    baseUrl = '%s/%s/%s/%s/files' % (GME_API_UPLOAD_URI, GME_API_VERSION,
                                  data_type, assetId)
    params = {'filename': fileName}
    requestUrl = '%s?%s' % (baseUrl, urllib.urlencode(params))

    results = self.makeGoogleMapsEngineRequest(
        requestUrl, token.access_token, data=content,
        content_type='application/octet-stream')
    return results
