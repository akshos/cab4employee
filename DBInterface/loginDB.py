import employeeDB

def insertLogin( cursor, data ):
	sql = "insert into login values( \"" 	+ 	\
			data['username']	+ "\" ,\"" 	+ 	\
			data['password']	+ "\" ,\"" 	+ 	\
			data['type'] 		+ "\" ,\""	+ 	\
			data['eid'] 		+ ") "
	cursor.execute( sql )

def changepassword(cursor, eid, newpass):
	try:
		sql = "update login set password ='"+newpass+"' where eid= '"+eid+"'"
		cursor.execute( sql )
		db.commit()
		return 1
	except:
		return 0

def authenticate( cursor, username, password, logintype ):
	sql = "select username from login where username=\"" + username + "\"AND password=\"" + password + "\"AND type=\"" + logintype + "\""
	data = { }
	cursor.execute( sql )
	eid = ''
	if cursor.rowcount == 0 :
		return None
	if logintype == 'admin' or logintype == 'emp':
		eid = employeeDB.getEidFromUsername( cursor, username )
	return eid
