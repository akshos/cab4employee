def insertEmployeeAddress( cursor, data ):
	sql = "insert into employee_address values( \"" + \
			data['eid']			+ "\" ,\"" 	+ 	\
			data['house_num']	+ "\" ,\"" 	+ 	\
			data['street_name'] + "\" ,\""	+ 	\
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
	return data

def searchEmployeeAddress( cursor, eid ):
	sql = "select * from employee_address where eid=\"" + eid + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True
