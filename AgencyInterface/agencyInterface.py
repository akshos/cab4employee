import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB

class AgencyInterface (threading.Thread):

	def __init__( self, clientConnection, msgList ):
		threading.Thread.__init__(self)
		self.type = "Agency Interface"
		self.loginType = "agency"
		self.clientConnection = clientConnection
		self.msgList = msgList
		
	def connectDB( self ): #connect to the sql database and create cursor object
		self.db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
		self.db.connect()
		self.cursor = self.db.getCursor()
	
	def sendData(self, data ):
		self.clientConnection.send( data + '\n' ) 
	
	def receiveData( self ):
		return self.clientConnection.recv(1024)
	
	def disconnect( self ):
		self.clientConnection.close()
		print 'client disconnected'
	
	def login( self ): #authenticate using username, password and type and get eid from database
		if self.msgList[1] != 'login':
			return None
		self.username = self.msgList[2]
		password = self.msgList[3]
		self.eid = loginDB.authenticate( self.cursor, self.username, password, self.loginType )
		del self.msgList
	
	def addCab( self, msgList ): #enter employee details into database
		data = {}
		data['cid'] 		= msgList[1];
		data['c_model'] 	= msgList[2];
		data['did'] 		= msgList[3];
		cabsDB.insertCab( self.cursor, data )
					
	def sendCabs( self ):
		cidList = cabsDB.getAllCid(self.cursor)
		msg = ""
		for cid in aidList:
			data = getCab(cursor, aid)
			msg += data[0] + " " + data[1] + " " + data[2]
		print msg
		self.sendData(msg)
	
	def run( self ): #main entry point
		try:
			self.connectDB() #establish connection to database
			self.login() #attempt authentication 
			if self.eid == None : #if authentication failed
				self.sendData("failed")	#send response that failed
				return #stop the thread due to login failure
			else :
				print 'sending done'
				self.sendData("done")
				sendAllocations()
				print 'sent'  #send a login accepted message
			
			##
			#main request loop
			##
			while True:
				print 'waiting for request'
				self.msg = str( self.receiveData() ) #get a request from server
				print self.msg
				msgList = self.msg.split()
				if msgList[0] == 'addcab' : #request to add an employee
					print 'add cab'
					addCab( msgList )
					self.sendData("done")
				else :
					return
			##
			#
			##
#		except IntegrityError as e:
#			self.sendData("EC1")
#		except :
#			print 'something wrong'
		finally:
			self.disconnect() # disconnect when leaving thread
