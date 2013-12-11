# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin/more_dialog_base.ui'
#
# Created: Tue Dec 10 15:19:38 2013
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
        Dialog.resize(500, 600)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 560, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 500, 540))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.groupBoxAccount = QtGui.QGroupBox(self.tab)
        self.groupBoxAccount.setGeometry(QtCore.QRect(10, 200, 480, 111))
        self.groupBoxAccount.setObjectName(_fromUtf8("groupBoxAccount"))
        self.checkBoxDefault = QtGui.QCheckBox(self.groupBoxAccount)
        self.checkBoxDefault.setGeometry(QtCore.QRect(10, 30, 171, 22))
        self.checkBoxDefault.setObjectName(_fromUtf8("checkBoxDefault"))
        self.comboBoxProjects = QtGui.QComboBox(self.groupBoxAccount)
        self.comboBoxProjects.setGeometry(QtCore.QRect(10, 60, 450, 27))
        self.comboBoxProjects.setObjectName(_fromUtf8("comboBoxProjects"))
        self.groupBoxWms = QtGui.QGroupBox(self.tab)
        self.groupBoxWms.setGeometry(QtCore.QRect(10, 310, 480, 121))
        self.groupBoxWms.setObjectName(_fromUtf8("groupBoxWms"))
        self.comboBoxVectorFormat = QtGui.QComboBox(self.groupBoxWms)
        self.comboBoxVectorFormat.setGeometry(QtCore.QRect(370, 30, 78, 30))
        self.comboBoxVectorFormat.setObjectName(_fromUtf8("comboBoxVectorFormat"))
        self.label = QtGui.QLabel(self.groupBoxWms)
        self.label.setGeometry(QtCore.QRect(10, 30, 281, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(self.groupBoxWms)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 281, 30))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.comboBoxRasterFormat = QtGui.QComboBox(self.groupBoxWms)
        self.comboBoxRasterFormat.setGeometry(QtCore.QRect(370, 70, 78, 30))
        self.comboBoxRasterFormat.setObjectName(_fromUtf8("comboBoxRasterFormat"))
        self.groupBoxAccount_2 = QtGui.QGroupBox(self.tab)
        self.groupBoxAccount_2.setGeometry(QtCore.QRect(10, 10, 480, 181))
        self.groupBoxAccount_2.setObjectName(_fromUtf8("groupBoxAccount_2"))
        self.lineEdit1 = QtGui.QLineEdit(self.groupBoxAccount_2)
        self.lineEdit1.setGeometry(QtCore.QRect(110, 100, 341, 30))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.label_2 = QtGui.QLabel(self.groupBoxAccount_2)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 75, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBoxAccount_2)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 100, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit2 = QtGui.QLineEdit(self.groupBoxAccount_2)
        self.lineEdit2.setGeometry(QtCore.QRect(110, 140, 341, 30))
        self.lineEdit2.setObjectName(_fromUtf8("lineEdit2"))
        self.webViewOAuth = QtWebKit.QWebView(self.groupBoxAccount_2)
        self.webViewOAuth.setGeometry(QtCore.QRect(10, 30, 441, 60))
        self.webViewOAuth.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webViewOAuth.setObjectName(_fromUtf8("webViewOAuth"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.webViewAbout = QtWebKit.QWebView(self.tab_2)
        self.webViewAbout.setGeometry(QtCore.QRect(0, 0, 500, 510))
        self.webViewAbout.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webViewAbout.setObjectName(_fromUtf8("webViewAbout"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "More", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxAccount.setTitle(QtGui.QApplication.translate("Dialog", "Account Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefault.setText(QtGui.QApplication.translate("Dialog", "Set Default Account", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxWms.setTitle(QtGui.QApplication.translate("Dialog", "WMS Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Default Image Format for Vector Overlays", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Default Image Format for Raster Overlays", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxAccount_2.setTitle(QtGui.QApplication.translate("Dialog", "OAuth 2.0 Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Client ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Client Secret:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Advanced Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
