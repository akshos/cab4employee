import threading
from DBInterface import DBConnection, loginDB
import time

class CompanyInterface (threading.Thread):

	def __init__( self, clientConnection, msgList ):
		threading.Thread.__init__(self)
		self.type = "Company Interface"
		self.loginType = "admin"
		self.clientConnection = clientConnection
		self.msgList = msgList
		
	def connectDB( self ): #connect to the sql database and create cursor object
		self.db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
		self.db.connect()
		self.cursor = self.db.getCursor()
	
	def sendData(self, data ):
		self.clientConnection.send( data )
		self.clientConnection.flush()
	
	def receiveData( self ):
		return self.clientConnection.recv(1024)
	
	def disconnect( self ):
		self.clientConnection.close()
	
	def login( self ): #authenticate using username, password and type and get eid from database
		self.username = self.msgList[2]
		password = self.msgList[3]
		self.eid = loginDB.authenticate( self.cursor, self.username, password, self.loginType )
		del self.msgList
	
	def run( self ): #main entry point
		try:
			self.connectDB() #establish connection to database
			self.login() #attempt authentication 
			if self.eid == None : #if authentication failed
				self.sendData("failed")	#send response that failed
				return #stop the thread due to login failure
			else :
				print 'sending done'
				self.sendData("done") #send a login accepted message
			while True:
				print 'waiting for request'
				self.msg = str( self.receiveData() ) #get a request from server
				print self.msg
				if self.msg == "disconnect" or self.msg == '0': #if disconnect request
					return #stop thread
		except:
			print 'Something went wrong : Company Interface'
		finally:
			self.disconnect() # disconnect when leaving thread
