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
		empdata = employeeDB.getEmployee( self.cursor, self.eid)
		msg = self.eid + " " + empdata['first_name'] + " " + empdata['last_name']
		#cabid drivername time of pickup location of pickup
		print msg
		self.sendData(msg)

	def getCabDetails( self ):
		allocationdata = allocationsDB.getEmpAllocations(self.cursor, self.eid)
		driver = driversDB.getDrivers(self.cursor, allocationsDB['did'])
		#msg = allocationdata['cid'] + " " + driver['first_name'] + " " + driver['last_name'] +" "+ allocationdata['atime']+" "+#employeeDB.getEmploye(allocationdata['eid'])[]
		print msg
		self.sendData(msg)

	def changePassword( self, msgList ):
		print 'change password'

	def changeAllocationTime(self, msgList):
		print 'change allocation'

	def sendFeedback(self,msgList):
		allocationdata=allocationsDB.getEmpAllocations(self.cursor, self.eid)
		cabdata=cabsDB.getCab(self.cursor , allocationdata['cid'])
		driverdata=driversDB(self.cursor, allocationdata['did'])
		cabrating=(cabdata['rating']+msgList[1])/2
		cabsDB.setRating(self.cursor, cabrating)
		driverrating=(driverdata['rating']+msgList[2])/2
		driversDB.setRating(self.cursor, driverrating)
		#include adding comments to database as msgList[3]

	def run( self ): #main entry point
		try:
			self.connectDB() #establish connection to database
			self.login() #attempt authentication
			if self.eid == None : #if authentication failed
				print 'login failed : employee interface'
				self.sendData("failed")	#send response that failed
				return #stop the thread due to login failure
			else :
				print 'sending done'
				self.getDetails();
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
				if msgList[0] == 'idreq' : #no use
					print 'id request'
					self.getDetails( msgList )
					self.sendData( "done" )
				elif msgList[0] == 'cabdetails' :
					print 'cab details'
					self.getCabDetails()
					self.sendData( "done" )
				elif msgList[0] == 'changepassword' :
					print 'change password'
					self.changePassword(msgList)
					self.sendData( "done" )
				elif msgList[0] == 'feedback':
					print 'send drivers'
					self.sendFeedback(msgList)
					self.sendData( "done" )
				elif msgList[0] == 'changetime':
					print'get allocations'
					self.changeAllocationTime(msgList)
					self.sendData("done")
				elif msgList[0] == 'stop':
					print 'stop'
					self.sendData("hello")
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
