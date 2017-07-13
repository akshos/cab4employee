def insertCab( cursor, db, data ):
	sql = "insert into cabs values(\"" + \
			data['cid']				+ "\" ,\"" + 	\
			data['c_model']			+ "\" ,\"" + 	\
			data['maxpassengers']	+ "\" ,\"" + 	\
			"0"						+ "\" ) "
	cursor.execute( sql )
	db.commit()

def getCab( cursor, cid ):
	sql = "select * from cabs where cid=\"" + cid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return None
	row = cursor.fetchone()
	data['cid'] 			= str( row[0] )
	data['c_model'] 		= str( row[1] )
	data['maxpassengers'] 	= str( row[2] )
	data['rating']			= str( row[3] )
	return data

def searchCab( cursor, cid ):
	sql = "select * from cabs where cid=\"" + cid + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True

def getCidList(cursor):
	sql = "select * from cabs;"
	cursor.execute(sql)
	rows = cursor.fetchall()
	cidList = []
	for row in rows:
		cidList.append( row[0] )
	return cidList

def getRating( cursor, cid):
	sql= "select rating from cabs where cid=\"" + cid + "\" ;"
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return None
	row =cursor.fetchone()
	return str( row[0] )


def getAllCid( cursor ):
	sql = "select cid from cabs"
	cursor.execute(sql)
	data=[]
	for i in range ( 0, cursor.rowcount ):
		data.append( cursor.fetchone()[0] )
	return data

def searchCabs(cursor, pattern):
	sql = "select distinct * from cabs where cid like \'%" + pattern + "%\' ;"
	cursor.execute(sql)
	dataList = []
	rows = cursor.fetchall()
	if cursor.rowcount == 0:
		return None
	for row in rows:
		data = {}
		data['cid'] 			= str( row[0] )
		data['c_model'] 		= str( row[1] )
		data['maxpassengers'] 	= str( row[2] )
		data['rating']			= str( row[3] )
		dataList.append(data)
	return dataList

def setRating(cursor, rate, cid):
	sql="update cabs set rating ='"+str(rate)+"'where cid='"+cid+"'"
	cursor.execute(sql)
