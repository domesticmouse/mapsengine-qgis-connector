"""Dialog to complete the OAuth sign-in flow.

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
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QDialog
from PyQt4.QtNetwork import QNetworkCookieJar
from qgis.gui import QgsMessageBar

import gme_api
import oauth2_utils
import settings
from signin_dialog_base import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
  """Dialog implementation class for the Sign-in dialog."""
  authStateChange = pyqtSignal(bool, object, str)

  def __init__(self, iface):
    """Constructor for the dialog.

    Args:
      iface: QgsInterface instance.
    """
    QDialog.__init__(self, iface.mainWindow())
    self.setupUi(self)
    self.iface = iface
    self.webView.loadFinished.connect(self.webBrowserNavigated)

  def setInitialUrl(self):
    """Set the url to go to when the dialog is loaded.

    Clear the cookies before setting the initial url.This is because once a
    user completes the sign-in flow, a cookie is stored within QWebview and
    are not cleared until the plugin is reloaded. Clearing the cookies before
    showing the sign-in box.
    """
    manager = self.webView.page().networkAccessManager()
    cookieJar = QNetworkCookieJar()
    manager.setCookieJar(cookieJar)
    qurl = QUrl()
    qurl.setEncodedUrl(oauth2_utils.buildAuthenticationUri())
    self.webView.setUrl(qurl)

  def webBrowserNavigated(self):
    """Check if the authentication was successful after every page load."""
    url_str = self.webView.url().toString()
    title = self.webView.title()
    self.setWindowTitle(title)

    if not url_str.startswith('https://accounts.google.com/o/oauth2/approval'):
      return

    # Trigger the automatic slot accept() to close the dialog.
    self.accept()
    token = oauth2_utils.decodeTitleResponse(title)

    if not token:
      self.authStateChange.emit(False, None, '')
      return

    oauth2_utils.setToken(token)
    api = gme_api.GoogleMapsEngineAPI(self.iface)
    userName = oauth2_utils.getUserName(token)
    results = api.getProjects(token)
    if not results:
      self.authStateChange.emit(False, token, userName)
      return

    # Make sure the user has access to maps engine projects.
    if not results.get('projects'):
      self.authStateChange.emit(False, token, userName)
      self.iface.messageBar().pushMessage(
          'Google Maps Engine Connector',
          'You do not have access to any Google Maps Engine accounts.',
          level=QgsMessageBar.INFO, duration=6)
      return

    self.authStateChange.emit(True, token, userName)
    projectDict = {}
    for project in results['projects']:
      projectDict[project['id']] = project['name']
    settings.write('gmeconnector/PROJECTS', projectDict)
