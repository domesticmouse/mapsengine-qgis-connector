"""More dialog to display settings and about info.

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

from PyQt4.QtCore import QFile
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QTextStream
from PyQt4.QtGui import QDialog
from PyQt4.QtWebKit import QWebPage

from more_dialog_base import Ui_Dialog
import settings


class Dialog(QDialog, Ui_Dialog):
  """Dialog implementation class for the More dialog."""

  def __init__(self, iface):
    """Constructor for the dialog.

    Args:
      iface: QgsInterface instance.
    """
    QDialog.__init__(self, iface.mainWindow())
    self.setupUi(self)

    # Settings Tab
    # Show the current value of client_id and client_secret
    client_id = settings.read('gmeconnector/CLIENT_ID')
    client_secret = settings.read('gmeconnector/CLIENT_SECRET')
    if client_id is None:
      client_id = ''
    if client_secret is None:
      client_secret = ''
    self.lineEdit1.setText(client_id)
    self.lineEdit2.setText(client_secret)

    # Other settings
    self.comboBoxProjects.setEnabled(False)
    self.checkBoxDefault.stateChanged.connect(self.comboBoxProjects.setEnabled)
    self.comboBoxFormat.addItem('JPEG', 'image/jpeg')
    self.comboBoxFormat.addItem('PNG', 'image/png')
    defaultFormat = settings.read('gmeconnector/WMS_IMAGE_FORMAT')

    if defaultFormat:
      defaultIndex = self.comboBoxFormat.findText(defaultFormat)
      if defaultIndex != -1:
        self.comboBoxFormat.setCurrentIndex(defaultIndex)
    self.comboBoxFormat.currentIndexChanged.connect(self.handleFormatChanged)

    # OAuth help
    oAuthPage = QWebPage()
    oAuthPage.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    self.webViewOAuth.setPage(oAuthPage)

    # Load the oauth_help file
    helpFile = QFile(':/plugins/googlemapsengineconnector/oauth_help.html')
    helpFile.open(QIODevice.ReadOnly | QIODevice.Text)
    helpStr = QTextStream(helpFile)
    helpText = helpStr.readAll()
    self.webViewOAuth.setHtml(helpText)
    self.webViewOAuth.linkClicked.connect(self.handleWebLink)

    # About Tab
    aboutPage = QWebPage()
    aboutPage.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    self.webViewAbout.setPage(aboutPage)
    # Load the about.html file and add current version info.
    aboutFile = QFile(':/plugins/googlemapsengineconnector/about.html')
    aboutFile.open(QIODevice.ReadOnly | QIODevice.Text)
    aboutStr = QTextStream(aboutFile)
    aboutText = aboutStr.readAll()
    newText = aboutText.format(version='1.1')
    self.webViewAbout.setHtml(newText)
    self.webViewAbout.linkClicked.connect(self.handleWebLink)

  def handleWebLink(self, url):
    """Opens the given url in the web browser.

    Args:
      url: str, url to open
    """
    webbrowser.open(url.toString())

  def handleFormatChanged(self, index):
    """Saves the format settings.

    Args:
      index: int, index of comboBoxFormat widget
    """
    imageFormat = unicode(
        self.comboBoxFormat.itemText(index))
    settings.write('gmeconnector/WMS_IMAGE_FORMAT', imageFormat)

  def populateProjects(self):
    """Adds the project information to the comboBoxProjects widget."""
    self.projectDict = settings.read('gmeconnector/PROJECTS')
    self.comboBoxProjects.clear()
    for key, val in self.projectDict.items():
      projectId = key
      projectName = val
      self.comboBoxProjects.addItem(projectName, projectId)

    defaultProjectId = settings.read('gmeconnector/DEFAULT_PROJECT')
    if defaultProjectId:
      self.checkBoxDefault.setChecked(True)
      index = self.comboBoxProjects.findData(defaultProjectId)
      self.comboBoxProjects.setCurrentIndex(index)

  def accept(self):
    """Saves the settings and closes the dialog."""
    if self.checkBoxDefault.isChecked():
      projectIndex = self.comboBoxProjects.currentIndex()
      projectId = unicode(self.comboBoxProjects.itemData(projectIndex))
      settings.write('gmeconnector/DEFAULT_PROJECT', projectId)
    else:
      settings.write('gmeconnector/DEFAULT_PROJECT', '')

    settings.write('gmeconnector/CLIENT_ID', self.lineEdit1.text().strip())
    settings.write('gmeconnector/CLIENT_SECRET', self.lineEdit2.text().strip())
    self.close()
