# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'monthlyprojectsequipment.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_equipment_picker(object):
    def setupUi(self, equipment_picker):
        equipment_picker.setObjectName(_fromUtf8("equipment_picker"))
        equipment_picker.resize(265, 86)
        self.gridLayout = QtGui.QGridLayout(equipment_picker)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.equipment_type = QtGui.QLabel(equipment_picker)
        self.equipment_type.setObjectName(_fromUtf8("equipment_type"))
        self.gridLayout.addWidget(self.equipment_type, 0, 0, 1, 1)
        self.equipment_in_stock = QtGui.QComboBox(equipment_picker)
        self.equipment_in_stock.setObjectName(_fromUtf8("equipment_in_stock"))
        self.gridLayout.addWidget(self.equipment_in_stock, 1, 0, 1, 1)

        self.retranslateUi(equipment_picker)
        QtCore.QMetaObject.connectSlotsByName(equipment_picker)

    def retranslateUi(self, equipment_picker):
        equipment_picker.setWindowTitle(_translate("equipment_picker", "Equipment Picker", None))
        self.equipment_type.setText(_translate("equipment_picker", "TextLabel", None))

