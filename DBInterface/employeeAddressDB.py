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
