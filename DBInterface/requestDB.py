def addRequest( cursor, db, data ):
	if(searchRequest(cursor, db, data)==True):
		removeRequest(cursor, db, data['eid'], data['req_date'])
	sql = "insert into requests values(\"" + \
			data['eid']				      + "\" ,\"" + 	\
			data['req_date']			  + "\" ,\"" + 	\
			data['time_in']	              + "\" ,\"" + 	\
			data['time_out']		      + "\" ) "
	cursor.execute( sql )
	db.commit()

def getRequest(cursor, eid, presentDate):
	sql = "select * from requests where eid=\""+eid+"\" and req_date=\""+presentDate+"\" "
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	data = {}
	data['eid'] = str(row[0])
	data['req_date'] = str(row[1])
	data['time_in'] = str(row[2])
	data['time_out'] = str(row[3])
	return data

def searchRequest( cursor, db, data ):
	sql = "select * from requests where eid=\"" + data['eid'] + "\" and req_date=\""+ data['req_date'] +"\""
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True

def removeRequest( cursor, db, eid ,req_date):
	sql = "delete from requests where eid=\"" + eid + "\" and req_date=\""+ req_date +"\""
	cursor.execute( sql )
	if cursor.rowcount == 1:
		return True
	return False
	db.commit()

def createPresentRequests(cursor, presentDate):
	sql = "create or replace view present_requests as select * from requests where req_date=\""+presentDate+"\" "
	cursor.execute(sql)
	
