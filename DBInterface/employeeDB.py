def insertEmployee( cursor, data ):
	sql = "insert into employee values( " + \
			data['eid']			+ " , " + 	\
			data['first_name']	+ " , " + 	\
			data['last_name'] 	+ " , "	+ 	\
			data['date_of_reg'] + " , " + 	\
			data['contact_num'] + " , " + 	\
			data['account_id']  + " , "	+ 	\
			data['time_in'] 	+ " , "	+ 	\
			data['time_out'] 	+ " ) "
	cursor.execute( sql )

def getEmployee( cursor, eid ):
	sql = "select * from employee where eid=" + eid + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['eid'] 		= str( row[0] )
	data['first_name'] 	= str( row[1] )
	data['last_name'] 	= str( row[2] )
	data['date_of_reg'] = str( row[3] )
	data['contact_num'] = str( row[4] )
	data['account_id'] 	= str( row[5] )
	data['time_in']		= str( row[6] )
	data['time_out'] 	= str( row[7] )
	return data

def searchEmployee( cursor, eid ):
	sql = "select * from employee where eid=" + eid + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True



