__author__ = 'Danuel'

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lxml import etree
from threading import Timer
import ui_monthlyprojectsmain
import monthlyprojects_makebooking_qt1
import datetime

import re


class MonthlyProjects(QDialog,
                      ui_monthlyprojectsmain.Ui_MonthlyProjects):
    def __init__(self, parent=None):
        super(MonthlyProjects, self).__init__(parent)
        self.setupUi(self)
        self.monthly_projects_data = etree.parse("MonthlyProjects(TestingPurposes).xml")
        self.test_date = datetime.datetime(2014, 10, 8)
        self.todays_tickets = self.monthly_projects_data.xpath(
            "/MonthlyProjects/EntryDate[@date='{}']/Ticket"
                .format(self.test_date.isoformat()))
        self.current_date.setText(self.test_date.strftime("%a %d, %b %Y"))

        # If for any reason a ticket should be postponed or cancelled
        self.discarded_tickets = []

    @pyqtSignature("")
    def on_makeBooking_clicked(self):
        dialog = monthlyprojects_makebooking_qt1.MakeBookingDiag(self.monthly_projects_data, self)
        if dialog.exec_():
            # Validation of the information placed in the form
            # for making a booking needs is validated

            # Check to see if the Ticket number has been repeated

            # Check Time Out and Time In

            # Ensure that notes is clean and doesn't interfere with the XML in anyway
            QMessageBox.information(self,"Make Booking",
                                    "Booking has been made successfully")
            pass
        else:
            pass


    @pyqtSignature("int")
    def on_current_booking_status_currentIndexChanged(self, int):
        if self.current_booking_status.currentText == "Postponed" or \
           self.current_booking_status.currentText == "Cancelled":
            # Place into discarded_tickets, in case of incidental cancellation
            self.discarded_tickets.append = self.ticket_num

    def tickets_in_next_hour(self, in_or_out):
        tickets_in_next_hour = []

        if in_or_out == "IN":
            in_or_out = "Out"
        elif in_or_out == "OUT":
            in_or_out = "Time"

        for ticket in self.todays_tickets:
            if ticket.find(in_or_out).text is not None:
                timein_ticket = ticket.find(in_or_out).text.strip()
            else:
                break
            # STRIPPING THE TIME OUT OF THE ENTRY
            amOrPm = re.search("(A\.?M\.?|(P\.?M\.?)|(a\.?m\.?|p\.?m\.?))", timein_ticket).group()
            amOrPm = self.strip_and_capitalize(amOrPm)
            hour = re.search("\d\d:", timein_ticket)
            if hour is None or int(hour.group()[:len(hour.group())-1]) > 12:
                hour = re.search("\d:", timein_ticket)
                hour = int(hour.group()[:len(hour.group())-1])
            else:
                hour = hour.group()[:len(hour.group())-1]
                hour = int(hour)
            minutes = int(re.search(":\d\d", timein_ticket).group()[1:])
            if amOrPm == "PM" and hour != 12:
                hour += 12

            ticket_time = datetime.time(hour, minutes)
            ticket_time = datetime.timedelta(hours=hour, minutes=minutes)
            current_time = datetime.timedelta(hours=datetime.datetime.now().time().hour,
                                              minutes=datetime.datetime.now().time().minute)

            difference = ticket_time - current_time
            if difference.seconds / 3600 <= 1:
                tickets_in_next_hour.append(ticket)
        return tickets_in_next_hour

    def strip_and_capitalize(self, string):
        """Strips . and unwanted spaces from strings in use"""
        split_string = string.split('.')
        return_string = ""
        for i in split_string:
            if not i.isupper():
                upperchar = i.upper()
                return_string += upperchar
            else:
                return_string += i
        return return_string

    def updateUi(self):
        """Updates the display to show the tickets in the next hour"""
        # TODO: Addition of animations to float updates in and out of the display.
        # Tickets whose time is coming to the end as well as
        # bookings which are starting.
        up_coming_tickets = self.tickets_in_next_hour("IN")
        up_coming_tickets += self.tickets_in_next_hour("OUT")
        if up_coming_tickets is [] :
            self.ticket_num.setText("Ticket #")
            self.client_name.setText("Client Name")
            self.setup_location.setText("Setup Location")
            self.notes.setText("Nothing Found")
            self.time_out.setText("Time Out")
            self.time_in.setText("Time In")
            self.time_out.setText("Time Out")
            self.setup_type.setText("N/A")
            self.tech_assigned.setText("N/A")
            return False
        else:
            for i, ticket in enumerate(up_coming_tickets):
                tags = ["Name", "SetupLocation", "RequestDetail",
                        "Time", "Out", "SetUppickUp", "TechAssigned"]
                labels = [self.client_name, self.setup_location, self.notes,
                          self.time_out, self.time_in, self.setup_type,
                          self.tech_assigned]
                # self.number_of_tickets.setText("{}/{}".format(i+1,len(up_coming_tickets)))
                self.number_of_tickets.display(i+1)
                if ticket.attrib['number'] is not None:
                    if not ticket.attrib['number'] in self.discarded_tickets:
                        self.ticket_num.setText(ticket.attrib['number'])
                    else:
                        continue
                else:
                    self.ticket_num.setText("NO Ticket Number Found")
                for i, tag in enumerate(tags):
                    if ticket.find(tag).text is not None:
                        if isinstance(labels[i], QTextEdit):
                            labels[i].toHtml(ticket.find(tag).text)
                        else:
                            labels[i].setText(ticket.find(tag).text)
                    else:
                        if isinstance(labels[i], QTextEdit):
                            labels[i].toHtml("Error")
                        else:
                            labels[i].setText("Error")
            return True


class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


app = QApplication(sys.argv)
app.setStyle("cleanlooks")
monthlyprojects = MonthlyProjects()
monthlyprojects.show()

test = perpetualTimer(10, monthlyprojects.updateUi)
test.start()

app.exec_()
