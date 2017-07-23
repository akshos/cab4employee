import cabsDB

def insertAllocations( cursor, data ):
	sql = "insert into allocations values( \"" + \
			data['aid']			+ "\" ,\"" 	+ 	\
			data['eid']			+ "\" ,\"" 	+ 	\
			data['cid'] 		+ "\" ,\""	+ 	\
			data['did'] 		+ "\" ,\"" 	+ 	\
			data['atime'] 		+ "\" , " 	+ 	\
			data['change_flag'] + " , "		+ 	\
			data['iftaken'] 	+ " , \""	+	\
			data['direction']  	+ "\" ); "
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
	data['direction']		= str( row[7] )
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
		data['direction']		= str( row[7] )
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

def modifyDid(cursor, aid, did):
	sql = "update allocations set did=\"" + did + "\" where aid=\"" + aid + "\" ;" 
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	return True

def checkCidAllocated(cursor, cid):
	sql = "select * from allocations where cid=\""+cid+"\" "
	cursor.execute(sql)
	if cursor.rowcount == 1:
		return True
	return False

def getAvailableCidList(cursor):
	sql = "select cabs.cid from cabs left join allocations on cabs.cid = allocations.cid, drivers where allocations.cid is null and cabs.cid = drivers.cid and drivers.rating>1 and cabs.rating>1"
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

def setChangeFlag(cursor, aid):
	sql = "update allocations set change_flag=1 where aid=\""+aid+"\" "
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return False
	return True

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
	data['direction']		= str( row[7] )
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

def getAllocationType(cursor, aid):
	sql = "select direction from allocations where aid=\""+aid+"\";"
	cursor.execute(sql)
	row = cursor.fetchone()
	data = str( row[0] )
	return data

def resetCidDid(cursor, aid):
	sql = "update allocations set cid=\"None\" where aid=\"" + aid + "\" ;"
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	sql = "update allocations set did=\"None\" where aid=\"" + aid + "\" ;"
	cursor.execute(sql)
	if cursor.rowcount == 0:
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
	#print "eid="+eid+"eidlist:"
	#print eidList
	for id in eidList:
		if id!=eid:
			neweid+=id+","
	#print neweid
	neweid = neweid[:-1]
	sql = "update allocations set eid ='"+neweid+"' where aid= '"+aid+"'"
	cursor.execute( sql )
