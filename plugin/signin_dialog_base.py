# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GoogleMapsEngineConnector/plugin/signin_dialog_base.ui'
#
# Created: Thu Oct 17 17:01:44 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 500)
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
