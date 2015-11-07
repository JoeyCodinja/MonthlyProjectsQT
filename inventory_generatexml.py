__author__ = 'Danuel'


from openpyxl import load_workbook
from lxml import etree

#EQUIPMENT_CHECK_FLAGS
MISSING = 50
DEPLOYED = 01
AVAILABLE = 00
INOPERABLE = 02
UNKNOWN = 51


def get_headings(worksheet):
    row_headings = []
    headings = []
    for cnt, row in enumerate(worksheet['A1':'G52']):
        if cnt == 10:
            # Laptops
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                else:
                    headings.append(cell.value) # saved since most of the values are in the first titular row
                    row_headings[0].append(cell.value)
        if cnt == 19:
            # Projectors
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[1].append(cell.value)
                else:
                    row_headings[1].append(headings[cnt1-1])
        if cnt == 30:
            # Projection Screens
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[2].append(cell.value)
                else:
                    row_headings[2].append(headings[cnt1-1])
        if cnt == 36:
            # Speakers
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[3].append(cell.value)
                else:
                    row_headings[3].append(headings[cnt1-1])
        if cnt == 42:
            # Document Camera
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[4].append(cell.value)
                else:
                    row_headings[4].append(headings[cnt1-1])

        if cnt == 46:
            # DVD Player
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[5].append(cell.value)
                else:
                    row_headings[5].append(headings[cnt1-1])
        if cnt == 49:
            # VCR
            for cnt1, cell in enumerate(row):
                if cnt1 == 0:
                    row_headings.append([cell.value])
                elif cell.value is not None:
                    row_headings[6].append(cell.value)
                else:
                    row_headings[6].append(headings[cnt1-1])
    return row_headings



def traverse_worksheet(sheet):
    """Traverses the given worksheet"""
    laptops = {}
    projectors = {}
    projection_screens = {}
    speakers = {}
    document_cameras = {}
    dvd_players = {}
    vcrs = {}

    for cnt, row in enumerate(sheet.rows):
        if cnt > 10 and cnt <= 17:
            if status_tag(row[3].value) != DEPLOYED:
                laptops.update({row[0].value: {"model": row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value)}})
            else:
                laptops.update({row[0].value: {"model":row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value),
                                               "deployedto": row[4].value,
                                               "ticket": row[5].value}})
        if cnt >= 20 and cnt <=28:
            if status_tag(row[3].value) != DEPLOYED:
                projectors.update({row[0].value: {"model": row[1].value,
                                                  "servicetag": row[2].value,
                                                  "status": status_tag(row[3].value)}})
            else:
                projectors.update({row[0].value: {"model":row[1].value,
                                                  "servicetag": row[2].value,
                                                  "status": status_tag(row[3].value),
                                                  "deployedto": row[4].value,
                                                  "ticket": row[5].value}})
        if cnt >= 31 and cnt <= 34:
            if status_tag(row[3].value) != DEPLOYED:
                projection_screens.update({row[0].value: {"model": row[1].value,
                                                          "servicetag": row[2].value,
                                                          "status": status_tag(row[3].value)}})
            else:
                projection_screens.update({row[0].value: {"model":row[1].value,
                                                          "servicetag": row[2].value,
                                                          "status": status_tag(row[3].value),
                                                          "deployedto": row[4].value,
                                                          "ticket": row[5].value}})
        if cnt >= 37 and cnt <= 40:
            if status_tag(row[3].value) != DEPLOYED:
                speakers.update({row[0].value: {"model": row[1].value,
                                                "servicetag": row[2].value,
                                                "status": status_tag(row[3].value)}})
            else:
                speakers.update({row[0].value: {"model":row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value),
                                               "deployedto": row[4].value,
                                               "ticket": row[5].value}})
        if cnt >= 43 and cnt <= 44:
            if status_tag(row[3].value) != DEPLOYED:
                document_cameras.update({row[0].value: {"model": row[1].value,
                                                        "servicetag": row[2].value,
                                                        "status": status_tag(row[3].value)}})
            else:
                document_cameras.update({row[0].value: {"model":row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value),
                                               "deployedto": row[4].value,
                                               "ticket": row[5].value}})
        if cnt == 47:
            if status_tag(row[3].value) != DEPLOYED:
                dvd_players.update({row[0].value: {"model": row[1].value,
                                                   "servicetag": row[2].value,
                                                   "status": status_tag(row[3].value)}})
            else:
                dvd_players.update({row[0].value: {"model":row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value),
                                               "deployedto": row[4].value,
                                               "ticket": row[5].value}})
        if cnt >= 50 and cnt <=51:
            if status_tag(row[3].value) != DEPLOYED:
                vcrs.update({row[0].value: {"model": row[1].value,
                                            "servicetag": row[2].value,
                                            "status": status_tag(row[3].value)}})
            else:
                vcrs.update({row[0].value: {"model":row[1].value,
                                               "servicetag": row[2].value,
                                               "status": status_tag(row[3].value),
                                               "deployedto": row[4].value,
                                               "ticket": row[5].value}})

    return dict(laptop=laptops, projector=projectors,
                projection_screen=projection_screens,
                speaker=speakers, document_camera=document_cameras,
                dvd_player=dvd_players, vcr=vcrs)

