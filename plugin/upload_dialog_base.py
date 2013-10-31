# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin/upload_dialog_base.ui'
#
# Created: Thu Oct 31 14:08:56 2013
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
        Dialog.resize(600, 475)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(280, 440, 300, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 120, 621, 271))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBoxProjects = QtGui.QComboBox(self.groupBox)
        self.comboBoxProjects.setGeometry(QtCore.QRect(160, 30, 400, 30))
        self.comboBoxProjects.setObjectName(_fromUtf8("comboBoxProjects"))
        self.labelAccount = QtGui.QLabel(self.groupBox)
        self.labelAccount.setGeometry(QtCore.QRect(10, 30, 100, 30))
        self.labelAccount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAccount.setObjectName(_fromUtf8("labelAccount"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 100, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEditDestinationName = QtGui.QLineEdit(self.groupBox)
        self.lineEditDestinationName.setGeometry(QtCore.QRect(160, 70, 400, 30))
        self.lineEditDestinationName.setObjectName(_fromUtf8("lineEditDestinationName"))
        self.labelAcl = QtGui.QLabel(self.groupBox)
        self.labelAcl.setGeometry(QtCore.QRect(10, 150, 100, 30))
        self.labelAcl.setObjectName(_fromUtf8("labelAcl"))
        self.lineEditAcl = QtGui.QLineEdit(self.groupBox)
        self.lineEditAcl.setGeometry(QtCore.QRect(160, 150, 400, 30))
        self.lineEditAcl.setObjectName(_fromUtf8("lineEditAcl"))
        self.labelAttribution = QtGui.QLabel(self.groupBox)
        self.labelAttribution.setGeometry(QtCore.QRect(10, 230, 100, 30))
        self.labelAttribution.setObjectName(_fromUtf8("labelAttribution"))
        self.lineEditAttribution = QtGui.QLineEdit(self.groupBox)
        self.lineEditAttribution.setGeometry(QtCore.QRect(160, 230, 400, 30))
        self.lineEditAttribution.setObjectName(_fromUtf8("lineEditAttribution"))
        self.labelTags = QtGui.QLabel(self.groupBox)
        self.labelTags.setGeometry(QtCore.QRect(10, 190, 100, 30))
        self.labelTags.setObjectName(_fromUtf8("labelTags"))
        self.lineEditTags = QtGui.QLineEdit(self.groupBox)
        self.lineEditTags.setGeometry(QtCore.QRect(160, 190, 400, 30))
        self.lineEditTags.setObjectName(_fromUtf8("lineEditTags"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 100, 30))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEditDescription = QtGui.QLineEdit(self.groupBox)
        self.lineEditDescription.setGeometry(QtCore.QRect(160, 110, 400, 30))
        self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 600, 100))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 20, 100, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEditLocalPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditLocalPath.setGeometry(QtCore.QRect(160, 60, 400, 30))
        self.lineEditLocalPath.setObjectName(_fromUtf8("lineEditLocalPath"))
        self.lineEditLayerName = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditLayerName.setGeometry(QtCore.QRect(160, 20, 400, 30))
        self.lineEditLayerName.setObjectName(_fromUtf8("lineEditLayerName"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 380, 550, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.LogText)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Upload a dataset to Google Maps Engine", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAccount.setText(QtGui.QApplication.translate("Dialog", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAcl.setText(QtGui.QApplication.translate("Dialog", "Access List", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAttribution.setText(QtGui.QApplication.translate("Dialog", "Attribution*", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTags.setText(QtGui.QApplication.translate("Dialog", "Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Layer Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Local Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "* Required for rasters. Must be the name of an existing attribution.", None, QtGui.QApplication.UnicodeUTF8))

