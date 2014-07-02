"""Dialog for select a Google Maps Engine map.

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
import codecs
import cStringIO
import csv
import gme_api
import oauth2_utils
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QTableWidgetItem
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsMessageLog
from qgis.core import QgsPoint
from qgis.core import QgsVectorLayer
from qgis.gui import QgsMessageBar
from search_gme_dialog_base import Ui_Dialog
import settings

worldGeom = QgsGeometry.fromPolygon(
    [[QgsPoint(-180, -90), QgsPoint(-180, 90),
      QgsPoint(180, 90), QgsPoint(180, -90)]])


class Dialog(QDialog, Ui_Dialog):
  """Dialog implementation class for the search dialog."""

  def __init__(self, iface):
    """Constructor for the dialog."""
    QDialog.__init__(self, iface.mainWindow())
    self.setupUi(self)
    self.iface = iface
    # Disable the OK button.
    self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
    self.okButton.setEnabled(False)
    self.okButton.setText('Add Selected to Map')

    self.comboBox.activated.connect(self.loadMapsForIndex)
    self.copyButton.setEnabled(False)
    self.copyButton.clicked.connect(self.copyToClipBoard)

    # When any cell in the table is clicked, select the entire row.
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.tableWidget.itemSelectionChanged.connect(
        self.handleSelectionChanged)

    # Trigger search on every keystroke.
    self.lineEdit.textChanged.connect(self.searchLocalDirectory)

    self.loadInitialMaps()
    self.iface.messageBar().clearWidgets()

  def loadInitialMaps(self):
    """Populates the dialog with maps."""
    self.projectDict = settings.read('gmeconnector/PROJECTS')
    self.comboBox.clear()
    for key, val in self.projectDict.items():
      projectId = key
      projectName = val
      self.comboBox.addItem(projectName, projectId)

    defaultProjectId = settings.read('gmeconnector/DEFAULT_PROJECT')
    lastUsedProjectId = settings.read('gmeconnector/LAST_USED_PROJECT')
    # Check if the user has selected a default project
    if defaultProjectId and defaultProjectId in self.projectDict:
      self.loadMapsForProject(defaultProjectId)
    # If there is no default project, load the last used project
    elif lastUsedProjectId and lastUsedProjectId in self.projectDict:
      self.loadMapsForProject(lastUsedProjectId)
    # Load the first project in the dictionary
    else:
      self.loadMapsForProject(self.projectDict.iterkeys().next())

  def searchLocalDirectory(self):
    """Simple search implementation based on substring match."""
    search_term = unicode(self.lineEdit.text())
    currentIndex = self.comboBox.currentIndex()
    currentProjectId = unicode(self.comboBox.itemData(currentIndex))
    if search_term:
      filtered_maps = []
      for gmeMap in self.maps:
        if (gmeMap.id.lower() == search_term.lower() or
            search_term.lower() in gmeMap.name.lower()):
          filtered_maps.append(gmeMap)
      self.populateTable(filtered_maps)
      labelText = 'Displaying %d results from account %s' % (
          len(filtered_maps), self.projectDict[currentProjectId])
      self.resultLabel.setText(labelText)
    else:
      # This is needed to return to original state after a search term is
      # deleted.
      self.populateTable(self.maps)
      labelText = 'Displaying %d maps from account %s' % (
          len(self.maps), self.projectDict[currentProjectId])
      self.resultLabel.setText(labelText)

  def populateTable(self, maps):
    """Populates the table widget with map information.

    Args:
      maps: list, of gme_map.Map objects.
    """
    numrows = len(maps)
    numcols = 2
    self.tableWidget.setSortingEnabled(True)
    self.tableWidget.setRowCount(numrows)
    self.tableWidget.setColumnCount(numcols)
    row_index = 0
    self.tableWidget.setColumnWidth(0, 400)
    self.tableWidget.setColumnWidth(1, 500)
    header2 = QTableWidgetItem('Map Identifier')
    self.tableWidget.setHorizontalHeaderItem(0, header2)
    header1 = QTableWidgetItem('Name')
    self.tableWidget.setHorizontalHeaderItem(1, header1)
    for gmeMap in maps:
      col1 = gmeMap.id
      item1 = QTableWidgetItem('%s' % col1)
      col2 = gmeMap.name
      item2 = QTableWidgetItem('%s' % col2)

      self.tableWidget.setItem(row_index, 0, item1)
      self.tableWidget.setItem(row_index, 1, item2)
      row_index += 1

  def loadMapsForIndex(self, index):
    """Loads map for thegiven index.

    Args:
      index: int, index of the comboBox widget.
    """
    projectId = unicode(self.comboBox.itemData(index))
    self.loadMapsForProject(projectId)

  def loadMapsForProject(self, projectId):
    """Loads maps for the given project id.

    Args:
      projectId: str, id of the maps engine project.
    """
    index = self.comboBox.findData(projectId)
    self.comboBox.setCurrentIndex(index)
    settings.write('gmeconnector/LAST_USED_PROJECT', projectId)
    api = gme_api.GoogleMapsEngineAPI(self.iface)
    token = oauth2_utils.getToken()
    self.maps = api.getMapsByProjectId(projectId, token)
    self.populateTable(self.maps)
    if not self.maps:
      labelText = 'No maps found from account %s' % self.projectDict[projectId]
    else:
      labelText = 'Displaying %d maps from account %s' % (
          len(self.maps), self.projectDict[projectId])
    self.resultLabel.setText(labelText)

  def handleSelectionChanged(self):
    """Enables the OK button when a row is selected."""
    selection = self.tableWidget.selectionModel()
    selectionList = selection.selectedRows()
    if selectionList:
      self.copyButton.setEnabled(True)
    else:
      self.copyButton.setEnabled(False)

    if len(selectionList) == 1:
      self.okButton.setEnabled(True)
    else:
      self.okButton.setEnabled(False)

  def copyToClipBoard(self):
    """Copies the selection to clipboard."""
    selection = self.tableWidget.selectionModel()
    selectionList = selection.selectedRows()
    copyText = cStringIO.StringIO()
    csvWriter = UnicodeWriter(copyText)
    for selection in selectionList:
      row = selection.row()
      mapId = self.tableWidget.item(row, 0).text()
      mapName = self.tableWidget.item(row, 1).text()
      csvWriter.writerow([unicode(mapId), unicode(mapName)])
    clipboard = QApplication.clipboard()
    clipboard.setText(copyText.getvalue())

  def accept(self):
    """Fetches the selected map and loads it in map canvas.

    Creates a new vector layer with features representing the bounding boxes for
    the map as well as all layers contained in the map. The layer is added to
    the QGIS canvas with the map feature selected.
    """
    # Close the dialog immediately and start the process of creating the layer.
    self.close()

    # Get the map identifier
    selection = self.tableWidget.selectionModel()
    selectionList = selection.selectedRows()
    row = selectionList[0].row()
    selectedMapId = self.tableWidget.item(row, 0).text()
    selectedMapName = self.tableWidget.item(row, 1).text()

    dislayText = ('Fetching map and layer extents: %s. '
                  'Please wait...') % selectedMapName
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector', dislayText, level=QgsMessageBar.INFO)
    QCoreApplication.processEvents()

    api = gme_api.GoogleMapsEngineAPI(self.iface)
    token = oauth2_utils.getToken()
    gmeMap = api.getMapById(selectedMapId, token)
    gmeLayers = self.getLayers(gmeMap)
    self.iface.messageBar().clearWidgets()
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector',
        'View tools are now enabled.',
        level=QgsMessageBar.INFO, duration=6)

    dislayText = 'Loaded extents for map: %s.' % gmeMap.name
    self.iface.messageBar().pushMessage(
        'Google Maps Engine Connector', dislayText,
        level=QgsMessageBar.INFO, duration=3)
    vectorLayer = self.createVectorLayer(gmeMap.name)
    provider = vectorLayer.dataProvider()
    vectorLayer.startEditing()
    # Add the map
    mapFeature = QgsFeature()
    projectId = gmeMap.id.split('-')[0]
    if gmeMap.bbox:
      geom = self.getGeomFromBbox(gmeMap.bbox)
      mapFeature.setGeometry(geom)
    else:
      errorMsg = 'Map %s does not have a geometry' % gmeMap.id
      QgsMessageLog.logMessage(errorMsg, 'GMEConnector', QgsMessageLog.WARNING)
      mapFeature.setGeometry(worldGeom)
    mapFeature.setAttributes([projectId, gmeMap.id, gmeMap.id,
                              projectId, 'map', gmeMap.name, 'n/a'])
    provider.addFeatures([mapFeature])

    # Add the layers
    for gmeLayer in gmeLayers:
      layerFeature = QgsFeature()
      projectId = gmeMap.id.split('-')[0]
      try:
        geom = self.getGeomFromBbox(gmeLayer.bbox)
        layerFeature.setGeometry(geom)
      except AttributeError:
        errorMsg = 'Layer %s does not have a geometry' % gmeLayer.id
        QgsMessageLog.logMessage(errorMsg, 'GMEConnector',
                                 QgsMessageLog.WARNING)
        layerFeature.setGeometry(worldGeom)

      try:
        datasourceType = gmeLayer.datasourceType
      except AttributeError:
        datasourceType = 'unknown'

      layerFeature.setAttributes([projectId, gmeMap.id, gmeLayer.id,
                                  gmeMap.id, 'layer', gmeLayer.name,
                                  datasourceType])
      provider.addFeatures([layerFeature])

    # Finalize the vector layer
    vectorLayer.updateExtents()
    vectorLayer.commitChanges()

    # Add the layer to the canvas
    vectorLayer.loadNamedStyle(
        ':/plugins/googlemapsengineconnector/styles/catalog_style.qml')
    QgsMapLayerRegistry.instance().addMapLayer(vectorLayer)

    # Zoom to the newly added layer
    self.iface.mapCanvas().setExtent(vectorLayer.extent())

    # Pre-select the map feature
    # This triggers the signal to enable other tools
    for feature in vectorLayer.getFeatures():
      if 'map' in feature.attributes():
        vectorLayer.setSelectedFeatures([feature.id()])

    # Set the newly loaded layer as the active layer
    self.iface.legendInterface().setCurrentLayer(vectorLayer)

  def createVectorLayer(self, layerName):
    """Creates a vector layer in memory.

    Args:
      layerName: str, name of the layer to create.
    Returns:
      QgsVectorLayer instance
    """
    vectorLayer = QgsVectorLayer('Polygon?crs=EPSG:4326', layerName, 'memory')
    self.dataProvider = vectorLayer.dataProvider()
    self.dataProvider.addAttributes(
        [QgsField('Project Identifier', QVariant.String),
         QgsField('Map Resource Identifier', QVariant.String),
         QgsField('Resource Identifier', QVariant.String),
         QgsField('Parent Resource Identifier', QVariant.String),
         QgsField('Resource Type', QVariant.String),
         QgsField('Resource Name', QVariant.String),
         QgsField('Data Source Type', QVariant.String)])
    return vectorLayer

  def getLayers(self, gmeMap):
    """Get full layers from the given map object.

    Args:
      gmeMap: gme_map.Map object
    Returns:
      list of gme_layer.Layer objects
    """
    gmeLayers = []
    layers = [x for x in gmeMap.contents if x.type == 'layer']
    for layer in layers:
      gmeLayer = self.fetchFullLayer(layer)
      if gmeLayer:
        gmeLayers.append(gmeLayer)

    folders = [x for x in gmeMap.contents if x.type == 'folder']
    for folder in folders:
      childLayers = self.fetchLayersInFolder(folder)
      gmeLayers.extend(childLayers)
    return gmeLayers

  def fetchFullLayer(self, layer):
    """Fetch full layer information.

    Args:
      layer: gme_item.Item object
    Returns:
      gme_layer.Layer object if successful, same object if failed.
    """
    api = gme_api.GoogleMapsEngineAPI(self.iface)
    token = oauth2_utils.getToken()
    gmeLayer = api.getLayerById(layer.id, token)
    if not gmeLayer:
      return layer
    else:
      return gmeLayer

  def fetchLayersInFolder(self, gmeFolder):
    """Fetch layers in the given folder.

    Args:
      gmeFolder: gme_folder.Folder object
    Returns:
      list of gme_layer.Layer objects
    """
    gmeLayers = []
    layers = [x for x in gmeFolder.contents if x.type == 'layer']
    for layer in layers:
      gmeLayer = self.fetchFullLayer(layer)
      gmeLayers.append(gmeLayer)
    # Recursive call to populate folders within the current folder
    folders = [x for x in gmeFolder.contents if x.type == 'folder']
    if folders:
      for folder in folders:
        gmeLayers.extend(self.fetchLayersInFolder(folder))
    return gmeLayers

  def getGeomFromBbox(self, bbox):
    """Creates a QgsGeometry object from the given bbox.

    Args:
      bbox: list, of bounding box cordinates.
    Returns:
      QgsGeometry object.
    """
    lllon, lllat, urlon, urlat = bbox
    geom = QgsGeometry.fromPolygon(
        [[QgsPoint(lllon, lllat),
          QgsPoint(lllon, urlat),
          QgsPoint(urlon, urlat),
          QgsPoint(urlon, lllat)]])
    return geom


# Drop-in code from pydoc example.
class UnicodeWriter:

  def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
    # Redirect output to a queue
    self.queue = cStringIO.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.stream = f
    self.encoder = codecs.getincrementalencoder(encoding)()

  def writerow(self, row):
    self.writer.writerow([s.encode('utf-8') for s in row])
    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode('utf-8')
    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)
    # write to the target stream
    self.stream.write(data)
    # empty queue
    self.queue.truncate(0)

  def writerows(self, rows):
    for row in rows:
      self.writerow(row)
