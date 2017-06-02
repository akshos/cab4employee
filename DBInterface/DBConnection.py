import MySQLdb

class DBConnection:

	def __init__( self, host, username, password, databaseName ):
		self.host = host
		self.username = username
		self.password = password
		self.databaseName = databaseName
	
	def connect( self ):
		self.connection = MySQLdb.connect( self.host, self.username, self.password, self.databaseName )
		self.cursor = self.connection.cursor()
		
	def getCursor( self ):
		return self.cursor
	
	def execute( self, sqlString ):
		return self.cursor.execute( sqlString )
		
	def commit( self ):
		self.connection.commit()
	
