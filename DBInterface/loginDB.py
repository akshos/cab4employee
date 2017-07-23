import employeeDB

def insertLogin( cursor, data ):
	sql = "insert into login values( \"" 	+ 	\
			data['username']	+ "\" ,\"" 	+ 	\
			data['password']	+ "\" ,\"" 	+ 	\
			data['type'] 		+ "\" ,\""	+ 	\
			data['eid'] 		+ ") "
	cursor.execute( sql )

def changePassword(cursor, un, newpass):
	#try:
		sql = "update login set password ='"+newpass+"' where username= '"+un+"'"
		cursor.execute( sql )

		return 1
	#except:
	#	return 0

def authenticate( cursor, username, password, logintype ):
	sql = "select username from login where username=\"" + username + "\"AND password=\"" + password + "\"AND type=\"" + logintype + "\""
	data = { }
	cursor.execute( sql )
	eid = ''
	if cursor.rowcount == 0 :
		return None
	if logintype == 'emp':
		eid = employeeDB.getEidFromUsername( cursor, username )
	return eid