def toXML(data):
    root = etree.Element("Inventory")
    laptops = etree.Element("Laptops")
    projectors = etree.Element("Projectors")
    projection_screens = etree.Element("ProjectionScreens")
    speakers = etree.Element("Speakers")
    document_camera = etree.Element("DocumentCameras")
    dvd_player = etree.Element("DVDPlayers")
    vcr = etree.Element("VCRs")

    def createTag(key, key_data, item):
        tag = etree.Element(key.__str__()[0].upper()+key.__str__()[1:])
        tag.text = item
        for details in key_data:
            if isinstance(key_data[details], unicode):
                text = key_data[details].replace(" ", "")
                tag.set(details, unicode(text))
            else:
                tag.set(details, unicode(key_data[details]))
        return tag

    for key in data.keys():
        if key == 'laptop':
            for item in data[key]:
                laptops.append(createTag(key, data[key][item], item=item))
        elif key =='projector':
            for item in data[key]:
                projectors.append(createTag(key, data[key][item], item=item))
        elif key =='projection_screen':
            for item in data[key]:
                projection_screens.append(createTag(key, data[key][item], item=item))
        elif key == 'speaker':
            for item in data[key]:
                speakers.append(createTag(key, data[key][item], item=item))
        elif key == 'document_camera':
            for item in data[key]:
                document_camera.append(createTag(key, data[key][item], item=item))
        elif key == 'dvd_player':
            for item in data[key]:
                dvd_player.append(createTag(key, data[key][item], item=item))
        elif key == 'vcr':
            for item in data[key]:
                vcr.append(createTag(key, data[key][item], item=item))

    root.append(laptops)
    root.append(projectors)
    root.append(projection_screens)
    root.append(document_camera)
    root.append(speakers)
    root.append(dvd_player)
    root.append(vcr)
    return root

def write_xml_to_file(xml_data):
    file = open("EquipInventory.xml", 'w')
    file.write(etree.tostring(xml_data, pretty_print=True))
    file.close()


def status_tag(string):
    if string == "Here" or string == 'here':
        return AVAILABLE
    elif string == "N/W" or string == "Not Working":
        return INOPERABLE
    elif string == "Deployed":
        return DEPLOYED
    elif string == "Stolen" or string == "Missing":
        return MISSING
    else:
        return UNKNOWN

def load_inventory_sheet(workbook):
    """Returns the most recent inventory done in the Excel workbook"""
    sheets = workbook.get_sheet_names()
    return workbook[sheets[-1]]

directory = "Monthly Projects 2014.xlsx"
mth_wb = load_workbook(filename=directory, read_only=True)
inventory_sheet = load_inventory_sheet(mth_wb)
headings = get_headings(inventory_sheet)
inventory_data = traverse_worksheet(inventory_sheet)
xml_data = toXML(inventory_data)
write_xml_to_file(xml_data=xml_data)
