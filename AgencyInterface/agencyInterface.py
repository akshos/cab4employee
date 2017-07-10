import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB, cabsDB, driversDB

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
		data['cid'] 			= msgList[1]
		data['c_model'] 		= msgList[2]
		data['maxpassengers'] 	= msgList[3]
		cabsDB.insertCab( self.cursor, self.db, data )

	def sendCabs( self ):
		cidList = cabsDB.getAllCid(self.cursor)
		msg = ""
		for cid in cidList:
			data = getCab( self.cursor, cid)
			msg += data[0] + " " + data[1] + " " + data[2] + " "
		print msg
		self.sendData(msg)

	def addDriver( self, msgList ):
		data = {}
		data['did'] 			= msgList[1]
		data['first_name'] 		= msgList[2]
		data['last_name'] 		= msgList[3]
		data['cid'] 			= msgList[4]
		data['contact_number'] 	= msgList[5]
		data['rating'] 			= "5"
		driversDB.insertDriver( self.cursor, data )
		self.db.commit()

	def sendDrivers( self ):
		didList = driversDB.getAllDid(self.cursor)
		msg = ""
		for did in didList:
			data = driversDB.getDrivers( self.cursor, did )
			msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['rating'] + " "
		print "msg"+msg
		self.sendData( msg )

	def sendCabs( self ):
		didList = cabsDB.getAllCid(self.cursor)
		msg = ""
		for did in didList:
			data = cabsDB.getCabs( self.cursor, cid )
			msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['rating'] + " "
		print "msg"+msg
		self.sendData( msg )

	def run( self ): #main entry point
		try:
			self.connectDB() #establish connection to database
			self.login() #attempt authentication
			if self.eid == None : #if authentication failed
				print 'login failed : agency interface'
				self.sendData("failed")	#send response that failed
				return #stop the thread due to login failure
			else :
				print 'sending done'
				self.sendData("done")
				#sendAllocations()
				print 'sent'  #send a login accepted message

			##
			#main request loop
			##
			while True:
				print 'waiting for request'
				self.msg = str( self.receiveData() ) #get a request from server
				print self.msg
				if self.msg == None:
					return
				msgList = self.msg.split()
				if len( msgList ) == 0:
					return
				if msgList[0] == 'addcab' : #request to add an employee
					print 'add cab'
					self.addCab( msgList )
					self.sendData( "done" )
				elif msgList[0] == 'adddriver' :
					print 'add driver'
					self.addDriver( msgList )
					self.sendData( "done" )
				elif msgList[0] == 'sendcabs' :
					print 'send cabs'
					self.sendCabs()
					self.sendData( "done" )
				elif msgList[0] == 'senddrivers':
					print 'send drivers'
					self.sendDrivers()
					self.sendData( "done" )
				elif msgList[0] == 'getallocations':
					print'get allocations'
					self.sendAllocations()
					self.sendData("done")
				elif msgList[0] == 'cabfeedback':
					print'cabfeedback'
					self.getCabFeedback()
					self.sendData("done")
				elif msgList[0] == 'driverfeedback':
					print'driver feedback'
					self.sendDrivers()
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
