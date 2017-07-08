def insertLogin( cursor, data ):
	sql = "insert into login values( \"" 	+ 	\
			data['username']	+ "\" ,\"" 	+ 	\
			data['password']	+ "\" ,\"" 	+ 	\
			data['type'] 		+ "\" ,\""	+ 	\
			data['eid'] 		+ ") "
	cursor.execute( sql )

def authenticate( cursor, username, password, logintype ):
	sql = "select username from login where username=\"" + username + "\"AND password=\"" + password + "\"AND type=\"" + logintype + "\""
	data = { }
	cursor.execute( sql )
	eid = ''
	if cursor.rowcount == 0 :
		return None
	if logintype == 'admin' or logintype == 'emp':
		eid = getEidFromUsername( cursor )
	return eid
