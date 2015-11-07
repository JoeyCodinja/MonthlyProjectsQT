__author__ = 'Danuel'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_monthlyprojectsequipment
import inventory_generatexml
from lxml import etree



class Equipment(QDialog,
                ui_monthlyprojectsequipment.Ui_equipment_picker):
    def __init__(self, equip_type, parent=None):
        super(Equipment,self).__init__(parent)
        self.setupUi(self)
        self.equip_data = etree.parse("EquipInventory.xml")
        equip_type = equip_type.replace(' ', '') + 's'
        self.equip_type_list = self.equip_data.xpath("/Inventory/{}".format(equip_type.__str__()))[0]
        self.equipment_type.setText(equip_type)
        if not len(self.equip_type_list) == 0 or not self.equip_type_list is None:
            stringlist = QStringList()
            for equip_type in self.equip_type_list:
                # update the list with the equipment
                if int(equip_type.attrib['status']) == inventory_generatexml.AVAILABLE:
                    stringlist.append(equip_type.text)
            self.equipment_in_stock.addItems(stringlist)
        else:
            raise ValueError


    @pyqtSignature("QString")
    def on_equipment_in_stock_currentIndexChanged(self, string):
        """Marks the highlighted piece of equipment as """
        equip = self.equip_data.xpath("/Inventory/{}/{}[text()={}]".format(self.equipment_type.text(),
                                                                           self.equipment_text.text()[:-1],
                                                                           string.__str__()))
        equip.attrib['status'] = inventory_generatexml.DEPLOYED


    def write_to_xml(self):
        xml_datastore = open("EquipInventory.xml", 'w')
        xml_datastore.write(etree.tostring(self.equip_data, pretty_print=True))
        xml_datastore.close()


