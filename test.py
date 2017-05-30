#!/usr/bin/python

from DBInterface import employeeDB
import MySQLdb

db = MySQLdb.connect("localhost","cab4employee","","cab4employee")
cursor = db.cursor()
data = {}
data['eid'] 		= "E01"
data['first_name'] 	= "Akshay"
data['last_name'] 	= "Venugopal"
data['date_of_reg'] = "2014-12-01"
data['contact_num'] = "7012779056"
data['account_id'] 	= "A01"
data['time_in']		= "9:30:00"
data['time_out'] 	= "5:30:00"
employeeDB.insertEmployee( cursor, data )
db.commit()
db.close()
