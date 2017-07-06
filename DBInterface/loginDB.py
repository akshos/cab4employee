def insertLogin( cursor, data ):
	sql = "insert into login values( \"" + \
			data['username']			+ "\" ,\"" 	+ 	\
			data['password']			+ "\" ,\"" 	+ 	\
			data['type'] 		+ "\" ,\""	+ 	\
			data['eid'] 	+ ") "
	cursor.execute( sql )

def authenticate( cursor, username, password, logintype ):
	sql = "select eid from login where username=\"" + username + "\"AND password=\"" + password + "\"AND type=\"" + logintype + "\""
	data = { }
	cursor.execute( sql )
	if cursor.rowcount() == 0 :
		return None
	row = cursor.fetchone()
	return row[4]
