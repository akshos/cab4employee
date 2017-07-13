import cabsDB

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

def getAllocation( cursor, aid ):
	sql = "select * from allocations where aid=\"" + aid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount == 0 :
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

def getAllocations( cursor ):
	sql = "select * from allocations;"
	dataList = []
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	rows = cursor.fetchall()
	for row in rows:
		data = {}
		data['aid'] 			= str( row[0] )
		data['eid'] 			= str( row[1] )
		data['cid'] 			= str( row[2] )
		data['did'] 			= str( row[3] )
		data['atime'] 			= str( row[4] )
		data['change_flag'] 	= str( row[5] )
		data['iftaken']			= str( row[6] )
		dataList.append(data)
	return dataList

def deleteAllocation(cursor, aid):
	sql = "delete from allocations where aid=\"" + aid + "\" ;"
	cursor.execute( sql )
	return None

def modifyCid(cursor, aid, cid):
	sql = "update allocations set cid=\"" + cid + "\" where aid=\"" + aid + "\" ;"
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	return True

def getAvailableCidList(cursor):
	sql = "select cabs.cid from cabs left join allocations on cabs.cid = allocations.cid where allocations.cid is null;"
 	cursor.execute(sql)
 	rows = cursor.fetchall()
 	data = []
 	for row in rows :
 		data.append(row[0])
 	return data

def getEid(cursor, aid):
	sql = "select eid from allocations where aid=\"" + aid + "\" ; "
	cursor.execute( sql )
	data = cursor.fetchone()[0]
	return data

def getTimeCid(cursor, aid):
	sql = "select atime,cid from allocations where aid=\"" + aid + "\" ;"
	cursor.execute( sql )
	row = cursor.fetchone()
	time = str(row[0])
	cid = row[1]
	return time, cid

def getEmpAllocations( cursor, eid ):
	sql = "select * from allocations where eid=\"" + eid + "\" "
	data = { }
	cursor.execute( sql )
	if cursor.rowcount == 0 :
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

def cancelAllocation( cursor, aid, eid ):
	sql = "select eid from allocations where aid=\"" + aid + "\" "
	cursor.execute( sql )
	neweid=""
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	eids = str( row[0] )
	eidList=eids.split(',')
	for each id in eidList:
		if id!=eid:
			neweid+=id+" "
	print neweid
	sql = "update allocations set eid ='"+neweid+"' where aid= '"+aid+"'"
	cursor.execute( sql )
	db.commit()
