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

	return data

def getTimeIn( cursor, eid ):
	sql = "select time_in from employee where eid=\'"+eid+"\';"
	cursor.execute(sql)
	row = cursor.fetchone()
	return str(row[0])

def createEidWithTimeIn( cursor, startTime, endTime ):
	sql = "create or replace view time_in_list as select eid from employee where time_in>\'"+startTime+"\' and time_in<\'"+endTime+"\' ;"
	cursor.execute(sql);

def createEidWithTimeOut( cursor, startTime, endTime ):
	sql = "create or replace view time_out_list as select eid from employee where time_out>\'"+startTime+"\' and time_out<\'"+endTime+"\' ;"
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
		data.append( emp )
	return data
