#!/usr/bin/env python3

'''
Print Schedule consists of reading all the rows from the fldigi_control sqlite3 database and
printing a report detailing the information within. It also adds two columns that report
the local time in standard or daylight time depending on the date.
'''

import sqlite3
import calendar
import pytz
import datetime

UTC_DAY_POS = 9
UTC_TIME_POS = 10

def main():
    print('print schedule')
    data = collectReportData()
    reportList = listifyTuples(data)
    reportList = addLocalDayTime(reportList)
    buildReport(reportList)

def addLocalDayTime(reportList):
    for report in reportList:
        local_day_time = deriveLocalDayTime((report[UTC_DAY_POS], report[UTC_TIME_POS]))
        report.append(local_day_time[0])
        report.append(local_day_time[1])
    return reportList

def deriveLocalDayTime(report):
    utc_now = datetime.datetime.utcnow()
    year = utc_now.year
    month = utc_now.month
    cal = calendar.monthcalendar(year, month)
    first_full_week = cal[1]
    dow = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dow_from_datasource = report[0]
    index = dow.index(dow_from_datasource)
    day = first_full_week[index]
    utc_time_from_datasource = report[1]
    lc = pytz.timezone('UTC')
    utc_time = datetime.datetime.strptime(str(year) + str(month) + str(day) + utc_time_from_datasource, '%Y%m%d%H:%M')
    lc_datetime = lc.localize(utc_time)
    pacific_time = lc_datetime.astimezone(pytz.timezone('US/Pacific'))
    local_dow_str = pacific_time.strftime('%a')
    local_time_str = pacific_time.strftime('%-I:%M %p')
    return (local_dow_str, local_time_str)

def buildReport(reportList):
    print_spacing = [(30, '<'),(4, '<'),(9, '>'),(1, '<'),(3, '<'),(5, '<'),(7, '<'),(5, '<'),(4, '<'),(4, '<'),(6, '<'),(4, '<'),(8, '>'),(0, '<')]
    #temporary file creation for development
    f = open('schedule_report.txt', 'w')

    print_str = 'Shortwave Broadcast Schedule\n'
    print_str += f'Print Date: {datetime.datetime.now():%B %d, %Y}\n\n'
    print_str += 'Program                       Stn      Freq Md BW   Modem  Cntr Atv UDy UTime LDy    LTime\n'
    print_str += '------------------------------------------------------------------------------------------\n'
    for line in reportList:
        for x, item in enumerate(line):
            print_str += f'{item:{print_spacing[x][1]}{print_spacing[x][0]}}'
            # ~ print_str += f'{item:20}'
        print_str += '\n\n'
    print_str += 'Stn = Station callsign\n'
    print_str += 'Freq = Station frequency in kHz\n'
    print_str += 'Md = Modulation mode (AM, FM, USB, LSB)\n'
    print_str += 'BW = Receiver bandwidth\n'
    print_str += 'Modem = Fldigi modem\n'
    print_str += 'Cntr = Fldigi center frequency\n'
    print_str += 'Act = Active\n'
    print_str += 'UDy = UTC day\n'
    print_str += 'UTime = UTC time\n'
    print_str += 'LDy = Local day\n'
    print_str += 'LTime = Local time'
    f.write(print_str)
    f.close()

def listifyTuples(data):
    reportList = [list(reportlist) for reportlist in data]
    return reportList

def collectReportData():
    con = sqlite3.connect('fldigi_control.db')
    cur = con.cursor()
    cur.execute('select Program, Station, StationFrequency, " " as Spacer, Modulation, Bandwidth, Modem, CenterFrequency, Active, Day, UtcTime from programs')
    data = cur.fetchall()
    return data

if __name__ == "__main__":
    main()
