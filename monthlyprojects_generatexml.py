from openpyxl import load_workbook


# Reserved By| Ticket | !Date! | Client Name | Time | None | Set up / pick up |
# Setup Location | Request Detail | Status | Tech Assigned | Department |
# Function | Laptop | Projector | Screen | Speakers | Microphone | VGA Cable|
# Extension/Surge | DVD Player | VCR | 21' Monitor | PA System | Video Recording |
# Doc Cam | Mics | Plasma Screens | Plasma Screen Stand | 

def check_rows(mth_ws):
    """ Checks the amount of rows on the fly """
    rows_in_worksheet = 0
    for row in mth_ws.rows:
        rows_in_worksheet += 1


def get_headings(mth_ws):
    """ Gets headings based on static row that is defined (Row 4) in the Monthly Projects.xlsx file"""
    headings_list = []
    for row in mth_ws['A4':'AC4']:
        for cell in row:
            #Sanitize by removing characters such as ':,.*#' among others
            new_cell = cell.value
            dirty_char = ':,.*#/'
            char_of_importance = "\'\""
            numbers = ['21',]
            char_replacements = ['Inch','Feet']
            number_replacements = ['TwentyOne']
            for i in range(0, len(dirty_char)):
                if new_cell is not None:
                    if i < len(char_of_importance):
                        new_cell = new_cell.replace(char_of_importance[i], char_replacements[i])
                    if numbers[1 % len(numbers)]:
                        new_cell = new_cell.replace(numbers[0], number_replacements[0])
                    new_cell = new_cell.replace(dirty_char[i], "")
            headings_list.append(new_cell)
    return headings_list




def traverseworksheet(mth_ws):
    """Traverses a given worksheet"""
    spreadsheet_data = []
    last_date = None

    for cnt, row in enumerate(mth_ws.rows):
        if cnt> 4:
            cellcount=0
            cellvalues = []
            for cnt, cell in enumerate(row):
                # try:
                if cellcount < 29:
                    if cellcount == 2:		                                        # Capturing the cell that might
                        if cell.value == None:                                      # have the date
                            cellvalues.append(last_date)
                        else:                                                       # Use the value of the date that
                            last_date = cell.value                                  # was saved before
                            cellvalues.append(cell.value)
                    else:
                        cellvalues.append(cell.value)
                else:
                    break
                cellcount+=1
            spreadsheet_data.append(cellvalues)
        cnt += 1
    return spreadsheet_data

# Resource function



def to_xml(ws_data,tags):
    """Transforms cell values to XML Entries"""
    from lxml import etree
    from datetime import timedelta, datetime, time
    from calendar import month_name

    day = timedelta(days = 1) # Representing a day

    root = etree.Element('MonthlyProjects')
    lastdate = None
    previous_date_entry = None
    for cnt, row in enumerate(ws_data):
        if isinstance(row[2], datetime):
            if row[2] == lastdate:                                                  # If the dates are equal there is
                dateentry = previous_date_entry                                     # no need to create a new tag for
            else:                                                                   # for the date
                if row[3] is None and row[4] is None and row[5] is None:
                    continue
                else:
                    dateentry = etree.Element('EntryDate', date=row[2].isoformat())
                    root.append(dateentry)
        elif isinstance(row[2], unicode):
            if (row[2][0].upper() + row[2][1:].lower()) in month_name:              # Special case for the
                                                                                    # Monthly separators
                continue
            else:       # If date is in any other format
                newdate = lastdate + day
                dateentry = etree.Element('EntryDate', date=newdate.isoformat())
        else:
            continue # Disregarding any rows that serve as separators
        if isinstance(row[1], int):
            ticket = etree.Element('Ticket', number=row[1].__str__())
            dateentry.append(ticket)                                                # Adds the ticket under the current
                                                                                    # date which it was booked under
        else:
            ticket = etree.Element('Ticket', number='none')
            dateentry.append(ticket)
        for cnt2, cell in enumerate(row):
            detailtags = etree.Element(tags[cnt2])
            if cnt2 != 2 and cnt2!= 1:                                              # Excluding the previously
                if cell is not None:                                                # extracted date and
                    if isinstance(cell, int):                                       # also the ticket #
                        detailtags.text = cell.__str__()
                    elif isinstance(cell, time):
                        detailtags.text = cell.strftime('%I:%M %p')
                    elif isinstance(cell, datetime):
                        detailtags.text = cell.time().strftime('%I:%M %p')
                    else:
                        detailtags.text = cell
                ticket.append(detailtags)
        if isinstance(row[2], datetime):
            lastdate = row[2]                                                       # If the date is in datetime format
            previous_date_entry = dateentry
        elif isinstance(row[2], unicode):
            lastdate = lastdate + day                                               # If the date is in text format
            previous_date_entry = dateentry
    return root

def tocamelcase(headings):
    """Configured to take a list, if not a list it should return an error"""
    import re

    pattern = ' ?'
    if isinstance(headings, list):
        newlist = []
        for cnt, i in enumerate(headings):
            if i is None:
                newlist.append('Out')
                continue
            i = i.strip()
            splitwords = re.split(pattern, i)
            for count, j in enumerate(splitwords):
                splitwords[count] = j[0].upper() + j[1:]
            newlist.append(''.join(splitwords))
    return newlist


def loadworkbook(filename):
    return load_workbook(filename=filename, read_only=True)

def loadworksheet(workbook, worksheet):
    return workbook[worksheet]

def load(filename, worksheet):
    workbook = loadworkbook(filename)
    return loadworksheet(workbook, worksheet)

if __name__ == "__main__":
    from lxml import etree

    mth_ws = load('Monthly Projects 2014.xlsx', 'Monthly Projects')
    spreadsheet_headings = get_headings(mth_ws)
    tags = tocamelcase(spreadsheet_headings)
    spreadsheet_data = traverseworksheet(mth_ws)
    xml_file = to_xml(spreadsheet_data, tags)
    f = open('MonthlyProjects.xml', 'w')
    f.write(etree.tostring(xml_file, pretty_print=True))
    f.close()