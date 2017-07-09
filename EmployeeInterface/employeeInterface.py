import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB, cabsDB, driversDB

class EmployeeInterface (threading.Thread):

	def __init__( self, clientConnection, msgList ):
		threading.Thread.__init__(self)
		self.type = "Employee Interface"
		self.loginType = "emp"
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

    def getDetails( self, msgList ):
        empdata=employeeDB.getEmployee( self.cursor, self.eid)
        msg=self.eid+" "+empdata['first_name']+" "+empdata['last_name']
        print msg
        self.sendData(msg)

    def getCabDetails( self ):
        allocationdata=allocationsDB.getEmpAllocations(self.cursor, self.eid)
        driver=driversDB.getDrivers(self.cursor, allocationsDB['did'])
        msg=self.eid+" "+allocationdata['aid']+" "+allocationdata['cid']+" "+allocationdata['']



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
				if msgList[0] == 'idreq' : #request to add an employee
					print 'id request'
					self.getDetails( msgList )
					self.sendData( "done" )
				elif msgList[0] == 'cabdetails' :
					print 'cab details'
					self.getCabDetails()
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
					self.getDriverFeedback()
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
