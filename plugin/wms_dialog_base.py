# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GoogleMapsEngineConnector/plugin/wms_dialog_base.ui'
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
        Dialog.resize(550, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 260, 300, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.comboBoxLayer = QtGui.QComboBox(Dialog)
        self.comboBoxLayer.setGeometry(QtCore.QRect(10, 130, 525, 30))
        self.comboBoxLayer.setObjectName(_fromUtf8("comboBoxLayer"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 171, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.labelMapName = QtGui.QLabel(Dialog)
        self.labelMapName.setGeometry(QtCore.QRect(20, 30, 411, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelMapName.setFont(font)
        self.labelMapName.setObjectName(_fromUtf8("labelMapName"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 411, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboBoxFormat = QtGui.QComboBox(Dialog)
        self.comboBoxFormat.setGeometry(QtCore.QRect(140, 170, 120, 30))
        self.comboBoxFormat.setObjectName(_fromUtf8("comboBoxFormat"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 210, 100, 30))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.comboBoxCrs = QtGui.QComboBox(Dialog)
        self.comboBoxCrs.setGeometry(QtCore.QRect(140, 210, 120, 30))
        self.comboBoxCrs.setObjectName(_fromUtf8("comboBoxCrs"))
        self.labelMapId = QtGui.QLabel(Dialog)
        self.labelMapId.setGeometry(QtCore.QRect(20, 60, 411, 30))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelMapId.setFont(font)
        self.labelMapId.setObjectName(_fromUtf8("labelMapId"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Select A Layer to Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Currently selected map: ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMapName.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Select the layer which you would like to add as a WMS overlay", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Image Format", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "CRS", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMapId.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

