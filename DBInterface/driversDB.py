def insertDriver( cursor, data ):
	sql = "insert into drivers values(\"" + \
			data['did']				+ "\" ,\"" 	+ 	\
			data['first_name']		+ "\" ,\"" 	+ 	\
			data['last_name']		+ "\" ,\"" 	+ 	\
			data['cid']				+ "\" , " 	+ 	\
			data['contact_number'] 	+ " , "		+ 	\
			data['rating']		 	+ " ) "
	cursor.execute( sql )

def getDriver( cursor, did ):
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

def searchDrivers(cursor, pattern):
	sql = "select * from drivers where first_name like \'%" + pattern + "%\' ; "
	dataList = []
	cursor.execute(sql)
	rows = cursor.fetchall()
	if cursor.rowcount == 0:
		return None
	for row in rows:
		data = {}
		data['did'] 			= str( row[0] )
		data['first_name'] 		= str( row[1] )
		data['last_name'] 		= str( row[2] )
		data['cid'] 			= str( row[3] )
		data['contact_number'] 	= str( row[4] )
		data['rating']			= str( row[5] )
		dataList.append(data)
	return dataList

def getRating( cursor, did):
	sql= "select rating from drivers where did=\"" + did + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row =cursor.fetchone()
	return str( row[0] )

def searchDriver( cursor, did ):
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

def getRemainingCidList( cursor ):
	sql = "select cabs.cid from cabs left join drivers on cabs.cid = drivers.cid where drivers.cid is null;"
	cursor.execute(sql)
 	rows = cursor.fetchall()
 	data = []
 	for row in rows :
 		data.append(row[0])
 	return data

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

def setRating(cursor, rate, did):
	sql="update drivers set rating ='"+str(rate)+"'where did='"+did+"'"
	cursor.execute(sql)
