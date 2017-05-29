#----------------------------Employee-------------------------------
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

#----------------------------Employee Address-----------------------

def insertEmployeeAddress( cursor, data ):
	sql = "insert into employee_address values( " + \
			data['eid']			+ " , " + 	\
			data['house_num']	+ " , " + 	\
			data['street_name'] + " , "	+ 	\
			data['city'] 		+ " ) "
	cursor.execute( sql )

def getEmployeeAddress( cursor, eid ):
	sql = "select * from employee_address where eid=" + eid + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['eid'] 		= str( row[0] )
	data['house_num'] 	= str( row[1] )
	data['street_name'] = str( row[2] )
	data['city'] 		= str( row[3] )
	return data

def searchEmployeeAddress( cursor, eid ):
	sql = "select * from employee_address where eid=" + eid + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True

#----------------------------Accounts-------------------------------

def insertAccounts( cursor, data ):
	sql = "insert into accounts values( " + \
			data['aid']			+ " , " + 	\
			data['name']	 	+ " ) "
	cursor.execute( sql )

def getAccounts( cursor, aid ):
	sql = "select * from accounts where aid=" + aid + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['aid'] 		= str( row[0] )
	data['name'] 		= str( row[1] )
	return data

def searchAccounts( cursor, aid ):
	sql = "select * from accounts where aid=" + aid + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True

#----------------------------Cabs----------------------------------

def insertCabs( cursor, data ):
	sql = "insert into cabs values( " + \
			data['cid']			+ " , " + 	\
			data['c_model']		+ " , " + 	\
			data['did']		 	+ " ) "
	cursor.execute( sql )

def geCabs( cursor, cid ):
	sql = "select * from cabs where cid=" + cid + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['cid'] 		= str( row[0] )
	data['c_model'] 	= str( row[1] )
	data['did'] 		= str( row[2] )
	return data

def searchCabs( cursor, cid ):
	sql = "select * from cabs where cid=" + cid + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True

#----------------------------Drivers--------------------------------

def insertDrivers( cursor, data ):
	sql = "insert into drivers values( " + \
			data['did']				+ " , " + 	\
			data['name']			+ " , " + 	\
			data['contact_num'] 	+ " , "	+ 	\
			data['rating']		 	+ " ) "
	cursor.execute( sql )

def getDrivers( cursor, did ):
	sql = "select * from drivers where did=" + did + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['did'] 			= str( row[0] )
	data['name'] 			= str( row[1] )
	data['contact_num'] 	= str( row[2] )
	data['rating']			= str( row[3] )
	return data

def searchDrivers( cursor, did ):
	sql = "select * from drivers where did=" + did + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True

#----------------------------Allocations----------------------------

def insertAllocations( cursor, data ):
	sql = "insert into allocations values( " + \
			data['aid']			+ " , " + 	\
			data['eid']			+ " , " + 	\
			data['cid'] 		+ " , "	+ 	\
			data['did'] 		+ " , " + 	\
			data['atime'] 		+ " , " + 	\
			data['change_flag'] + " , "	+ 	\
			data['iftaken'] 	+ " ) "
	cursor.execute( sql )

def getAllocations( cursor, aid ):
	sql = "select * from allocations where aid=" + aid + " ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['aid'] 			= str( row[0] )
	data['eid'] 			= str( row[1] )
	data['cid'] 			= str( row[2] )
	data['did'] 			= str( row[3] )
	data['atime'] 			= str( row[4] )
	data['change_flag'] 	= str( row[5] )
	data['iftaken']			= str( row[6] )
	return data

def searchAllocations( cursor, aid ):
	sql = "select * from allocations where aid=" + aid + " ;"
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True
