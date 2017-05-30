def insertDrivers( cursor, data ):
	sql = "insert into drivers values(\"" + \
			data['did']				+ "\" ,\" " + 	\
			data['name']			+ "\" , " + 	\
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
