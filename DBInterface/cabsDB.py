def insertCab( cursor, data ):
	sql = "insert into cabs values(\" " + \
			data['cid']				+ "\" ,\"" + 	\
			data['c_model']			+ "\" ,\"" + 	\
			data['maxpassengers']	+ "\" ) "
	cursor.execute( sql )

def geCab( cursor, cid ):
	sql = "select * from cabs where cid=\"" + cid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['cid'] 			= str( row[0] )
	data['c_model'] 		= str( row[1] )
	data['maxpassengers'] 	= str( row[2] )
	return data

def searchCab( cursor, cid ):
	sql = "select * from cabs where cid=\"" + cid + "\" "
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True
	
def getAllCid( cursor ):
	sql = "select cid from cabs"
	cursor.execute(sql)
	data=[]
	for i in range ( 0, cursor.rowcount ):
		data.append( cursor.fetchone()[0] )
	return data
