"""Dialog to load a Google Maps Engine map via WMS.

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
import oauth2_utils
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from qgis.core import QgsDataSourceURI
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsMessageLog
from qgis.core import QgsRasterLayer
from qgis.gui import QgsMessageBar
import settings
from wms_dialog_base import Ui_Dialog
# OWSLib is part of the default package from QGIS 2.4
# Older versions of QGIS may not have it installed.
try:
  from owslib.wms import WebMapService
  owslib_available = True
except ImportError:
  QgsMessageLog.logMessage('OWSLib not available',
                           'GMEConnector',
                           QgsMessageLog.INFO)
  owslib_available = False

# Vector and Raster layers can be displayed in different CRS
# TODO: Use crsOptions from OWSLib to populate this from GetCapabilities.
CRS_DICT = {'table': ('EPSG:3857', 'EPSG:3785', 'EPSG:900913'),
            'image': ('EPSG:4326', 'EPSG:3857', 'EPSG:3785', 'EPSG:900913'),
            'baselayer': ('EPSG:3857', 'EPSG:3785', 'EPSG:900913'),
            'unknown': ('EPSG:4326', 'EPSG:3857', 'EPSG:3785', 'EPSG:900913')}


class Dialog(QDialog, Ui_Dialog):
  """Dialog implementation class for the WMS dialog."""

  def __init__(self, iface):
    """Constructor for the dialog.

    Args:
      iface: QgsInterface instance.
    """
    QDialog.__init__(self, iface.mainWindow())
    self.setupUi(self)
    self.iface = iface
    self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
    self.okButton.setText('Add Selected to Map')
    self.comboBoxLayer.activated.connect(self.loadCrsForIndex)
    self.comboBoxLayer.activated.connect(self.loadFormatForIndex)
    self.comboBoxFormat.addItem('JPEG', 'image/jpeg')
    self.comboBoxFormat.addItem('PNG', 'image/png')

  def getLayers(self, folders):
    """Fetches layers from the given folders.

    Args:
      folders: list, of gme_folder.Folder objects.
    Returns:
      list of gme_item.Item objects.
    """
    layers = []
    for folder in folders:
      new_layers = [x for x in folder.contents if x.type == 'layer']
      layers.extend(new_layers)
      # Recursive call to populate folders within the current folder
      folders = [x for x in folder.contents if x.type == 'folder']
      if folders:
        layers.extend(self.getLayers(folders))
    return layers

  def loadFormatForIndex(self, index):
    """Loads WMS overlay format for the given index.

    Args:
      index: int, index of the comboBoxCrs widget.
    """
    unused_layerId, dataType = self.comboBoxLayer.itemData(index)
    if dataType == 'image':
      # Raster overlay default format is JPEG.
      self.comboBoxFormat.setCurrentIndex(self.comboBoxFormat.findText('JPEG'))
      defaultFormat = settings.read('gmeconnector/WMS_RASTER_FORMAT')
      if defaultFormat:
        defaultIndex = self.comboBoxFormat.findText(defaultFormat)
        if defaultIndex != -1:
          self.comboBoxFormat.setCurrentIndex(defaultIndex)
    elif dataType == 'table':
      # Vector overlay default format is PNG.
      self.comboBoxFormat.setCurrentIndex(self.comboBoxFormat.findText('PNG'))
      defaultFormat = settings.read('gmeconnector/WMS_VECTOR_FORMAT')
      if defaultFormat:
        defaultIndex = self.comboBoxFormat.findText(defaultFormat)
        if defaultIndex != -1:
          self.comboBoxFormat.setCurrentIndex(defaultIndex)
    else:
      # Set default format as PNG.
      self.comboBoxFormat.setCurrentIndex(self.comboBoxFormat.findText('PNG'))

  def loadCrsForIndex(self, index):
    """Loads compatible CRSs for the given index.

    Args:
      index: int, index of the comboBoxCrs widget.
    """
    self.comboBoxCrs.clear()
    unused_layerId, dataType = self.comboBoxLayer.itemData(index)
    if dataType:
      for crs in CRS_DICT[dataType]:
        self.comboBoxCrs.addItem(crs)

  def populateLayersOWS(self, gmeMap):
    """Adds layer information to comboBoxLayer widget using OWSLib.

    Args:
      gmeMap: gme_map.Map object.
    """
    self.labelMapName.setText(gmeMap.name)
    self.labelMapId.setText(gmeMap.id)
    self.comboBoxLayer.clear()
    mapId = gmeMap.id
    # Create the WMS layer
    token = oauth2_utils.getToken()
    url = 'https://mapsengine.google.com/%s-4/wms/%s/'
    wmsUrl = url % (mapId, token.access_token)
    wms = WebMapService(wmsUrl)
    for layer in list(wms.contents):
      if wms[layer].abstract == 'Raster layer':
        dataType = 'image'
      elif wms[layer].abstract == 'Vector layer':
        dataType = 'table'
      elif wms[layer].abstract == 'Base layer':
        dataType = 'baselayer'
      else:
        dataType = 'unknown'

      userData = (layer, dataType)
      if dataType != 'unknown':
        self.comboBoxLayer.addItem(wms[layer].title, userData)

  def populateLayers(self, gmeMap, gmeLayers):
    """Adds layer information to comboBoxLayer widget.

    Args:
      gmeMap: gme_map.Map object.
      gmeLayers: list, of gme_layer.Layer objects.
    """
    if owslib_available:
      self.populateLayersOWS(gmeMap)
    else:
      self.labelMapName.setText(gmeMap.name)
      self.labelMapId.setText(gmeMap.id)
      self.comboBoxLayer.clear()
      for gmeLayer in gmeLayers:
        userData = (gmeLayer.id + '-4', gmeLayer.datasourceType)
        self.comboBoxLayer.addItem(gmeLayer.name, userData)

  def accept(self):
    """Creates and loads the WMS layer."""
    self.close()
    currentIndex = self.comboBoxLayer.currentIndex()
    currentLayerId, unused_dataType = self.comboBoxLayer.itemData(currentIndex)
    currentLayerName = unicode(self.comboBoxLayer.currentText())
    mapId = self.labelMapId.text()
    # Create the WMS layer
    token = oauth2_utils.getToken()
    url = 'https://mapsengine.google.com/%s-4/wms/%s/'
    wmsUrl = url % (mapId, token.access_token)
    currentFormatIndex = self.comboBoxFormat.currentIndex()
    imageFormat = unicode(self.comboBoxFormat.itemData(currentFormatIndex))
    crs = self.comboBoxCrs.currentText()

    uri = QgsDataSourceURI()
    uri.setParam('url', wmsUrl)
    uri.setParam('layers', currentLayerId)
    uri.setParam('format', imageFormat)
    uri.setParam('crs', crs)
    uri.setParam('styles', '')

    rlayer = QgsRasterLayer(str(uri.encodedUri()), currentLayerName, 'wms')
    if rlayer.isValid():
      QgsMapLayerRegistry.instance().addMapLayer(rlayer)
    else:
      logText = 'Failed to add WMS layer %s with URI %s' % (
          currentLayerName, str(uri.encodedUri()))
      warnText = 'Failed to add WMS layer %s' % currentLayerName
      QgsMessageLog.logMessage(logText, 'GMEConnector', QgsMessageLog.CRITICAL)
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector', warnText,
          level=QgsMessageBar.CRITICAL, duration=3)
