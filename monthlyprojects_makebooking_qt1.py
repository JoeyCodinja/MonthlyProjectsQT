__author__ = 'Danuel'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from lxml import etree
from datetime import datetime

import getpass
import ui_monthlyprojects_makebooking
import ui_monthlyprojectsequipment

import monthlyprojects_equipment

from models.Booking import Booking

class MakeBookingDiag(QDialog,
                      ui_monthlyprojects_makebooking.Ui_makebooking_diag):

    def __init__(self, monthlyprojects_data, parent=None):
        super(MakeBookingDiag, self).__init__(parent)
        self.setupUi(self)
        self.tabActivated = self.bookingTypeTab.currentIndex()
        self.otb_notSameDay.setHidden(True)
        self.mib_buttonBox.children()[3].setEnabled(False)
        self.mp_data = monthlyprojects_data
        self.bookings_list = []
        self.booked_equipment = dict()

    @pyqtSignature("int")
    def on_bookingTypeTab_currentChanged(self, num):
        self.tabActivated = num

    # One Time Booking
    @pyqtSignature("QAbstractButton*")
    def on_otb_buttonBox_clicked(self, button):
        if self.otb_buttonBox.buttonRole(button) == 0:
            # AcceptRole
            self.buildXMLBookingOTB(self.tabActivated)
        elif self.otb_buttonBox.buttonRole(button) == 1:
            # RejectRole
            pass
        elif self.otb_buttonBox.buttonRole(button) == 7:
            # ResetRole
            pass
        elif self.otb_buttonBox.buttonRole(button) == 8:
            # ApplyRole
            pass

    @pyqtSignature("int")
    def on_otb_sameDay_stateChanged(self, onOrOff):
        if onOrOff:
            pass
        else:
            #Unchecked
            print onOrOff


    # Weekly Bookings
    @pyqtSignature("QAbstractButton*")
    def on_wb_buttonBox_clicked(self, button):
        if self.wb_buttonBox.buttonRole(button) == 0:
            # Accept Role
            self.buildXMLBookingWB(self.tabActivated)
        elif self.wb_buttonBox.buttonRole(button) == 1:
            # Reject Role
            pass
        elif self.wb_buttonBox.buttonRole(button) == 7:
            # Reset Role
            pass
        elif self.wb_buttonBox.buttonRole(button) == 8:
            # Apply Role
            pass

    # Multiple Instance Booking
    @pyqtSignature("QAbstractButton*")
    def on_mib_buttonBox_clicked(self, button):
        if self.mib_buttonBox.buttonRole(button) == 0:
            # Accept Role
            self.buildXMLBookingMIB(self.tabActivated)
        elif self.mib_buttonBox.buttonRole(button) == 1:
            pass
        elif self.mib_buttonBox.buttonRole(button) == 7:
            # Reset Role
            pass
        elif self.mib_buttonBox.buttonRole(button) == 8:
            pass

    @pyqtSignature("")
    def on_mib_addNewDate_clicked(self):
        """Adds the booking to the list in this view"""
        self.mib_buttonBox.children()[3].setEnabled(True)
        new_booking = {"TICKET#": self.get_ticket_num(self.tabActivated),
                       "CLIENT": self.get_client_name(self.tabActivated),
                       "DATEIN": self.get_date_in(self.tabActivated),
                       "DATEOUT": self.get_date_out(self.tabActivated),
                       "TIMEIN": self.get_time_in(self.tabActivated),
                       "TIMEOUT": self.get_time_out(self.tabActivated),
                       "SETUPTYPE": self.get_setup_type(self.tabActivated),
                       "SETUPLOCAT": self.get_setup_location(self.tabActivated),
                       "NOTES": self.get_notes(self.tabActivated),
                       "TECHASSIGN": self.get_tech_assigned(self.tabActivated),
                       "EQUIPMENT": self.get_equipment_needed(self.tabActivated)}
        self.bookings_list.append(Booking(new_booking))
        item = QListWidgetItem(QString("%1 - %2 (%3-%4) %5")
                               .arg(self.bookings_list[len(self.bookings_list)-1]
                                    .get_clientName())
                               .arg(self.bookings_list[len(self.bookings_list)-1]
                                    .get_setupLocation())
                               .arg(self.bookings_list[len(self.bookings_list)-1]
                                    .get_timeIn())
                               .arg(self.bookings_list[len(self.bookings_list)-1]
                                    .get_timeOut())
                               .arg(self.booking_list[len(self.bookings_list)-1]
                                    .get_date_out()))
        self.mib_listView.addItem(item)

    @pyqtSignature("")
    def on_mib_removeNewDate_clicked(self):
        """Removes the selected booking from the list in this view"""
        newDateFocused = self.mib_listView.selectedItems()
        for items in newDateFocused:
            self.mib_listView.takeItem(self.mib_listView.row(items))


    @pyqtSignature("QListWidgetItem*")
    def on_mib_listView_itemClicked(self, mib_listItem):
        """Gets the member in the list and replicate the selected item data in the form"""
        item_names = ["TICKET#", "CLIENT", "DATEIN", "DATEOUT", "TIMEIN",
                      "TIMEOUT", "SETUPTYPE", "SETUPLOCAT", "NOTES", "TECHASSIGN",
                      "EQUIPMENT"]

        index = self.mib_listView.indexFromItem(mib_listItem).row()
        booking_in_question = self.bookings_list[index]
        self.mib_ticketNumInput.setText(booking_in_question.get_ticketNum())

        self.mib_clientNameInput.setText(booking_in_question.get_clientName())

        if booking_in_question.get_setupType() == "PICKUP":
            self.mib_pickup.setChecked(True)
        elif booking_in_question.get_setupType() == "SETUP":
            self.mib_setup.setChecked(True)
        elif booking_in_question.get_setupType() == "COUNCILRMSETUP":
            self.mib_councilRoomSetup.setChecked(True)
        elif booking_in_question.get_setupType() == "COUNCILRMSTAY":
            self.mib_councilRoomStay.setChecked(True)

        self.mib_techAssignedInput.setText(booking_in_question.get_techAssigned())

        self.mib_setupLocationInput.setText(booking_in_question.get_setupLocation())

        # TODO: Equipment

    @pyqtSignature("int")
    def on_mib_equipment_currentIndexChanged(self, int):
        self.add_equipment(self.mib_equipment.currentText())

    @pyqtSignature("int")
    def on_wb_equipment_currentIndexChanged(self,int):
        self.add_equipment(self.wb_equipment.currentText())

    @pyqtSignature("int")
    def on_otb_equipment_currentIndexChanged(self,int):
        self.add_equipment(self.otb_equipment.currentText())

    def add_equipment(self, equip_type):
        dialog = monthlyprojects_equipment.Equipment(equip_type=equip_type)
        if dialog.exec_():
            QMessageBox.information(self, "{} has been booked".format(equip_type))
        else:
            pass

    def accept(self):
        # One Time Booking
        if self.tabActivated == 0:
            self.buildXMLBookingOTB(self.tabActivated)
        # Weekly Booking
        if self.tabActivated == 1:
            self.buildXMLBookingMIB(self.tabActivated)
        # Multiple Instance Bookings
        if self.tabActivated == 2:
            self.buildXMLBookingWB(self.tabActivated)

    def contains(self, value, holder):
        # Only works with lists at the moment
        for i in holder:
            if i == value:
                return True
        return False

    def buildXMLBookingOTB(self, tab):
        detailtags = ["ReservedBy", "Date", "Name", "Time", "Out", "SetUppickUp",
                      "SetupLocation", "RequestDetail", "Status", "TechAssigned",
                      "Department", "Function", "Laptop", "Projector", "Screen",
                      "Speakers", "Microphone", "VGACable", "ExtensionSurge",
                      "DVDPlayer", "VCR", "TwentyOneInchMonitor", "PASystem",
                      "VideoRecording", "DocCam", "Mics", "PlasmaScreens", "PlasmaScreenStand"]
        try:
           date_to_append_booking = self.monthlyprojects_data.\
               xpath("/MonthlyProjects/EntryDate[@date='{}']"
                     .format(QDate(self.get_date_out().year(),
                                   self.get_date_out().month(),
                                   self.get_date_out().day()).toPyDate().date.isoformat()))
        except Exception:
            date_to_append_booking =  []
        booking = etree.Element("Ticket", number=self.get_ticket_num(tab=tab))

        for i, tags in enumerate(detailtags):
            tag = etree.Element(detailtags[i])
            if tags == "ReservedBy":
                tag.text = "Danuel"
            elif tags == "Name":
                tag.text = self.get_client_name(tab=tab)
            elif tags == "Time":
                tag.text = self.get_time_out(tab=tab).toString(format= "H:m AP")
            elif tags == "Out":
                if len(date_to_append_booking) != 0:
                    if self.get_time_in(tab=tab).toPyTime().isoformat() \
                            == date_to_append_booking.attrib['date'][:10]:
                        tag.text = self.get_time_in(tab=tab).toString(format= "H:m AP")
                    else:
                        tag.text = self.get_time_in().toString(format="H:m AP")
                else:
                    if self.get_time_in(tab=tab).date().toPyTime().isoformat() \
                            == self.get_time_out(tab=tab).toPyTime().isoformat():
                        tag.text = self.get_time_in().toString(format="H:m AP")
                    else:
                        tag.text = self.get_time_in().toPyTime().isoformat()
            elif tags == "SetUppickUp":
                tag.text = self.get_setup_type(tab=tab)
            elif tags == "SetupLocation":
                tag.text = self.get_setup_location(tab=tab)
            elif tags == "RequestDetail":
                tag.text = self.get_notes(tab=tab)
            elif tags == "TechAssigned":
                tag.text = self.get_tech_assigned(tab=tab)
            else:
                pass
            booking.append(tag)

        if len(date_to_append_booking) == 0:
            entrydates = self.mp_data.xpath("/MonthlyProjects/EntryDate")
            a_day = datetime.timedelta(days=1)
            for entrydate in entrydates:
                date = entrydate.attrib["date"][:10].split('-')
                date = datetime(int(date[0]), int(date[1]), int(date[2]))
                if self.get_date_out().date() < date.date():
                    date_minus_day = date.date() - a_day
                    if date_minus_day.isoformat() == self.get_date_out(tab=tab)\
                            .toPyTime()\
                            .isoformat():
                        entrydatewrapper = etree.Element("EntryDate",
                                                         date=self.get_date_out(tab=tab)
                                                         .toPyTime()
                                                         .isoformat())
                        entrydatewrapper.append(booking)
                        entrydate.addprevious(entrydatewrapper)
                        break
                    elif entrydates.index(entrydate) == 0:
                        entrydate.addprevious(booking)
                        break
                else:
                    date_plus_day = date.date() + a_day
                    if date_plus_day.isoformat() == self.get_time_out(tab=tab).toPyTime().isoformat():
                        entrydate.append(booking)
                        break
                    elif entrydates.index(entrydate) == len(entrydate)-1:
                        entrydatewrapper = etree.Element("EntryDate",
                                                         date=self.get_time_out()
                                                         .isoformat())
                        entrydatewrapper.append(booking)
                        entrydate.addnext(entrydatewrapper)
                        break
            else:
                date_to_append_booking[0].append(booking)
            self.write_to_xml(self.mp_data)
            monthlyprojects_equipment.write_to_xml()

    def buildXMLBookingWB(self, tab):
        detailtags = ["ReservedBy", "Date", "Name", "Time", "Out", "SetUppickUp",
                      "SetupLocation", "RequestDetail", "Status", "TechAssigned",
                      "Department", "Function", "Laptop", "Projector", "Screen",
                      "Speakers", "Microphone", "VGACable", "ExtensionSurge",
                      "DVDPlayer", "VCR", "TwentyOneInchMonitor", "PASystem",
                      "VideoRecording", "DocCam", "Mics", "PlasmaScreens", "PlasmaScreenStand"]
        DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        def retrieve_dates(start_end_dates, days):
            if len(start_end_dates) == 2:
                date = start_end_dates[0]
                date_range = []
                cnt=0
                while date <= start_end_dates[1]:
                    try:
                        if self.contains(DAYS[DAYS.index(date.toString('dddd'))].upper(), days):
                            date_range.append(date)
                    except ValueError:
                        print "Day was not in range" # If the date doesn't exist in the list
                    finally:
                        date = date.addDays(1)                 #Add a day to check the next day
                        cnt += 1
            else:
                raise ValueError
            return date_range

        dates_booked = retrieve_dates([self.get_date_out(tab=tab), self.get_date_in(tab=tab)],
                                      self.get_days_booked(tab=tab))
        time_in_details = self.get_time_in(tab)
        time_out_details = self.get_time_out(tab)

        for date in dates_booked:
            try:
                query_date= date.toPyDate()
                query_date= datetime(query_date.year,query_date.month,query_date.day)
                date_to_append_booking = self.mp_data.\
                    xpath("/MonthlyProjects/EntryDate[@date='{}']"
                          .format(query_date.isoformat()))
            except Exception:
                date_to_append_booking = []             #Date does not exist
            booking = etree.Element("Ticket", number=self.get_ticket_num(tab=tab))

            for i, tags in enumerate(detailtags):
                tag = etree.Element(detailtags[i])
                if tags == "ReservedBy":
                    tag.text = "Danuel Williams"
                    booking.append(tag)
                elif tags == "Name":
                    tag.text = self.get_client_name(tab=tab)
                    booking.append(tag)
                elif tags == "Time":
                    for day in DAYS:
                        if date.toString('dddd') == day:
                            tag.text = unicode(time_in_details[day.upper()].toString('h:mm AP'))
                            booking.append(tag)
                        else:
                            continue
                elif tags == "Out":
                    for day in DAYS:
                        if date.toString('dddd') == day:
                            tag.text = unicode(time_out_details[day.upper()].toString('h:m AP'))
                            booking.append(tag)
                        else:
                            continue
                elif tags == "SetUppickUp":
                    tag.text = self.get_setup_type(tab=tab)
                    booking.append(tag)
                elif tags == "SetupLocation":
                    tag.text = self.get_setup_location(tab=tab)
                    booking.append(tag)
                elif tags == "RequestDetail":
                    tag.text = self.get_notes(tab=tab)
                    booking.append(tag)
                elif tags == "TechAssigned":
                    tag.text = self.get_tech_assigned(tab=tab)
                    booking.append(tag)
                    # Equipment based stuff
            if len(date_to_append_booking) == 0:
                entrydates = self.mp_data.xpath("/MonthlyProjects/EntryDate")
                a_day = datetime.timedelta(days=1)
                for entrydate in entrydates:
                    xml_date = entrydate.attrib["date"][:10].split('-')
                    xml_date = datetime(int(date[0]), int(date[1]), int(date[2]))
                    if date < xml_date.date():
                        date_minus_day = xml_date.date - a_day
                        if date_minus_day.isoformat() == date.toPyTime().isoformat():
                            entrydatewrapper = etree.Element("EntryDate",
                                                             date=date
                                                             .toPyDate()
                                                             .isoformat())
                            entrydatewrapper.append(booking)
                            entrydate.addprevious(entrydatewrapper)
                            break
                        elif entrydates.index(entrydate) == 0:
                            entrydate.addprevious(booking)
                            break
                    else:
                        date_plus_day = xml_date.date + a_day
                        if date_plus_day.isoformat == date.toPyDate().isoformat():
                            entrydate.append(booking)
                            break
                        elif entrydates.index(entrydate) == len(entrydate)-1:
                            entrydatewrapper = etree.Element("EntryDate",
                                                             date= date
                                                             .toPyDate()
                                                             .isoformat())
                            entrydatewrapper.append(booking)
                            entrydate.addnext(entrydatewrapper)
                            break
            else:
                date_to_append_booking[0].append(booking)
        self.write_to_xml(self.mp_data)

    def buildXMLBookingMIB(self, tab):
        booking = etree.Element("Ticket", number=self.get_ticket_num(tab=tab))
        detailtags = ["ReservedBy", "Date", "Name", "Time", "Out", "SetUppickUp",
                      "SetupLocation", "RequestDetail", "Status", "TechAssigned",
                      "Department", "Function", "Laptop", "Projector", "Screen",
                      "Speakers", "Microphone", "VGACable", "ExtensionSurge",
                      "DVDPlayer", "VCR", "TwentyOneInchMonitor", "PASystem",
                      "VideoRecording", "DocCam", "Mics", "PlasmaScreens", "PlasmaScreenStand"]
        for i, tags in enumerate(detailtags):
            tag = etree.Element(detailtags[i])
            if tags == "ReservedBy":
                pass
            elif tags == "Name":
               pass
            elif tags == "Time":
                pass
            elif tags == "Out":
                pass
            elif tags == "SetUppickUp":
                pass
            elif tags == "SetupLocation":
                pass
            elif tags == "RequestDetail":
                pass
            elif tags == "TechAssigned":
                pass
            #Equipment based stuff

    @staticmethod
    def write_to_xml(data):
        xml_datastore = open('MonthlyProjects(ResultingTestingPurposes).xml', 'w')
        xml_datastore.write(etree.tostring(data, pretty_print=True))
        xml_datastore.close()

    def get_ticket_num(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return unicode(self.otb_ticketNumInput.text())
            elif tab == 1:
                return unicode(self.wb_ticketNumInput.text())
            elif tab == 2:
                return unicode(self.mib_ticketNumInput.text())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_client_name(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return unicode(self.otb_clientNameInput.text())
            elif tab == 1:
                return unicode(self.wb_clientNameInput.text())
            elif tab == 2:
                return unicode(self.mib_clientNameInput.text())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_setup_location(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return unicode(self.otb_setupLocationInput.text())
            elif tab == 1:
                return unicode(self.wb_setupLocationInput.text())
            elif tab == 2:
                return unicode(self.mib_setupLocationInput.text())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_date_in(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                if self.isSameDayReturn():
                    return QDate(self.otb_dateStart.date())
                else:
                    return QDate(self.otb_dateEnd.date())
            elif tab == 1:
                return QDate(self.wb_dateEnd.date())
            elif tab == 2:
                return QDate(self.mib_dateStart.date())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_date_out(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return QDate(self.otb_dateOut.date())
            elif tab == 1:
                return QDate(self.wb_dateStart.date())
            elif tab == 2:
                return QDate(self.mib_dateEnd.date())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_time_out(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return self.otb_timeOut.time()
            elif tab == 1:
                times = dict()
                days_checked = self.get_days_booked(tab)
                for day in days_checked:
                    if day == "MONDAY":
                        times.update([(day, self.wb_timeOutMonday.time())])
                    elif day == "TUESDAY":
                        times.update([(day, self.wb_timeOutTuesday.time())])
                    elif day == "WEDNESDAY":
                        times.update([(day, self.wb_timeOutWednesday.time())])
                    elif day == "THURSDAY":
                        times.update([(day, self.wb_timeOutThursday.time())])
                    elif day == "FRIDAY":
                        times.update([(day, self.wb_timeOutFriday.time())])
                    else:
                        raise ValueError
                return times
            elif tab == 2:
                return self.mib_timeOut.time()
            else:
                raise ValueError
        else:
            raise TypeError

    def get_time_in(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return self.otb_timeIn.time()
            elif tab == 1:
                times = dict()
                days_checked = self.get_days_booked(tab)
                for day in days_checked:
                    if day == "MONDAY":
                        times.update([(day, self.wb_timeInMonday.time())])
                    elif day == "TUESDAY":
                        times.update([(day, self.wb_timeInTuesday.time())])
                    elif day == "WEDNESDAY":
                        times.update([(day, self.wb_timeInWednesday.time())])
                    elif day == "THURSDAY":
                        times.update([(day, self.wb_timeInThursday.time())])
                    elif day == "FRIDAY":
                        times.update([(day, self.wb_timeInFriday.time())])
                    else:
                        raise ValueError
                return times
            elif tab == 2:
                # TODO: Revise to work with Booking model
                return self.mib_timeIn.time()
            else:
                return ValueError
        else:
            return TypeError


    def get_days_booked(self, tab):
        days = [self.wb_monday, self.wb_tuesday,
                self.wb_wednesday, self.wb_thursday,
                self.wb_friday]
        day_names = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        days_checked = []
        if isinstance(tab, int):
            if tab == 1:
                for day in days:
                    if day.isChecked():
                        days_checked.append(day_names[days.index(day)])
                return days_checked
            else:
                # Cannot call days booked on tabs other than weekly booking tab
                return ValueError
        else:
            raise TypeError

    def get_setup_type(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                if self.otb_pickup.isChecked() and not self.otb_setup.isChecked():
                    return "PICKUP"
                elif not self.otb_pickup.isChecked() and self.otb_setup.isChecked():
                    return "SETUP"
            elif tab == 1:
                if self.wb_setup.isChecked() and not self.wb_pickup.isChecked():
                    return "PICKUP"
                elif not self.wb_pickup.isChecked() and self.wb_pickup.isChecked():
                    return "SETUP"
            elif tab == 2:
                setup_types = [self.mib_setup, self.mib_pickup,
                               self.mib_councilRoomSetup, self.mib_councilRoomStay]
                checked = None
                for i in setup_types:
                    if i.isChecked():
                        checked = setup_types.pop(setup_types.index(i))
                        for j in setup_types:
                            if j.isChecked():
                                raise ValueError
                if checked == self.mib_setup:
                    return "SETUP"
                elif checked == self.mib_pickup:
                    return "PICKUP"
                elif checked == self.mib_councilRoomSetup:
                    return "COUNCILRMSETUP"
                elif checked == self.mib_councilRoomStay:
                    return "COUNCILRMSTAY"
                else:
                    raise ValueError("Setup Type Not checked / Setup Type Value Invalid")
            else:
                raise ValueError("No Such tab: {}".format(tab))
        else:
            raise TypeError

    def get_equipment_needed(self, tab):
        # TODO: Based on combo box choices and integration with inventory
        if isinstance(tab, int):
            if tab == 0:
                return "Under Construction"
            elif tab == 1:
                return "Under Construction"
            elif tab == 2:
                return "Under Construction"
            else:
                raise ValueError
        else:
            raise TypeError

    def get_notes(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return unicode(self.otb_notes.toPlainText())
            elif tab == 1:
                return unicode(self.wb_notes.toPlainText())
            elif tab == 2:
                return unicode(self.mib_notes.toPlainText())
            else:
                raise ValueError
        else:
            raise TypeError

    def get_tech_assigned(self, tab):
        if isinstance(tab, int):
            if tab == 0:
                return unicode(self.otb_techAssignedInput.text())
            elif tab == 1:
                return unicode(self.wb_techAssignedInput.text())
            elif tab == 2:
                return unicode(self.mib_techAssignedInput.text())
            else:
                raise ValueError
        else:
            raise TypeError

    def isSameDayReturn(self):
        return self.otb_sameDay

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("cleanlooks")
    form = MakeBookingDiag(None)
    form.show()
    app.exec_()


