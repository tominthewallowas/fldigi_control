'''This file contains all the sql statements used in the app.'''

import app_constants as ac


def retrieveSQL(request):
    sql = ''
    if request == ac.SQL_SELECT_ALL:
        sql = "select Id, program, station, stationfrequency, modulation, bandwidth, modem, centerfrequency, day, utctime, active, notes from programs"
    elif request == ac.SQL_INSERT:
        sql = "INSERT INTO programs (program, station, stationfrequency, modulation, bandwidth, modem, centerfrequency, day, utctime, active, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif request == ac.SQL_DELETE:
        sql = "delete from programs where id = ?"
    elif request == ac.SQL_UPDATE:
        sql = "update programs set program = ?, station = ?, stationfrequency = ?, modulation = ?, bandwidth = ?, modem = ?, centerfrequency = ?, day = ?, utctime = ?, active = ?,  notes = ? where Id = ?"
    elif request == ac.RADIO_FREQUENCIES:
        sql = "select frequency from radio_frequencies"
    elif request == ac.CENTER_DATA_FREQUENCIES:
        sql = "select frequency from center_data_frequencies"
    elif request == ac.MODEMS:
        sql = "select modem from modems"
    elif request == ac.MODES:
        sql = "select mode from modes"
    elif request == ac.RADIO_STATIONS:
        sql = "select station from radio_stations"
    elif request == ac.BANDWIDTHS:
        sql = "select bandwidth from bandwidths"

    return sql
