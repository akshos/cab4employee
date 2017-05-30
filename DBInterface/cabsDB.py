def insertCabs( cursor, data ):
	sql = "insert into cabs values(\" " + \
			data['cid']			+ "\" ,\" " + 	\
			data['c_model']		+ "\" ,\" " + 	\
			data['did']		 	+ "\" ) "
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
