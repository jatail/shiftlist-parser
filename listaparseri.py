# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jiltanen -at- kapsi -piste- fi> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return
# ----------------------------------------------------------------------------

from tabula import read_pdf
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
from icalendar import Calendar, Event

class vuoro:
    def __init__(self, start, end, description):
        self.start = start
        self.end = end
        self.description = description

def dutylistparser(file, year, month):
    dfs = read_pdf(file, pages=1)
    df = pd.concat(dfs)

    vuorot = []

    new = True
    for index, row in df.iterrows():
        dutyfield = str(row['Duty Start End'])
        if new == False:
            descriptiontext = descriptiontext + ' ' + str(row['Length Rest after Activity sequence'])
        else:
            descriptiontext = str(row['Length Rest after Activity sequence'])
        if 'Duty' in dutyfield:
            new = False
            militimestring = dutyfield[-4:]
            hours = int(militimestring[:2])
            minutes = int(militimestring[-2:])
            try:
                day = int(row['Day'][:2])
                prevDay = day
            except TypeError:
                day = prevDay
            dateinfo_start = datetime(year, month, day, hours, minutes)
            start_utc = dateinfo_start.astimezone(timezone('UTC'))

        elif len(dutyfield) == 4:
            militimestring = dutyfield[-4:]
            hours = int(militimestring[:2])
            minutes = int(militimestring[-2:])
            dateinfo_end = datetime(year, month, day, hours, minutes)
            if dateinfo_end < dateinfo_start:
                dateinfo_end += timedelta(days=1)
                prevDay = day + 1
            end_utc = dateinfo_end.astimezone(timezone('UTC'))
            new = True
            tyovuoro = vuoro(start_utc, end_utc, descriptiontext)
            vuorot.append(tyovuoro)


    cal = Calendar()
    cal.add('prodid', '-//TYOVUOROT//')
    cal.add('version', '2.0')

    for i in vuorot:
        event = Event()
        event.add('name', 'Työvuoro')
        event.add('summary', 'Työvuoro')
        event.add('description', i.description)
        event.add('dtstart', i.start)
        event.add('dtend', i.end)
        cal.add_component(event)

    cal_string = cal.to_ical()
    return cal_string