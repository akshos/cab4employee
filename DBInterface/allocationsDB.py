def insertAllocations( cursor, data ):
	sql = "insert into allocations values( \"" + \
			data['aid']			+ "\" ,\"" 	+ 	\
			data['eid']			+ "\" ,\"" 	+ 	\
			data['cid'] 		+ "\" ,\""	+ 	\
			data['did'] 		+ "\" ,\"" 	+ 	\
			data['atime'] 		+ "\" , " 	+ 	\
			data['change_flag'] + " , "		+ 	\
			data['iftaken'] 	+ ") "
	cursor.execute( sql )

def getAllocations( cursor, aid ):
	sql = "select * from allocations where aid=\"" + aid + "\" "
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

def getAllAid(cursor):
	sql = "select aid from allocations"
	cursor.execute(sql)
	data=[]
	for i in range (0,cursor.rowcount):
		data.append(cursor.fetchone()[0])
	return data

def searchAllocations( cursor, aid ):
	sql = "select * from allocations where aid=\"" + aid + "\" "
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return False
	return True
