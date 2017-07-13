def insertEmployeeAddress( cursor, data ):
	sql = "insert into employee_address values( \"" + \
			data['eid']			+ "\" ,\"" 	+ 	\
			data['house_num']	+ "\" ,\"" 	+ 	\
			data['street_name'] + "\" ,\""	+ 	\
			data['postal_code'] + "\" ,\"" 	+	\
			data['city'] 		+ "\" ) "
	cursor.execute( sql )

def getEmployeeAddress( cursor, eid ):
	sql = "select * from employee_address where eid=\"" + eid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return None
	row = cursor.fetchone()
	data['eid'] 		= str( row[0] )
	data['house_num'] 	= str( row[1] )
	data['street_name'] = str( row[2] )
	data['city'] 		= str( row[3] )
	data['postal_code'] = str( row[4] )
	return data

def getDistinctPostalCodes( cursor, eid ):
	sql = "select distinct postal_code from employee_address;"
	data = []
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	rows = cursor.fetchall()
	for row in rows:
		data.append(row[0])
	return data

def createTimeInAddress(cursor):
	sql = "create or replace view time_in_address as select employee_address.eid,employee_address.house_num,employee_address.street_name,employee_address.city,employee_address.postal_code from employee_address, time_in_list where employee_address.eid = time_in_list.eid;"
	cursor.execute(sql)
	
def getTimeInPostalCodes( cursor ):
	sql = "select distinct postal_code from time_in_address;"
	cursor.execute(sql)
	data = []
	rows = cursor.fetchall()
	for row in rows:
		data.append( str(row[0] ) )
	return data

def getTimeInEidList( cursor, postalCode ):
	sql = "select eid from time_in_address where postal_code=\'"+postalCode+"\';"
	cursor.execute(sql)
	data = []
	rows = cursor.fetchall()
	for row in rows:
		data.append( str(row[0] ) )
	return data

def createTimeOutAddress(cursor):
	sql = "create or replace view time_out_address as select employee_address.eid,employee_address.house_num,employee_address.street_name,employee_address.city,employee_address.postal_code from employee_address, time_out_list where employee_address.eid = time_out_list.eid;"
	cursor.execute(sql)
	
def getTimeOutPostalCodes( cursor ):
	sql = "select distinct postal_code from time_out_address;"
	cursor.execute(sql)
	cursor.execute(sql)
	data = []
	rows = cursor.fetchall()
	for row in rows:
		data.append( str(row[0] ) )
	return data
	
def getEidListWithPostalCode(cursor, postalCode):
	sql = "select eid from employee_address where postal_code=\"" + postalCode + "\" ;"
	data = []
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	rows = cursor.fetchall()
	for row in rows:
		data.append(row[0])
	return data

def searchEmployeeAddress( cursor, eid ):
	sql = "select * from employee_address where eid=\"" + eid + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True
