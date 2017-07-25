import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB, cabsDB, driversDB, employeeAddressDB

class AgencyInterface (threading.Thread):

	def __init__( self, clientConnection, msgList, db ):
		threading.Thread.__init__(self)
		self.type = "Agency Interface"
		self.loginType = "agency"
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

	def addCab( self, msgList ): #enter employee details into database
		data = {}
		data['cid'] 			= msgList[1]
		data['c_model'] 		= msgList[2]
		data['maxpassengers'] 	= msgList[3]
		data['rating'] 			= "5"
		checkData = cabsDB.getCab(self.cursor, data['cid'])
		if checkData == None:
			cabsDB.insertCab( self.cursor, self.db, data )
			self.db.commit()
			self.sendData("done")
		else:
			self.sendData("existing")
			

#	def sendCabs( self ):
#		cidList = cabsDB.getAllCid(self.cursor)
#		msg = ""
#		for cid in cidList:
#			data = cabsDB.getCab( self.cursor, cid)
#			msg += data[0] + " " + data[1] + " " + data[2] + " "
#		print msg
#		self.sendData(msg)
	
	def addDriver( self, msgList ):
		data = {}
		data['did'] 			= msgList[1]
		data['first_name'] 		= msgList[2]
		data['last_name'] 		= msgList[3]
		data['cid'] 			= msgList[4]
		data['contact_number'] 	= msgList[5]
		data['rating'] 			= "5"
		checkData = driversDB.getDriver(self.cursor, data['did'])
		if checkData == None:
			driversDB.insertDriver( self.cursor, data )
			self.db.commit()
			self.sendData("done")
		elif int( checkData['rating'] ) == -1 :
			self.sendData("flagged")
		elif int( checkData['rating'] ) < -1 :
			data['rating'] = str( -1* int(checkData['rating']) )
			driversDB.modifyDriver( self.cursor, data )
			self.db.commit()
			self.sendData("redone")
		else:
			self.sendData("existing")

	def sendAllocations( self ):
		dataList = allocationsDB.getAllocations( self.cursor )
		msg = ""
		for data in dataList:
			count = len( data['eid'].split(',') )
			msg += data['aid']+" "+data['cid']+" "+str(count)+" "+data['atime']+" "
		print msg
		self.sendData( msg )
			
	def sendDrivers( self ):
		didList = driversDB.getAllDid(self.cursor)
		msg = ""
		for did in didList:
			data = driversDB.getDriver( self.cursor, did )
			msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['cid'] + " " + data['contact_number'] + " " + data['rating'] + " "
		print "msg : "+msg
		self.sendData( msg )

	def sendDriver(self, msgList):
		did = msgList[1]
		msg = ""
		data = driversDB.getDriver( self.cursor, did )
		msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['cid'] + " " + data['contact_number'] + " " + data['rating']
		print "msg : " + msg
		self.sendData(msg)	

	def sendCabs( self ):
		cidList = cabsDB.getAllCid(self.cursor)
		msg = ""
		for cid in cidList:
			data = cabsDB.getCab( self.cursor, cid )
			msg += data['cid'] + " " + data['c_model'] + " " + data['maxpassengers'] + " " + data['rating'] + " "
		print "msg : "+msg
		self.sendData( msg )
		
	def sendCab(self, msgList):
		cid = msgList[1]
		msg = ""
		data = cabsDB.getCab( self.cursor, cid)
		msg += data['cid'] + " " + data['c_model'] + " " + data['maxpassengers'] + " "
		print msg
		self.sendData(msg)

	def sendCidList(self):
		cidList = cabsDB.getCidList(self.cursor)
		msg = ""
		for cid in cidList:
			msg += str( cid ) + " "
		print msg
		self.sendData(msg)
	
	def checkCidAllocated(self, msgList):
		cid = msgList[1]
		status = allocationsDB.checkCidAllocated(self.cursor, cid)
		if status == True:
			self.sendData("yes")
		else:
			self.sendData("no")
	
	def allocateCab(self, msgList):
		aid = msgList[1]
		cid = msgList[2]
		pcid = msgList[3]
		status = allocationsDB.modifyCid( self.cursor, aid, cid )
		if( status == True ):
			did = driversDB.getDidFromCid( self.cursor, cid )
			if did == None:
				self.sendData("fail")
				return
			status = allocationsDB.modifyDid( self.cursor, aid, did )
			status = allocationsDB.setChangeFlag( self.cursor, aid )
			if status == True :
				self.db.commit()
				self.sendData("success")
				return
			else :
				self.sendData("fail")
		else:
			self.sendData("fail")
	
	def sendAvailableCidList(self):
		cidList = allocationsDB.getAvailableCidList(self.cursor)
		msg = ""
		for cid in cidList:
			msg += str(cid) + " "
		print msg
		self.sendData(msg)
	
	def searchDrivers(self, msgList):
		msg = ""
		pattern = msgList[1]
		dataList = driversDB.searchDrivers(self.cursor, pattern)
		if dataList == None:
			self.sendData("NotFound")
			return
		for data in dataList:
			msg += data['did'] + " " + data['first_name'] + " " + data['last_name'] + " " + data['cid'] + " " + data['contact_number'] + " " + data['rating'] + " "
		print msg
		self.sendData(msg)
	
	def searchCabs(self, msgList):
		msg = ""
		pattern = msgList[1]
		dataList = cabsDB.searchCabs(self.cursor, pattern)
		if dataList == None:
			self.sendData(str(" "))
			return
		for data in dataList:
			msg += data['cid'] + " " + data['c_model'] + " " + data['maxpassengers'] + " " + data['rating'] + " "
		print msg
		self.sendData(msg)
	
	def sendRemainingCidList(self):
		cidList = driversDB.getRemainingCidList(self.cursor)
		msg = ""
		for cid in cidList:
			msg += str(cid) + " "
		print msg
		self.sendData(msg)
	
	def sendAllocationType(self, msgList):
		aid = msgList[1]
		data = allocationsDB.getAllocationType(self.cursor, aid)
		self.sendData(data)
	
	def sendAllocationAddresses(self, msgList):
		aid = msgList[1]
		data = allocationsDB.getAllocation( self.cursor, aid )
		eidList = data['eid']
		eids = eidList.split(',')
		msg = ""
		for eid in eids:
			data = employeeAddressDB.getEmployeeAddress(self.cursor, eid)
			msg += data['house_num']+" "+data['street_name']+" "+data['city']+" "+data['postal_code']+" "
		print msg
		self.sendData(msg)
	
	def sendAllocatedDriver(self, msgList):
		aid = msgList[1]
		data = allocationsDB.getAllocation( self.cursor, aid )
		did = data['did']
		driver = driversDB.getDriver(self.cursor, did)
		msg = driver['did']+" "+driver['first_name']+" "+driver['last_name']+" "+driver['contact_number']+" "+driver['rating']+" "
		self.sendData(msg)
	
	def sendAllocatedCab(self, msgList):
		aid = msgList[1]
		data = allocationsDB.getAllocation( self.cursor, aid )
		cid = data['cid']
		cab = cabsDB.getCab(self.cursor, cid)
		msg = cab['cid']+" "+cab['c_model']+" "+cab['maxpassengers']+" "+cab['rating']+" "
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
	
	def removeCab(self, msgList):
		cid = msgList[1]
		status = cabsDB.removeCab( self.cursor, cid )
		if status == True:
			status = driversDB.resetCab( self.cursor, cid )
			if status == True: 
				self.sendData("done")
				self.db.commit()
		else:
			self.sendData("fail")
	
	def modifyCab(self, msgList):
		data = {}
		data['cid'] = msgList[1]
		data['model'] = msgList[2]
		data['maxpassengers'] = msgList[3]
		status = cabsDB.modifyCab( self.cursor, data )
		if status == True:
			self.sendData("done")
			self.db.commit()
		else:
			self.sendData("fail")
	
	def modifyDriver(self, msgList):
		data = {}
		data['did'] = msgList[1]
		data['first_name'] = msgList[2]
		data['last_name'] = msgList[3]
		data['cid'] = msgList[4]
		data['contact_number'] = msgList[5]
		data['rating'] = 'None'
		status = driversDB.modifyDriver(self.cursor, data)
		if status == True:
			self.sendData("done")
			self.db.commit()
		else:
			self.sendData("fail")
	
	def removeDriver(self, msgList):
		did = msgList[1]
		driver = driversDB.getDriver(self.cursor, did)
		rating = int(driver['rating'])
		rating = -1*rating
		status = driversDB.removeDriver(self.cursor, did, str(rating) )
		if status == True:
			self.sendData("done")
			self.db.commit()
		else:
			self.sendData("fail")
		
	def getDriverFromCid(self, msgList):
		cid = msgList[1]
		data = driversDB.getDriverFromCid(self.cursor, cid)
		if data != None:
			msg = data['did']+" "+data['first_name']+" "+data['last_name']+" "+data['cid']+" "+data['contact_number']
			self.sendData(msg)
		else:
			self.sendData("failed")
		
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
				elif msgList[0] == 'adddriver' :
					print 'add driver'
					self.addDriver( msgList )
				elif msgList[0] == 'sendcabs' :
					print 'send cabs'
					self.sendCabs()
				elif msgList[0] == 'sendcab':
					print 'send cab'
					self.sendCab(msgList)
				elif msgList[0] == 'senddriver':
					print 'send driver'
					self.sendDriver(msgList)
				elif msgList[0] == 'senddrivers':
					print 'send drivers'
					self.sendDrivers()
				elif msgList[0] == 'sendallocations':
					print 'get allocations'
					self.sendAllocations()
				elif msgList[0] == 'sendcidlist':
					print 'send cidlist'
					self.sendCidList()
				elif msgList[0] == 'sendavailablecidlist':
					print 'send available cidlist'
					self.sendAvailableCidList()
				elif msgList[0] == 'allocatecab':
					print 'allocate cab'
					self.allocateCab(msgList)
				elif msgList[0] == 'deallocatecab':
					print 'deallocate cab'
					self.deallocateCab( msgList )
				elif msgList[0] == 'searchdrivers':
					print 'search drivers'
					self.searchDrivers(msgList)
				elif msgList[0] == 'searchcabs':
					print 'search cabs'
					self.searchCabs(msgList)
				elif msgList[0] == 'semdremainingcidlist' :
					print 'send remaining cabs'
					self.sendRemainingCidList()
				elif msgList[0] == 'sendallocationaddresses':
					print 'send allocation addresses'
					self.sendAllocationAddresses(msgList)
				elif msgList[0] == 'sendallocateddriver':
					print 'send allocated driver'
					self.sendAllocatedDriver(msgList)
				elif msgList[0] == 'sendallocatedcab' :
					print 'send allocated cab'
					self.sendAllocatedCab(msgList)
				elif msgList[0] == 'sendallocationtype':
					print 'send allocation type'
					self.sendAllocationType(msgList)
				elif msgList[0] == 'removecab':
					print 'remove cab'
					self.removeCab(msgList)
				elif msgList[0] == 'modifycab':
					print 'modify cab'
					self.modifyCab(msgList)
				elif msgList[0] == 'removedriver':
					print 'remove driver'
					self.removeDriver(msgList)
				elif msgList[0] == 'modifydriver':
					print 'modify driver'
					self.modifyDriver(msgList)
				elif msgList[0] == 'checkcidallocated':
					print 'check cid allocated'
					self.checkCidAllocated(msgList)
				elif msgList[0] == 'getdriverfromcid':
					print 'get driver from cid'
					self.getDriverFromCid(msgList)
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
