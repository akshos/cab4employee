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

	def getDetails( self):
		empdata = employeeDB.getEmployee( self.cursor, self.eid)
		msg = self.eid + " " + empdata['first_name'] + " " + empdata['last_name'] +" "
		allallocations = allocationsDB.getAllocations(self.cursor)
		aid=None
		for allocation in allallocations:
			eids=allocation['eid'].split(',')
			for eid in eids:
				if eid==self.eid:
					aid=allocation['aid']
		if aid != None:
			allocationdata = allocationsDB.getAllocation(self.cursor, aid)
			msg+="1 "
			if allocationdata['direction']=="pickup":
				msg+="pickup "+empdata['time_in']
			else :
				msg+="drop "+empdata['time_out']
		else:
			msg+="0 0 0"
		#cabid drivername time of pickup location of pickup
		print msg
		self.sendData(msg)

	def getCabDetails( self ):
		allallocations = allocationsDB.getAllocations(self.cursor)
		aid=None
		for allocation in allallocations:
			eids=allocation['eid'].split(',')
			for eid in eids:
				if eid==self.eid:
					aid=allocation['aid']
		if aid == None:
			print "empty"
			self.sendData("empty")
		else:
			allocationdata = allocationsDB.getAllocation(self.cursor, aid)
			did=allocationdata['did']
			cid = allocationdata['cid']
			print allocationdata
			if did != "None" and cid != "None":
				driver = driversDB.getDriver(self.cursor, did)
				msg = cid + " " + driver['first_name'] +" "+ driver['last_name'] +" "+driver['contact_number']+" "+allocationdata['atime']
				#employeeDB.getEmploye(allocationdata['eid'])[]
				print msg
				self.sendData(msg)
			else :
				self.sendData("empty")
			self.sendData("done")

	def changePassword( self, msgList ):
		print 'changing password..................'
		uname=employeeDB.getEmployee(self.cursor,self.eid)['username']
		return loginDB.changePassword(self.cursor, uname, msgList[1])

	def cancelAllocation(self, msgList):
		print 'changing allocation................'
		allallocations = allocationsDB.getAllocations(self.cursor)
		aid=None
		for allocation in allallocations:
			eids=allocation['eid'].split(',')
			for eid in eids:
				if eid==self.eid:
					aid=allocation['aid']
		return allocationsDB.cancelAllocation(self.cursor, aid, self.eid)



	def sendFeedback(self,msgList):
		allallocations = allocationsDB.getAllocations(self.cursor)
		aid=None
		for allocation in allallocations:
			eids=allocation['eid'].split(',')
			for eid in eids:
				if eid==self.eid:
					aid=allocation['aid']
		allocationdata=allocationsDB.getAllocation(self.cursor, aid)
		cabdata=cabsDB.getCab(self.cursor , allocationdata['cid'])
		driverdata=driversDB.getDriver(self.cursor, allocationdata['did'])
		cabrating=(float(cabdata['rating'])+float(msgList[3]))/2
		cabsDB.setRating(self.cursor, cabrating, allocationdata['cid'])
		driverrating=(float(driverdata['rating'])+(float(msgList[2])+float(msgList[1]))/2)/2
		driversDB.setRating(self.cursor, driverrating, allocationdata['did'])
		self.db.commit();
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

				elif msgList[0] == 'changepassword' :
					print 'change password'
					a=self.changePassword(msgList)
					self.db.commit()
					if a==1:
						self.sendData( "done" )
					else:
						self.sendData( "failed" )
				elif msgList[0] == 'feedback':
					print 'send drivers'
					self.sendFeedback(msgList)
					self.sendData( "done" )
				elif msgList[0] == 'cancel':
					print'get allocations'
					self.cancelAllocation(msgList)
					self.db.commit()
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
