import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB, employeeAddressDB, cabsDB, driversDB

class CompanyInterface (threading.Thread):

	def __init__( self, clientConnection, msgList, db ):
		threading.Thread.__init__(self)
		self.type = "Company Interface"
		self.loginType = "admin"
		self.clientConnection = clientConnection
		self.msgList = msgList
		self.db = db

	def connectDB( self ): #connect to the sql database and create cursor object
		#self.db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
		#self.db.connect()
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

	def addEmployee( self, msgList ): #enter employee details into database
		data = {}
		data['eid'] 		= msgList[1];
		data['first_name'] 	= msgList[2];
		data['last_name'] 	= msgList[3];
		data['date_of_reg'] = msgList[4];
		data['contact_num'] = msgList[5];
		data['account_id'] 	= msgList[6];
		data['time_in']		= msgList[7];
		data['time_out'] 	= msgList[8];
		employeeDB.insertEmployee( self.cursor, data )

	def sendAllocations( self ):
		aidList = allocationsDB.getAllAid(self.cursor)
		if (aidList==None):
			self.sendData('fail')
		msg = ""
		for aid in aidList:
			data = allocationsDB.getAllocation(self.cursor, aid)
			#employee = employeeDB.getEmployee( self.cursor, data['eid'] )
			msg += data['aid'] + " " + data['eid'] + " " +data['cid'] + " " + data['atime']+" "
		print msg
		self.sendData(msg)

	def searchEmployee( self, msgList ):
		data = employeeDB.getEmployee( self.cursor, msgList[1])
		print data
		if data != None:
			msg = data['eid']+" "+data['first_name']+" "+data['last_name']+" "+data['contact_num']+" "+data['account_id']+" "+data['time_in']+" "+data['time_out']
			self.sendData(msg)
		else:
			self.sendData("notfound")

	def rejectAllocation( self, msgList ):
		for i in range( 1, len(msgList) ):
			allocationsDB.deleteAllocation(self.cursor,msgList[i])
		self.db.commit()

	def sendExtraDetails(self,aid):
		allocation=allocationsDB.getAllocation(self.cursor, aid)
		eidList=allocation['eid'].split(',')
		employeedetails=""
		print eidList
		for eid in eidList:
			data=employeeDB.getEmployee(self.cursor,eid)
			address=employeeAddressDB.getEmployeeAddress(self.cursor,eid)
			employeedetails += data['eid']+" "+data['first_name']+" "+data['last_name']+" "+data['date_of_reg']+" "+data['contact_num']+" "+data['account_id']+" "+data['time_in']+" "+data['time_out']+" "+address['house_num']+" "+ address['street_name']+" "+address['city']+" "+address['postal_code']+" "
		cabdetails = ""
		driverdetails = ""
		if allocation['cid'] != "None":
			cab=cabsDB.getCab(self.cursor,allocation['cid'])
			cabdetails=cab['cid']+" "+cab['c_model']+" "+cab['maxpassengers']
			driver=driversDB.getDriver(self.cursor,allocation['did'])
			driverdetails=driver['did']+" "+driver['first_name']+" "+driver['last_name']+" "+driver['contact_number']+" "+driver['rating']
		msg=cabdetails+" "+driverdetails+" "+employeedetails
		self.sendData(msg)

	def sendEmployeeList(self):
		eidList = employeeDB.getAllEid(self.cursor)
		print 'eid list : ' + str(eidList)
		msg=""
		for eid in eidList:
			data = employeeDB.getEmployee(self.cursor,eid)
			msg += data['eid']+" "+data['first_name']+" "+data['last_name']+" "+data['date_of_reg']+" "+data['contact_num']+" "+data['account_id']+" "+data['time_in']+" "+data['time_out']+" "
		print msg
		self.sendData(msg)

	def sendDrivers( self ):
		didList = driversDB.getAllDid(self.cursor)
		msg = ""
		for did in didList:
			data = driversDB.getDriver( self.cursor, did )
			msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['cid'] + " " + data['contact_number'] + " " + data['rating'] + " "
		print "msg : "+msg
		self.sendData( msg )

	def sendCabs( self ):
		cidList = cabsDB.getAllCid(self.cursor)
		msg = ""
		for cid in cidList:
			data = cabsDB.getCab( self.cursor, cid )
			msg += data['cid'] + " " + data['c_model'] + " " + data['maxpassengers'] + " " + data['rating'] + " "
		print "msg : "+msg
		self.sendData( msg )
	
	def searchEmployeeName(self, msgList):
		pattern = msgList[1]
		employees = employeeDB.searchEmployeeName(self.cursor, pattern)
		if employees == None:
			self.sendData("None")
		msg = ""
		for emp in employees:
			msg += emp['eid']+" "+emp['first_name']+" "+emp['last_name']+" "+emp['date_of_reg']+" "+emp['contact_num']+" "+emp['account_id']+" "+emp['time_in']+" "+emp['time_out']+" "+emp['username']+" " 
		self.sendData(msg)

	def deallocateCab(self, msgList):
		aid = msgList[1]
		status = allocationsDB.resetCidDid( self.cursor, aid )
		if status == True:
			status = allocationsDB.setChangeFlag( self.cursor, aid )
			if status == True:
				self.sendData("success")
				self.db.commit()
			else:
				self.sendData("fail")
	
	def getEmployeeFull(self, msgList):
		eid = msgList[1]
		data = employeeDB.getEmployeeFull(self.cursor, eid)
		if data == None:
			self.sendData("fail")
			return
		msg = data['eid']+" "+data['first_name']+" "+data['last_name']+" "+data['date_of_reg']+" "+data['contact_num']+" "+data['account_id']+" "+data['time_in']+" "+data['time_out']+" "+data['house_num']+" "+data['street_name']+" "+data['city']+" "+data['postal_code']+" "
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
				self.sendAllocations()
				print 'sent'  #send a login accepted message

			##
			#main request loop
			##
			while True:
				print 'waiting for request'
				self.msg = str( self.receiveData() ) #get a request from server
				if self.msg == None:
					return
				print self.msg
				msgList = self.msg.split()
				if len(msgList) == 0:
					return
				if msgList[0] == 'allocations' :
					print'send allocations'
					self.sendAllocations()
					self.sendData('done')
				elif msgList[0] == 'addemployee' : #request to add an employee
					print 'add employee'
					self.addEmployee( msgList )
					self.sendData("done")
				elif msgList[0] == 'search' :#request to search for an employee
					print 'search employee'
					self.searchEmployee(msgList)
				elif msgList[0] == 'reject' :#request to reject an allocation
					print 'reject allocation'
					self.rejectAllocation(msgList)
					self.sendData("done")
				elif msgList[0] == 'employeelist' :#request employee listens
					print 'send employee list'
					self.sendEmployeeList()
					self.sendData("done")
				elif msgList[0] == 'extra':#request for extra allocaton details
					print 'send extra details'
					self.sendExtraDetails(msgList[1])
					self.sendData("done")
				elif msgList[0] == 'senddrivers':
					print 'send drivers'
					self.sendDrivers()
				elif msgList[0] == 'sendcabs':
					print 'send cabs'
					self.sendCabs()
				elif msgList[0] == 'searchemployeename':
					print 'search employee name'
					self.searchEmployeeName(msgList)
				elif msgList[0] == 'deallocatecab':
					print 'deallocate cab'
					self.deallocateCab( msgList )
				elif msgList[0] == 'getemployeefull':
					print 'get employee full'
					self.getEmployeeFull(msgList)
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
