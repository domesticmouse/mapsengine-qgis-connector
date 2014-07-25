"""Dialog to allow users to upload a dataset to Google Maps Engine.

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
import os
import shutil
import tempfile
import webbrowser
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QDialog
from qgis.core import QgsMessageLog
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsRasterPipe
from qgis.core import QgsRasterFileWriter
from qgis.core import QgsMapLayer
from qgis.gui import QgsMessageBar
import gme_api
import oauth2_utils
import settings
from upload_dialog_base import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
  """Dialog implementation class for the upload dialog."""

  def __init__(self, iface):
    """Constructor for the dialog.

    Args:
      iface: QgsInterface instance.
    """
    QDialog.__init__(self, iface.mainWindow())
    self.setupUi(self)
    self.iface = iface

    # Set defaults
    self.lineEditTags.setText('QGIS Desktop')

    # Initialize
    self.populateProjects()
    self.populateLayerSelection()

  def populateProjects(self):
    """Read project information and add it to comboBoxProjects widget."""
    self.projectDict = settings.read('gmeconnector/PROJECTS')
    self.comboBoxProjects.clear()
    for projectId, projectName in self.projectDict.iteritems():
      self.comboBoxProjects.addItem(projectName, projectId)

    defaultProjectId = settings.read('gmeconnector/DEFAULT_PROJECT')
    lastUsedProjectId = settings.read('gmeconnector/LAST_USED_PROJECT')
    # Check if the user has selected a default project
    if defaultProjectId in self.projectDict:
      currentProjectId = defaultProjectId
    elif lastUsedProjectId in self.projectDict:
      currentProjectId = lastUsedProjectId
    else:
      currentProjectId = self.projectDict.iterkeys().next()
    index = self.comboBoxProjects.findData(currentProjectId)
    self.comboBoxProjects.setCurrentIndex(index)

  def populateLayerSelection(self):
    """Read layer information and add it to dialog."""
    currentLayer = self.iface.mapCanvas().currentLayer()
    self.lineEditLayerName.setText(currentLayer.name())
    self.lineEditDestinationName.setText(currentLayer.name())
    self.lineEditLocalPath.setText(currentLayer.source())

    self.lineEditLayerName.setReadOnly(True)
    self.lineEditLocalPath.setReadOnly(True)

  def extractVectorLayer(self, tempDir):
    """Extract the features from the current layer to a temporary shapefile.

    Extracts a shapefile that can be uploaded to maps engine. This approach
    ensures that we are able to upload any layer that QGIS has ability to read,
    including CSV files, databases etc.

    Args:
      tempDir: str, path of directory where to extract the shapefile.
    Returns:
      a dictionary with file names as keys and file path as values or None
      if there is error.
    """
    layerName = unicode(self.lineEditLayerName.text())
    tempShpPath = os.path.join(tempDir, layerName + '.shp')

    outputCrs = QgsCoordinateReferenceSystem(
        4326, QgsCoordinateReferenceSystem.EpsgCrsId)
    currentLayer = self.iface.mapCanvas().currentLayer()
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector',
        'Extracting data to a temporary shapefile. Please wait...',
        level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()
    error = QgsVectorFileWriter.writeAsVectorFormat(
        currentLayer, tempShpPath, 'utf-8',
        outputCrs, 'ESRI Shapefile')

    if error != QgsVectorFileWriter.NoError:
      QgsMessageLog.logMessage(error, 'GMEConnector',
                               QgsMessageLog.CRITICAL)
      return

    filesToUpload = {}
    for ext in ('shp', 'shx', 'dbf', 'prj'):
      fileName = '%s.%s' % (layerName, ext)
      filePath = os.path.join(tempDir, fileName)
      filesToUpload[fileName] = filePath
    return filesToUpload

  def extractRasterLayer(self, tempDir):
    """Extract the raster from the current layer to a temporary GeoTiff file.

    Extracts a geotiff file that can be uploaded to maps engine. This approach
    ensures that we are able to upload any layer that QGIS has ability to read.

    Args:
      tempDir: str, path of directory where to extract the shapefile.
    Returns:
      a dictionary with file names as keys and file path as values.
    """
    layerName = unicode(self.lineEditLayerName.text())
    tempTifPath = os.path.join(tempDir, layerName + '.tif')

    currentLayer = self.iface.mapCanvas().currentLayer()
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector',
        'Extracting data to a temporary geotiff file. Please wait...',
        level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()

    pipe = QgsRasterPipe()
    provider = currentLayer.dataProvider()
    pipe.set(provider.clone())

    rasterWriter = QgsRasterFileWriter(tempTifPath)
    xSize = provider.xSize()
    ySize = provider.ySize()
    if xSize and ySize:
      error = rasterWriter.writeRaster(
          pipe, xSize, ySize, provider.extent(), provider.crs())
      if error != QgsRasterFileWriter.NoError:
        QgsMessageLog.logMessage(error, 'GMEConnector',
                                 QgsMessageLog.CRITICAL)
        return
    else:
      return

    filesToUpload = {}
    fileName = layerName + '.tif'
    filePath = os.path.join(tempDir, fileName)
    filesToUpload[fileName] = filePath
    return filesToUpload

  def accept(self):
    """Uploads the selected layer to maps engine."""
    self.close()
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector', 'Uploading data. Please wait...',
        level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()
    currentProject = self.comboBoxProjects.currentIndex()

    acl = unicode(self.lineEditAcl.text())
    tags = unicode(self.lineEditTags.text())

    # TODO: use with tempfile.TemporaryDirectory() instead of try/finally.
    tempDir = tempfile.mkdtemp()
    try:
      currentLayer = self.iface.mapCanvas().currentLayer()
      if currentLayer.type() == QgsMapLayer.VectorLayer:
        filesToUpload = self.extractVectorLayer(tempDir)
      elif currentLayer.type() == QgsMapLayer.RasterLayer:
        filesToUpload = self.extractRasterLayer(tempDir)
      else:
        QgsMessageLog.logMessage('Unsupported layer type.', 'GMEConnector',
                                 QgsMessageLog.CRITICAL)
        filesToUpload = []

      if not filesToUpload:
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', 'Extraction failed.',
            level=QgsMessageBar.CRITICAL, duration=3)
        QgsMessageLog.logMessage('Extraction failed', 'GMEConnector',
                                 QgsMessageLog.CRITICAL)
        return

      data = {}
      data['projectId'] = unicode(
          self.comboBoxProjects.itemData(currentProject))
      data['name'] = unicode(self.lineEditDestinationName.text())
      data['description'] = unicode(self.lineEditDescription.text())
      data['files'] = [{'filename': x} for x in filesToUpload]
      if acl:
        data['draftAccessList'] = acl
      if tags:
        data['tags'] = [unicode(x) for x in tags.split(',')]

      if currentLayer.type() == QgsMapLayer.VectorLayer:
        data_type = 'tables'
      elif currentLayer.type() == QgsMapLayer.RasterLayer:
        # attribution to be specified for raster layers only.
        data['attribution'] = unicode(self.lineEditAttribution.text())
        data_type = 'rasters'
      else:
        QgsMessageLog.logMessage('Unsupported layer type.', 'GMEConnector',
                                 QgsMessageLog.CRITICAL)

      token = oauth2_utils.getToken()
      api = gme_api.GoogleMapsEngineAPI(self.iface)
      assetId = api.postCreateAsset(data_type, data, token)
      if not assetId:
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', 'Upload failed.',
            level=QgsMessageBar.CRITICAL, duration=3)
        QgsMessageLog.logMessage('Upload failed', 'GMEConnector',
                                 QgsMessageLog.CRITICAL)
        return

      msg = 'Asset creation successful. Asset ID: %s' % assetId
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector', msg, level=QgsMessageBar.INFO)
      QgsMessageLog.logMessage(msg, 'GMEConnector', QgsMessageLog.INFO)
      for fileName in filesToUpload:
        msg = 'Uploading file %s' % filesToUpload[fileName]
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', msg, level=QgsMessageBar.INFO)
        QCoreApplication.processEvents()

        content = open(filesToUpload[fileName], 'rb').read()
        api.postUploadFile(assetId, data_type, fileName, content, token)

      self.iface.messageBar().clearWidgets()

      # Open the newly created asset in web browser
      url = ('https://mapsengine.google.com/admin/'
             '#RepositoryPlace:cid=%s&'
             'v=DETAIL_INFO&aid=%s')
      # The assetId returned by the API in a globally unique id of the form
      # 'project_id-asset_id'. Split the assetId to get the project_id
      # parameter (cid) in the url.
      gmeUrl = url % (assetId.split('-')[0], assetId)
      webbrowser.open(gmeUrl)
    finally:
      # Cleanup
      shutil.rmtree(tempDir)
