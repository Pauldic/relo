#!/usr/bin/python
import MySQLdb
import sys

import os
from shutil import copy2

"""
Used for one time transfer of files
"""
ABS_IMAGE_PATH = "/USE/ABSOLUTE/PATH/TO/LOCATION/OF/THOSE/IMAGES/"
IMAGE_TYPES = ['.gif', '.png', '.jpg', '.jpeg']
DB_IMAGE_PATH = "documents/"
DESTINATION_DIRECTORY = '/ABSOLUTE/PATH/OF/THE/DESTINATION/IMAGES/'


# Get MySQL Connection
def get_conn():
    try:
        # return MySQLdb.connect(host="...", user="...", passwd="....", db="....")
        return MySQLdb.connect(host="...", user="...", passwd="....", db=".....")
    except MySQLdb.Error as e:
        print(e)
        return None


# Update the table core_retailer_detail.
def update_record_image_path(conn, db_path, id, filename):
    # print("%s    %s    %s" % (db_path, id, filename))
    sql = "UPDATE .... SET slogo='%s' WHERE id=%d" %(db_path, id)
    cursor = conn.cursor()
    counter = cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    if counter > 0:
        copy2(ABS_IMAGE_PATH+filename, DESTINATION_DIRECTORY)


# Search for the Image files in the Absolute path and use the name to update the table
for f in os.listdir(ABS_IMAGE_PATH):
    ext = os.path.splitext(f)[1]
    if ext.lower() in IMAGE_TYPES:
        try:
            _fname = os.path.splitext(f)[0].split("/")[-1] if len(os.path.splitext(f)[0].split("/")) > 1 else os.path.splitext(f)[0]
            filename = _fname + ext
            path = DB_IMAGE_PATH+_fname + ext
            update_record_image_path(get_conn(), path, int(_fname), _fname+ext)
            print("Updated '%s' to '%s' in the database" % (os.path.splitext(f)[0]+os.path.splitext(f)[1], os.path.splitext(f)))
        except ValueError:
            print("Skipping '%s' because image name is not an int" % os.path.splitext(f)[0]+os.path.splitext(f)[1])

# We are done
sys.exit()