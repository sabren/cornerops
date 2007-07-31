"""
cornerhost control panel configuration file.
modify this to fit your own site and table names.
"""
from clerks import Clerk, Schema
from storage import MySQLStorage
from cornerhost import *
from cornerhost.dbmap import DBMAP
schema = Schema(DBMAP)

def makeClerk():
    import sqlCornerhost
    return Clerk(MySQLStorage(sqlCornerhost.connect()), schema)

