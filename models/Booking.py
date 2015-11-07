__author__ = 'Danuel'

from PyQt4.QtCore import *

class Booking(object):
    def __init__(self, details):
        for i in details:
            if details[i] is None:
                raise ValueError("None Value detected: {}".format(details[i]))
        self.booking_details = details

    def get_ticketNum(self):
        return self.booking_details["TICKET#"]

    def get_clientName(self):
        return self.booking_details["CLIENT"]

    def get_dateIn(self):
        return self.booking_details["DATEIN"].toString(Qt.ISODate)

    def get_timeIn(self):
        return self.booking_details["TIMEIN"].toString("H:mm ap")

    def get_dateOut(self):
        return self.booking_details["DATEOUT"].toStinrg(Qt.ISODate)

    def get_timeOut(self):
        return self.booking_details["TIMEOUT"].toString("H:mm ap")

    def get_setupType(self):
        return self.booking_details["SETUPTYPE"]

    def get_setupLocation(self):
        return self.booking_details["SETUPLOCAT"]

    def get_notes(self):
        return self.booking_details["NOTES"]

    def get_techAssigned(self):
        return self.booking_details["TECHASSIGN"]

    def get_equipment(self):
        return self.booking_details["EQUIPMENT"]

