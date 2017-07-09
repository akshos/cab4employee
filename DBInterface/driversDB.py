def insertDriver( cursor, data ):
	sql = "insert into drivers values(\"" + \
			data['did']				+ "\" ,\"" 	+ 	\
			data['first_name']		+ "\" ,\"" 	+ 	\
			data['last_name']		+ "\" ,\"" 	+ 	\
			data['cid']				+ "\" , " 	+ 	\
			data['contact_number'] 	+ " , "		+ 	\
			data['rating']		 	+ " ) "
	cursor.execute( sql )

def getDrivers( cursor, did ):
	sql = "select * from drivers where did=\"" + did + "\" ;"
	data = { }
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return None
	row = cursor.fetchone()
	data['did'] 			= str( row[0] )
	data['first_name'] 		= str( row[1] )
	data['last_name'] 		= str( row[2] )
	data['cid'] 			= str( row[3] )
	data['contact_number'] 	= str( row[4] )
	data['rating']			= str( row[5] )
	return data

def getRating( cursor, did):
	sql= "select rating from drivers where did=\"" + did + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row =cursor.fetchone()
	return str( row[0] )

def searchDrivers( cursor, did ):
	sql = "select * from drivers where did=\"" + did + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True

def getCid( cursor, did ):
	sql = "select cid from drivers where did=\"" + did + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	return str( row[0] )

def getDid( cursor, cid ):
	sql = "select did from drivers where cid=\"" + cid + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	return str( row[0] )

def getAllDid( cursor ):
	sql = "select did from drivers"
	cursor.execute(sql)
	data=[]
	for i in range ( 0, cursor.rowcount ):
		data.append( cursor.fetchone()[0] )
	return data
