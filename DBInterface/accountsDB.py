def insertAccount( cursor, data ):
	sql = "insert into accounts values(\"" 	+ 				\
						data['aid']			+ "\" ,\"" + 	\
						data['name']	 	+ "\" ) "
	cursor.execute( sql )

def getAccount( cursor, aid ):
	sql = "select * from accounts where aid=\"" + aid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	data['aid'] 		= str( row[0] )
	data['name'] 		= str( row[1] )
	return data

def searchAccount( cursor, aid ):
	sql = "select * from accounts where aid=\"" + aid + "\" "
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True
