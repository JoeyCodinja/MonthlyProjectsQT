# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'monthlyprojectsmain.ui'
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

class Ui_MonthlyProjects(object):
    def setupUi(self, MonthlyProjects):
        MonthlyProjects.setObjectName(_fromUtf8("MonthlyProjects"))
        MonthlyProjects.resize(335, 309)
        MonthlyProjects.setMouseTracking(False)
        MonthlyProjects.setAutoFillBackground(False)
        self.gridLayout_2 = QtGui.QGridLayout(MonthlyProjects)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.number_of_tickets = QtGui.QLCDNumber(MonthlyProjects)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_of_tickets.sizePolicy().hasHeightForWidth())
        self.number_of_tickets.setSizePolicy(sizePolicy)
        self.number_of_tickets.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.number_of_tickets.setObjectName(_fromUtf8("number_of_tickets"))
        self.gridLayout_2.addWidget(self.number_of_tickets, 0, 1, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tech_assigned = QtGui.QLabel(MonthlyProjects)
        self.tech_assigned.setObjectName(_fromUtf8("tech_assigned"))
        self.gridLayout.addWidget(self.tech_assigned, 4, 0, 1, 1)
        self.client_name = QtGui.QLabel(MonthlyProjects)
        self.client_name.setObjectName(_fromUtf8("client_name"))
        self.gridLayout.addWidget(self.client_name, 1, 0, 1, 1)
        self.ticket_num = QtGui.QLabel(MonthlyProjects)
        self.ticket_num.setText(_fromUtf8(""))
        self.ticket_num.setObjectName(_fromUtf8("ticket_num"))
        self.gridLayout.addWidget(self.ticket_num, 0, 1, 1, 1)
        self.current_date = QtGui.QLabel(MonthlyProjects)
        self.current_date.setObjectName(_fromUtf8("current_date"))
        self.gridLayout.addWidget(self.current_date, 0, 2, 1, 1)
        self.setup_location = QtGui.QLabel(MonthlyProjects)
        self.setup_location.setObjectName(_fromUtf8("setup_location"))
        self.gridLayout.addWidget(self.setup_location, 1, 1, 1, 1)
        self.label = QtGui.QLabel(MonthlyProjects)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.time_out = QtGui.QLabel(MonthlyProjects)
        self.time_out.setObjectName(_fromUtf8("time_out"))
        self.gridLayout.addWidget(self.time_out, 3, 1, 1, 1)
        self.time_in = QtGui.QLabel(MonthlyProjects)
        self.time_in.setObjectName(_fromUtf8("time_in"))
        self.gridLayout.addWidget(self.time_in, 3, 2, 1, 1)
        self.setup_type = QtGui.QLabel(MonthlyProjects)
        self.setup_type.setObjectName(_fromUtf8("setup_type"))
        self.gridLayout.addWidget(self.setup_type, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 2)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(MonthlyProjects)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.current_booking_status = QtGui.QComboBox(MonthlyProjects)
        self.current_booking_status.setObjectName(_fromUtf8("current_booking_status"))
        self.current_booking_status.addItem(_fromUtf8(""))
        self.current_booking_status.addItem(_fromUtf8(""))
        self.current_booking_status.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.current_booking_status, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(MonthlyProjects)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.notes = QtGui.QTextEdit(MonthlyProjects)
        self.notes.setReadOnly(True)
        self.notes.setObjectName(_fromUtf8("notes"))
        self.verticalLayout.addWidget(self.notes)
        self.makeBooking = QtGui.QPushButton(MonthlyProjects)
        self.makeBooking.setObjectName(_fromUtf8("makeBooking"))
        self.verticalLayout.addWidget(self.makeBooking)
        self.gridLayout_2.addLayout(self.verticalLayout, 3, 0, 1, 2)

        self.retranslateUi(MonthlyProjects)
        QtCore.QMetaObject.connectSlotsByName(MonthlyProjects)

    def retranslateUi(self, MonthlyProjects):
        MonthlyProjects.setWindowTitle(_translate("MonthlyProjects", "MonthlyProjects", None))
        self.tech_assigned.setText(_translate("MonthlyProjects", "Tech Assigned", None))
        self.client_name.setText(_translate("MonthlyProjects", "Client Name ", None))
        self.current_date.setText(_translate("MonthlyProjects", "TextLabel", None))
        self.setup_location.setText(_translate("MonthlyProjects", "Setup Location", None))
        self.label.setText(_translate("MonthlyProjects", "Ticket Number ", None))
        self.time_out.setText(_translate("MonthlyProjects", "Time Out ", None))
        self.time_in.setText(_translate("MonthlyProjects", "Time In", None))
        self.setup_type.setText(_translate("MonthlyProjects", "Setup Type", None))
        self.label_2.setText(_translate("MonthlyProjects", "Current Booking Status", None))
        self.current_booking_status.setItemText(0, _translate("MonthlyProjects", "Postponed", None))
        self.current_booking_status.setItemText(1, _translate("MonthlyProjects", "Cancelled", None))
        self.current_booking_status.setItemText(2, _translate("MonthlyProjects", "On Going", None))
        self.label_9.setText(_translate("MonthlyProjects", "Notes", None))
        self.makeBooking.setText(_translate("MonthlyProjects", "New Booking", None))

