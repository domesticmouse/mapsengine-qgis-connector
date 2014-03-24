"""Google Maps Engine Connector for QGIS.

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
import webbrowser
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QMessageBox
from qgis.gui import QgsMessageBar
from plugin import more_dialog
from plugin import oauth2_utils
from plugin import search_gme_dialog
from plugin import settings
from plugin import signin_dialog
from plugin import upload_dialog
from plugin import wms_dialog
from plugin.datamodel import gme_layer
from plugin.datamodel import gme_map
# Initialize Qt resources
import resources_rc


class GoogleMapsEngineConnector:
  """The QGIS interface implementation for the plugin."""

  def __init__(self, iface):
    """Class constructor.

    Args:
      iface: QgsInterface instance.
    """
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    """Gui initialization procedure (for QGIS plugin api)."""
    # Create action for sign-in icon
    self.signIn = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/private-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Sign in or out of your Google Maps Engine account'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.signIn)
    # Set initial state
    self.signIn.setCheckable(True)
    self.signIn.setChecked(False)
    self.signIn.toggled.connect(self.doSignInOrOut)
    self.token = None

    # Create action for search in GME icon
    self.searchGme = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/search-16.png'),
        QCoreApplication.translate(
            'GMEConnector', 'Search for a Google Maps Engine asset'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.searchGme)
    self.searchGme.setEnabled(False)
    self.searchGme.triggered.connect(self.doSearchGme)

    # Create action for search in gallery icon
    self.searchGallery = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/gallery-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Search for a Google Maps Engine map in Google Earth Gallery'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector',
                               self.searchGallery)
    self.searchGallery.setEnabled(False)
    self.searchGallery.triggered.connect(self.doOpenGallery)

    # Create action for WMS overlay icon
    self.addWms = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/overlay-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Add your selected Google Maps Engine service to your map'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.addWms)
    self.addWms.setEnabled(False)
    self.addWms.triggered.connect(self.doAddWms)

    # Create action for view in GME icon
    self.viewInGme = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/maps_engine-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Open selected Google Maps Engine service in '
            'Google Maps Engine UI'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.viewInGme)
    self.viewInGme.setEnabled(False)
    self.viewInGme.triggered.connect(self.doViewInMapsEngine)

    # Create action for view in Google Maps icon
    self.viewInGoogleMaps = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/maps-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Open selected Google Maps Engine service in Google Maps'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu(
        '&Google Maps Engine Connector', self.viewInGoogleMaps)
    self.viewInGoogleMaps.setEnabled(False)
    self.viewInGoogleMaps.triggered.connect(self.doViewInGoogleMaps)

    # Create action for share secure link icon
    self.shareSecureLink = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/link-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Generate a hyperlink to share the selected '
            'Google Maps Engine service'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu(
        '&Google Maps Engine Connector', self.shareSecureLink)
    self.shareSecureLink.setEnabled(False)
    self.shareSecureLink.triggered.connect(self.doShareSecureLink)

    # Create action for upload icon
    self.upload = QAction(
        QIcon(':/plugins/googlemapsengineconnector/images/upload_item-16.png'),
        QCoreApplication.translate(
            'GMEConnector',
            'Upload selected data to your Google Maps Engine account'),
        self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.upload)
    self.upload.setEnabled(False)
    self.upload.triggered.connect(self.doUpload)

    # Create action for More text
    self.showMore = QAction(QIcon(),
                            QCoreApplication.translate('GMEConnector', 'More'),
                            self.iface.mainWindow())
    self.iface.addPluginToMenu('&Google Maps Engine Connector', self.showMore)
    self.showMore.setEnabled(True)
    self.showMore.triggered.connect(self.doShowMore)

    # Create the toolbar
    self.toolBar = self.iface.addToolBar(
        QCoreApplication.translate('GMEConnector',
                                   'Google Maps Engine Connector'))
    self.toolBar.setObjectName(
        QCoreApplication.translate('GMEConnector',
                                   'Google Maps Engine Connector'))

    # Create labels for the toolbar
    self.searchlabel = QLabel(
        QCoreApplication.translate('GMEConnector', 'Find'))
    self.viewlabel = QLabel(QCoreApplication.translate('GMEConnector', 'View'))
    self.interactlabel = QLabel(QCoreApplication.translate(
        'GMEConnector', 'Interact'))

    # Add toolbar buttons and labels
    self.toolBar.addAction(self.signIn)
    self.toolBar.addSeparator()
    self.toolBar.addWidget(self.searchlabel)
    self.toolBar.addAction(self.searchGme)
    self.toolBar.addAction(self.searchGallery)
    self.toolBar.addSeparator()
    self.toolBar.addWidget(self.viewlabel)
    self.toolBar.addAction(self.addWms)
    self.toolBar.addAction(self.viewInGme)
    self.toolBar.addAction(self.viewInGoogleMaps)
    self.toolBar.addAction(self.shareSecureLink)
    self.toolBar.addSeparator()
    self.toolBar.addWidget(self.interactlabel)
    self.toolBar.addAction(self.upload)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.showMore)

    # Hook up a slot when selection is changed
    self.iface.mapCanvas().selectionChanged.connect(self.handleSelectionChange)
    self.iface.mapCanvas().layersChanged.connect(self.handleSelectionChange)
    self.iface.currentLayerChanged.connect(self.handleSelectionChange)
    self.iface.legendInterface().itemRemoved.connect(self.handleSelectionChange)

    # Hook up slots for signals from the sign-in dialog.
    self.signInDlg = signin_dialog.Dialog(self.iface)
    self.signInDlg.authStateChange.connect(self.handleAuthChange)

  def unload(self):
    """Unloads the plugin and cleans up the GUI."""
    # Remove the plugin menu items
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.signIn)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.searchGme)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.searchGallery)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.addWms)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.viewInGme)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.viewInGoogleMaps)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.shareSecureLink)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.upload)
    self.iface.removePluginMenu('&Google Maps Engine Connector',
                                self.showMore)

    # Remove the toolbar
    del self.toolBar

    # Revoke the token on exit
    oauth2_utils.revokeToken()
    # Remove the access credientials from settings
    settings.clear()

  def handleAuthChange(self, success, token, userName):
    """Enable or disable tools in response to an authStateChange event.

    Args:
      success: bool, True if authentication was successful.
      token: OAuth2Token object, authentication token.
      userName: str, name of the user who has logged-in.
    """
    if success:
      self.token = token
      if userName:
        signInText = 'Logged in as %s.' % userName
      else:
        signInText = 'Logged in.'
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector', signInText,
          level=QgsMessageBar.INFO, duration=3)
      self.signIn.setText(signInText)
      self.searchGme.setEnabled(True)
      self.searchGallery.setEnabled(True)
      self.signIn.setChecked(True)
      self.handleSelectionChange()
    else:
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector',
          'Authentication failed. Please try again.',
          level=QgsMessageBar.CRITICAL, duration=3)
      self.signIn.setChecked(False)
      self.disableAllTools()

  def handleSelectionChange(self):
    """Enables or disables tools in response to changes in selection."""
    # Disable all the tools first.
    # We will enable them one by one if certain criteria are met.
    self.upload.setEnabled(False)
    self.viewInGoogleMaps.setEnabled(False)
    self.viewInGme.setEnabled(False)
    self.addWms.setEnabled(False)
    self.shareSecureLink.setEnabled(False)

    currentLayer = self.iface.mapCanvas().currentLayer()

    # If a layer is selected and is of type vector or raster
    if currentLayer and (currentLayer.type() in (0, 1)):
      gmeMap, gmeLayers = self.getAssetsFromLayer(currentLayer)
      # If a map is available
      if gmeMap and self.token:
        self.viewInGoogleMaps.setEnabled(True)
        self.viewInGme.setEnabled(True)
        self.addWms.setEnabled(True)
        self.shareSecureLink.setEnabled(True)
      # If no map is available, but layers are available
      elif gmeLayers and self.token:
        self.viewInGme.setEnabled(True)

      # If the currently selected layer is a vector or raster layer
      if (currentLayer.type() in (0, 1) and
          not self.isGmeConnectorLayer(currentLayer)
          and self.token):
        self.upload.setEnabled(True)

  def isGmeConnectorLayer(self, layer):
    """Check if the given layer was created by Google Maps Engine Connector.

    The layers created by the tools are temporary vector layers using the
    memory provider and contain an attribute 'Resource Type'.

    Args:
      layer: QgsMapLayer
    Returns:
      True if the layer was created by Google Maps Engine Connector.
    """
    provider = layer.dataProvider()
    if provider.name() == 'memory' and layer.type() == 0:
      if layer.dataProvider().fieldNameIndex('Resource Type') != -1:
        return True
    return False

  def getFeatures(self, layer, selected=True):
    """Return the features from the given layer.

    Args:
      layer: QgsVectorLayer
      selected: Return only the selected features from the layer
    Returns:
      The features for the given layer.  Returns all the features from the
      layer if selected=False else returns only the selected features (default).
    """
    if selected:
      return iter(layer.selectedFeatures())
    else:
      return layer.getFeatures()

  def getAssetsFromLayer(self, layer, selected_only=True):
    """Creates Google Maps Engine assets from vector layer.

    Args:
      layer: QgsMapLayer
      selected_only: bool, True if only selected feature are used.
    Returns:
      gme_map.Map and a list of gme_layer.Layer objects
    """
    gmeMap = None
    gmeLayers = []

    if not self.isGmeConnectorLayer(layer):
      return gmeMap, gmeLayers

    for feature in self.getFeatures(layer, selected_only):
      resourceType = feature['Resource Type']
      name = feature['Resource Name']
      resourceId = feature['Resource Identifier']

      if resourceType == 'map':
        gmeMap = gme_map.Map(id=resourceId, name=name)
      elif resourceType == 'layer':
        layerDataSource = feature['Data Source Type']
        gmeLayer = gme_layer.Layer(id=resourceId, name=name,
                                   datasourceType=layerDataSource)
        gmeLayers.append(gmeLayer)
    return gmeMap, gmeLayers

  def doSignInOrOut(self, checked):
    """Show the sign-in dialog and manage authentication status.

    Args:
      checked: bool, whether the sign-in action was checked.
    """
    if checked:
      # check if client_id and client_secret exist
      client_id = settings.read('gmeconnector/CLIENT_ID')
      client_secret = settings.read('gmeconnector/CLIENT_SECRET')
      if client_id and client_secret:
        token = oauth2_utils.getToken()
        if token:
          self.token = token
          self.handleAuthChange(True, token, '')
        else:
          # The sign-in dialog is initialized when the plugin is loaded.
          # We need to have setInitialUrl outside the dialog constructor to make
          # sure it's called everytime the sign-in button is clicked.
          self.signInDlg.setInitialUrl()
          result = self.signInDlg.exec_()
          if not result:
            self.handleAuthChange(False, None, '')
      else:
        self.signIn.setChecked(False)
        warnText = ('You must enter valid OAuth2.0 Client ID '
                    'and Client secret in Advanced Settings.')
        QMessageBox.warning(self.iface.mainWindow(), 'Warning', warnText)
        self.doShowMore()
    else:
      self.token = None
      self.signIn.setText('Logged out. Click to log in.')
      self.signIn.setChecked(False)
      self.disableAllTools()
      # Revoke the token
      oauth2_utils.revokeToken()
      # Remove the access credientials from settings
      settings.clear()

  def doSearchGme(self):
    """Show the search dialog."""
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector', 'Fetching maps. Please wait...',
        level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()
    searchGmeDialog = search_gme_dialog.Dialog(self.iface)
    searchGmeDialog.exec_()

  def doAddWms(self):
    """Show the WMS dialog."""
    currentLayer = self.iface.mapCanvas().currentLayer()
    gmeMap, gmeLayers = self.getAssetsFromLayer(
        currentLayer, selected_only=False)
    self.wmsDialog = wms_dialog.Dialog(self.iface)
    self.wmsDialog.populateLayers(gmeMap, gmeLayers)
    self.wmsDialog.loadCrsForIndex(0)
    self.wmsDialog.loadFormatForIndex(0)
    self.wmsDialog.exec_()

  def doShareSecureLink(self):
    """Copy the WMS link to clipboard."""
    currentLayer = self.iface.mapCanvas().currentLayer()
    gmeMap, unused_gmeLayers = self.getAssetsFromLayer(currentLayer)
    selectedMapId = gmeMap.id
    access_token = self.token.access_token

    url = 'https://mapsengine.google.com/%s-4/wms/%s/'
    wmsUrl = url % (selectedMapId, access_token)
    clipboard = QApplication.clipboard()
    clipboard.setText(wmsUrl)
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector',
        'Copied WMS service url to clipboard.',
        level=QgsMessageBar.INFO, duration=3)

  def doViewInMapsEngine(self):
    """Open the maps engine asset view page in a browser."""
    currentLayer = self.iface.mapCanvas().currentLayer()
    gmeMap, gmeLayers = self.getAssetsFromLayer(currentLayer)
    if gmeMap:
      mapId = gmeMap.id
      url = ('https://mapsengine.google.com/admin/'
             '?pli=1#MapCreationPlace:cid=%s&'
             'v=MAP_CREATION&'
             'aid=%s')
      gmeUrl = url % (mapId.split('-')[0], mapId)
      webbrowser.open(gmeUrl)
    if gmeLayers:
      for gmeLayer in gmeLayers:
        layerId = gmeLayer.id
        url = ('https://mapsengine.google.com/admin/'
               '?pli=1#LayersPlace:cid=%s&'
               'v=DETAIL_INFO&'
               'aid=%s')
        gmeUrl = url % (layerId.split('-')[0], layerId)
        webbrowser.open(gmeUrl)

  def doOpenGallery(self):
    """Open the Google Earth Gallery in a browser."""
    url = 'http://www.google.com/gadgets/directory?synd=earth'
    webbrowser.open(url)

  def doViewInGoogleMaps(self):
    """Open the selected map in Google Maps viewer."""
    token = oauth2_utils.getToken()
    url = ('https://mapsengine.google.com/'
           '%s-4/mapview/?'
           'access_token=%s')
    currentLayer = self.iface.mapCanvas().currentLayer()
    gmeMap, unused_gmeLayers = self.getAssetsFromLayer(currentLayer)
    mapId = gmeMap.id
    gmapUrl = url % (mapId, token.access_token)
    webbrowser.open(gmapUrl)

  def doShowMore(self):
    """Show the more dialog."""
    # Trigger the login dialog if we detect a change to client_id or
    # client_secret.
    pre_client_id = settings.read('gmeconnector/CLIENT_ID')
    pre_client_secret = settings.read('gmeconnector/CLIENT_SECRET')
    self.moreDialog = more_dialog.Dialog(self.iface)
    if self.token:
      self.moreDialog.groupBoxAccount.setEnabled(True)
      self.moreDialog.populateProjects()
    else:
      self.moreDialog.groupBoxAccount.setEnabled(False)
    self.moreDialog.exec_()
    # Read the client_id and client_secret again to compare.
    post_client_id = settings.read('gmeconnector/CLIENT_ID')
    post_client_secret = settings.read('gmeconnector/CLIENT_SECRET')

    # If both client_id and client_secret are not empty and if either one has
    # changed, trigger the sign-in dialog.
    if (post_client_id and post_client_secret and
        (post_client_id != pre_client_id or
         post_client_secret != pre_client_secret)):
      self.signInDlg.setInitialUrl()
      result = self.signInDlg.exec_()
      if not result:
        self.handleAuthChange(False, None, '')

  def doUpload(self):
    """Show the upload dialog."""
    self.uploadDialog = upload_dialog.Dialog(self.iface)
    self.uploadDialog.exec_()

  def disableAllTools(self):
    """Diable all the tools."""
    self.searchGme.setEnabled(False)
    self.searchGallery.setEnabled(False)
    self.viewInGme.setEnabled(False)
    self.viewInGoogleMaps.setEnabled(False)
    self.addWms.setEnabled(False)
    self.shareSecureLink.setEnabled(False)
    self.upload.setEnabled(False)
