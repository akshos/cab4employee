import threading
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB

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
		msg = ""
		for aid in aidList:
			data = allocationsDB.getAllocations(self.cursor, aid)
			employee = employeeDB.getEmployee( self.cursor, data['eid'] )
			msg += data['aid'] + " " + employee['first_name'] + " " + employee['last_name'] +" "+ data['atime']+" "
		print msg
		self.sendData(msg)

	def searchEmployee( self, msgList ):
		data=employeeDB.getEmployee( self.cursor, msgList[1])
		msg = data['eid']+" "+data['first_name']+" "+data['last_name']+" "+data['contact_num']+" "+data['account_id']+" "+data['time_in']+" "+data['time_out']
		self.sendData(msg)

	def rejectAllocation( self, msgList ):
		for i in range( 1, len(msgList) ):
			allocationsDB.DeleteAllocation(self.cursor,msgList[i])
		self.db.commit()

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
					self.sendAllocations(msgList)
					self.sendData('done')
				if msgList[0] == 'addemployee' : #request to add an employee
					print 'add employee'
					self.addEmployee( msgList )
					self.sendData("done")
				if msgList[0] == 'search' :#request to search for an employee
					print 'search employee'
					self.searchEmployee(msgList)
				if msgList[0] == 'reject' :#request to reject an allocation
					print 'reject allocation'
					self.rejectAllocation(msgList)
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
