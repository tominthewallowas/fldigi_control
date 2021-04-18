#!/usr/bin/python
# -*- coding: utf-8 -*-

# sqlitedb.py

import sqlite3

class SQLiteDB():

        def __init__(self, db_type=':memory:'):
                self.db = sqlite3.connect(db_type)
                # ~ self.db.row_factory = sqlite3.Row
                self.cur = self.db.cursor()

        def createTable(self, statement):
                self.db.execute(statement)
        
        def insertData(self, statement, data):
                self.db.executemany(statement, data)
                self.db.commit()

        def select(self, statement):
                self.cur.execute(statement)
                return self.cur.fetchall()

        def dropTable(self, table_name):
                self.db.execute('drop table ' + table_name)

        def updateData(self, statement, values):
                result = self.db.execute(statement, values)
                self.db.commit()
                return result

        def selectwithparm(self, sql, parm):
                self.cur.execute(sql, parm)
                return self.cur.fetchall()
        
        def deleteRow(self, sql, table_id):
                self.cur.execute(sql, table_id)
                self.db.commit()

        def getColumnNames(self, statement):
                self.cur.execute(statement)
                r = self.cur.fetchone()
                return r.keys()

        def __del__(self):
                self.db.close()

if __name__ == '__main__':
        sld = SQLiteDB()
        create_table = 'create table brag(id integer primary key, call text, band text, qso_date date)'
        sld.createTable(create_table)
        insert_statement = 'insert into brag(call, band, qso_date) values (?, ?, ?)'
        insert_data = [('K8JD', '20M', 20141002), ('KI5IO', '10M', 20141123)]
        sld.insertData(insert_statement, insert_data)
        select_statement = 'select * from brag'
        rows = sld.select(select_statement)
        print('---- Result after create table and insert data ----')
        print(rows)
        tablename = 'brag'
        column = 'call'
        primarykey = 'id'
        update_statement = "UPDATE %s SET %s=? WHERE %s = ?" % (tablename, column, primarykey)
        print(update_statement)
        update_values = ('AB7WXZ', 1)
        result = sld.updateData(update_statement, update_values)
        print('---- Result after update ----')
        rows = sld.select(select_statement)
        print(rows)
        sld.dropTable('brag')
