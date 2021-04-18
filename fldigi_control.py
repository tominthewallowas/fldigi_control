#!/usr/bin/env python3

import os, sys
from datetime import datetime
from pytz import UTC
import sqlite3
import time

import pyfldigi


def main():
    cur = createDatabaseCursor()
    day_time = extractUTCDayTime()
    program_values = retrieveProgramValues(day_time, cur)
    if program_values:
        sendRadioCommands(program_values)
    # ~ else:
        # ~ print('Ooops!')

def sendRadioCommands(values):
    try:
        command_obj = pyfldigi.Client().rig
        time.sleep(1)
        command_obj.frequency = values[0]
        time.sleep(1)
        command_obj.mode = values[1]
        time.sleep(1)
        command_obj.bandwidth = values[2]
        time.sleep(1)
        del(command_obj)
        command_obj = pyfldigi.Client().modem
        time.sleep(1)
        command_obj.name = values[3]
        time.sleep(1)
        command_obj.carrier = values[4]
    except:
        print('******* ERROR: It appears that fldigi is not running! *******')

def retrieveProgramValues(day_time, cur):
    sql = 'select StationFrequency, Modulation, Bandwidth, Modem, CenterFrequency from programs where Active="Yes" and Day=? and UtcTime=?'
    result = cur.execute(sql, day_time)
    row = result.fetchone()
    return row

def createDatabaseCursor():
    con = sqlite3.connect('fldigi_control.db')
    cur = con.cursor()
    return cur
    
def extractUTCDayTime():
    ''' Use datetime retrieve the UTC date and time '''
    ''' Note: I will have test code in here to set hard code
        UTC date and time for testing. The production code
        is commented out. '''
    #Uncommment the line below and remove the test code for production!!
    utc_now = datetime.utcnow()
    #Testing code starts here
    # ~ a = datetime.strptime('2021-03-24 18:00', '%Y-%m-%d %H:%M')
    # ~ utc_now = a.astimezone(UTC)
    #Testing code ends here
    day = utc_now.strftime('%a')
    time = utc_now.strftime('%H:%M')
    return (day, time)

if __name__ == "__main__":
    main()
