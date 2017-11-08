#!/usr/bin/python
import MySQLdb
import sys

import os
from shutil import copy2

# Edit the quire to suit your need
SELECT_SQL = "SELECT sName from core_retailer_detail"
INSERT_SQL = "INSERT INTO test (name) VALUES %s"


# Edit the connection parameters to suit your need
def get_source_conn():
    try:
        # return MySQLdb.connect(host="localhost", user="root", passwd="nd@1331993", db="relorestapi")
        return MySQLdb.connect(host="localhost", user="root", passwd="p4ulp4ul", db="freelancer_relo_retailer")
    except MySQLdb.Error as e:
        print(e)
        return None


# Edit the connection parameters to suit your need
def get_dest_conn():
    try:
        # return MySQLdb.connect(host="localhost", user="root", passwd="nd@1331993", db="relorestapi")
        return MySQLdb.connect(host="localhost", user="root", passwd="p4ulp4ul", db="freelancer_relo")
    except MySQLdb.Error as e:
        print(e)
        return None

# Edit the connection parameters to suit your need
def get_dest_conn():
    try:
        return MySQLdb.connect(host="localhost", user="root", passwd="p4ulp4ul", db="utility")
    except:
        return None


def transfer(conn):
    def put(conn, names):
        cursor = conn.cursor()
        part = ""
        for n in names:
            part += "('"+n+"'), "
        counter = cursor.execute(INSERT_SQL % part.strip()[:-1])
        cursor.close()
        conn.commit()
        conn.close()
        return counter

    cursor = conn.cursor()
    cursor.execute(SELECT_SQL)
    names = []
    for row in cursor.fetchall():
        names.append(row[0])
    print(names)
    cursor.close()
    conn.close()

    print("Transfered %d records" % put(get_dest_conn(), names))


transfer(get_source_conn())
# We are done
sys.exit()