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
from qgis.core import QgsMessageLog, QgsVectorFileWriter, QgsCoordinateReferenceSystem
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
    self.lineEditAcl.setText('Map Editors')
    self.lineEditEncoding.setText('UTF-8')
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

  def getNonGmeLayersFromCanvas(self):
    """Fetch only layers which are not created by this plugin."""
    validLayers = []
    layers = self.iface.mapCanvas().layers()
    for layer in layers:
      # Check that the type is VectorLayer
      if layer.type() == 0:
        # Ensure that the layer does not have a field called 'Resource Type'
        # as we are looking only for layers not created by this plugin.
        if layer.dataProvider().fieldNameIndex('Resource Type') == -1:
          validLayers.append(layer)

    return validLayers

  def accept(self):
    """Uploads the selected layer to maps engine."""
    self.close()
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector', 'Uploading data. Please wait...',
        level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()
    currentProject = self.comboBoxProjects.currentIndex()
    projectId = unicode(
        self.comboBoxProjects.itemData(currentProject))

    currentLayer = self.lineEditLayerName.text()
    layerName = unicode(self.lineEditLayerName.text())

    acl = unicode(self.lineEditAcl.text())
    encoding = unicode(self.lineEditEncoding.text())
    tags = unicode(self.lineEditTags.text())

    # Extract the features from the current layer to a temporary shapefile.
    # This shapefile would be uploaded to maps engine. This approach ensures
    # that we are able to upload any layer that QGIS has ability to read,
    # including CSV files, databases etc.

    # TODO: use with tempfile.TemporaryDirectory() instead of try/finally.
    try:
      tempDir = tempfile.mkdtemp()
      tempShpPath = os.path.join(tempDir, layerName + '.shp')

      outputCrs = QgsCoordinateReferenceSystem(
          4326, QgsCoordinateReferenceSystem.EpsgCrsId)
      currentLayer = self.iface.mapCanvas().currentLayer()
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector',
          'Extracting data to a temporary shapefile. Please wait...',
          level=QgsMessageBar.INFO)
      error = QgsVectorFileWriter.writeAsVectorFormat(
          currentLayer, tempShpPath, encoding.lower(),
          outputCrs, 'ESRI Shapefile')

      if error != QgsVectorFileWriter.NoError:
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', 'Extraction to shapefile failed.',
            level=QgsMessageBar.CRITICAL, duration=3)
        QgsMessageLog.logMessage('Extraction to shapefile failed.',
                                 'GMEConnector', QgsMessageLog.CRITICAL)
        return None

      filesToUpload = {}
      for ext in ('shp', 'shx', 'dbf', 'prj'):
        fileName = '%s.%s' % (layerName, ext)
        filePath = os.path.join(tempDir, fileName)
        filesToUpload[fileName] = filePath

      data = {}
      data['name'] = unicode(self.lineEditDestinationName.text())
      data['description'] = unicode(self.lineEditDescription.text())
      data['files'] = [{'filename': x} for x in filesToUpload]
      data['sharedAccessList'] = acl
      if tags:
        data['tags'] = [unicode(x) for x in tags.split(',')]
      data['sourceEncoding'] = encoding

      token = oauth2_utils.getToken()
      api = gme_api.GoogleMapsEngineAPI(self.iface)
      assetId = api.postCreateAsset(projectId, data, token)
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
      for fileName in filesToUpload:
        msg = 'Uploading file %s' % filesToUpload[fileName]
        self.iface.messageBar().pushMessage(
            'Google Maps Engine Connector', msg, level=QgsMessageBar.INFO)
        QCoreApplication.processEvents()

        content = open(filesToUpload[fileName]).read()
        api.postUploadFile(assetId, fileName, content, token)

      self.iface.messageBar().clearWidgets()

      # Open the newly created asset in web browser
      url = ('https://mapsengine.google.com/admin/'
             '#RepositoryPlace:cid=%s&'
             'v=DETAIL_INFO&aid=%s')
      gmeUrl = url % (assetId.split('-')[0], assetId)
      webbrowser.open(gmeUrl)
    finally:
      # Cleanup
      shutil.rmtree(tempDir)
