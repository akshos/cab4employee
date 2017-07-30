import employeeDB

def insertLogin( cursor, data ):
	sql = "insert into login values( \"" 	+ 	\
			data['username']	+ "\" ,\"" 	+ 	\
			data['password']	+ "\" ,\"" 	+ 	\
			data['type'] 		+ "\" ,\""	+ 	\
			data['eid'] 		+ "\" ) "
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
		eid = getEidFromUsername( cursor, username )
		#add condition here to check if there is already a username in that field otherwise it gets refreshed each time
		#that doesnt seem like a problem atm though.
		employeeDB.setUsername(cursor, eid, username)
		#db.commit()
	return eid

def checkEid(cursor, eid):
	sql = "select eid from login where eid=\""+eid+"\" "
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	return True

def checkUsername(cursor, username):
	sql = "select username from login where username=\""+username+"\" "
	cursor.execute(sql)
	if cursor.rowcount == 0:
		return False
	return True

def getEidFromUsername( cursor, username ):
	sql = "select eid from login where username=\"" + username + "\" "
	cursor.execute( sql )
	if cursor.rowcount == 0:
		return None
	row = cursor.fetchone()
	return row[0]
