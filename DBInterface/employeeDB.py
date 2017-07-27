def insertEmployee( cursor, data ):
	sql = "insert into employee values( \"" +   \
			data['eid']			+ "\" , \"" + 	\
			data['first_name']	+ "\" , \"" + 	\
			data['last_name'] 	+ "\" , \""	+ 	\
			data['date_of_reg'] + "\" ,   " + 	\
			data['contact_num'] + "   , \"" + 	\
			data['account_id']  + "\" , \""	+ 	\
			data['time_in'] 	+ "\" , \""	+ 	\
			data['time_out']	+ "\" , \"" +	\
			data['username'] 	+ "\" ) "
	cursor.execute( sql )

def getEmployee( cursor, eid ):
	sql = "select * from employee where eid=\"" + eid + "\" "
	data = {}
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return None
	row = cursor.fetchone()
	data['eid'] 		= str( row[0] )
	data['first_name'] 	= str( row[1] )
	data['last_name'] 	= str( row[2] )
	data['date_of_reg'] = str( row[3] )
	data['contact_num'] = str( row[4] )
	data['account_id'] 	= str( row[5] )
	data['time_in']		= str( row[6] )
	data['time_out'] 	= str( row[7] )
	data['username']	= str( row[8] )
	data['email'] 		= str( row[9] )
	return data

def searchEmployeeName(cursor, pattern):
	sql = "select * from employee where first_name like \'%"+pattern+"%\' "
	dataList = []
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	rows = cursor.fetchall()
	for row in rows:
		data = {}
		data['eid'] 		= str( row[0] )
		data['first_name'] 	= str( row[1] )
		data['last_name'] 	= str( row[2] )
		data['date_of_reg'] = str( row[3] )
		data['contact_num'] = str( row[4] )
		data['account_id'] 	= str( row[5] )
		data['time_in']		= str( row[6] )
		data['time_out'] 	= str( row[7] )
		data['username']	= str( row[8] )
		data['email'] 		= str( row[9] )
		dataList.append(data)
	return dataList	

def getEmployeeFull(cursor, eid):
	sql = "select * from employee natural join employee_address"
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	data = {}
	data['eid'] 		= str( row[0] )
	data['first_name'] 	= str( row[1] )
	data['last_name'] 	= str( row[2] )
	data['date_of_reg'] = str( row[3] )
	data['contact_num'] = str( row[4] )
	data['account_id'] 	= str( row[5] )
	data['time_in']		= str( row[6] )
	data['time_out'] 	= str( row[7] )
	data['username']	= str( row[8] )
	data['email'] 		= str( row[9] )
	data['house_num'] 	= str( row[10] )
	data['street_name']	= str( row[11] )
	data['city']		= str( row[12] )
	data['postal_code'] = str( row[13] )
		
	return data

def getTimeIn( cursor, eid ):
	sql = "select time_in from employee where eid=\'"+eid+"\';"
	cursor.execute(sql)
	row = cursor.fetchone()
	return str(row[0])

def createEidWithTimeIn( cursor, startTime, endTime ):
	sql = "create or replace view time_in_list as select eid from employee \
			where time_in>\'"+startTime+"\' and time_in<\'"+endTime+"\' \
			and not exists (select eid from present_requests where present_requests.eid=employee.eid) \
			UNION select eid from present_requests where time_in<\'"+endTime+"\' and time_in>\'"+startTime+"\' ;" 	
	cursor.execute(sql);
#	print cursor.fetchall()

def createEidWithTimeOut( cursor, startTime, endTime ):
	sql = "create or replace view time_out_list as select eid from employee \
			where time_out>\'"+startTime+"\' and time_out<\'"+endTime+"\' \
			and not exists (select eid from present_requests where present_requests.eid=employee.eid) \
			UNION select eid from present_requests where time_out<\'"+endTime+"\' and time_out>\'"+startTime+"\' ;" 
	cursor.execute(sql);

def searchEmployee( cursor, eid ):
	sql = "select * from employee where eid=\"" + eid + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0 :
		return False
	return True

def getEidFromUsername( cursor, username ):
	sql = "select eid from employee where username=\"" + username + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	return row[0]

def getAllEid( cursor ) :
	sql = "select eid from employee"
	data = []
	cursor.execute( sql )
	if( cursor.rowcount == 0 ):
		return None
	rows = cursor.fetchall()
	for row in rows :
		data.append( str( row[0] ) )
	return data

def printAll(cursor):
	sql = "select * from employee natural join employee_address"
	cursor.execute(sql)
	rows = cursor.fetchall()
	print rows

def getEmail(cursor, eid):
	sql = "select email from employee where eid=\""+eid+"\" "
	cursor.execute(sql)
	row = cursor.fetchone()
	return str( row[0] )

def setUsername(cursor, eid, username):
	sql = "update employee set username=\""+username+"\" where eid=\""+eid+"\" "
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	return True

def getAllEmployees( cursor ) :
	sql = "select * from employee"
	data = []
	emp = {}
	cursor.execute( sql )
	rows = cursor.fetchall()
	for row in rows:
		emp['eid'] 			= str( row[0] )
		emp['first_name'] 	= str( row[1] )
		emp['last_name'] 	= str( row[2] )
		emp['date_of_reg'] 	= str( row[3] )
		emp['contact_num'] 	= str( row[4] )
		emp['account_id'] 	= str( row[5] )
		emp['time_in']		= str( row[6] )
		emp['time_out'] 	= str( row[7] )
		emp['username'] 	= str( row[8] )
		emp['email'] 		= str( row[9] )
		data.append( emp )
	return data
