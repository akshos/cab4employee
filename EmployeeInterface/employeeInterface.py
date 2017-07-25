import threading
import datetime
from DBInterface import DBConnection, loginDB, employeeDB, allocationsDB, cabsDB, driversDB,requestDB

class EmployeeInterface (threading.Thread):

	def __init__( self, clientConnection, msgList, db ):
		threading.Thread.__init__(self)
		self.type = "Employee Interface"
		self.loginType = "emp"
		self.clientConnection = clientConnection
		self.msgList = msgList
		self.db = db

	def connectDB( self ): #connect to the sql database and create cursor object
		self.cursor = self.db.getCursor()

	def sendData(self, data ):
		print "sending : " + data;
		self.clientConnection.send( data + '\n' )

	def receiveData( self ):
		data=self.clientConnection.recv(1024)
		print "recieved:"+data;
		return data

	def disconnect( self ):
		self.clientConnection.close()
		print 'client disconnected'

	def login( self ): #authenticate using username, password and type and get eid from database
		if self.msgList[1] != 'login':
			return None
		self.username = self.msgList[2]
		password = self.msgList[3]
		self.eid = loginDB.authenticate( self.cursor, self.username, password, self.loginType )
		#self.eid="e01"
		del self.msgList

	def getDetails( self):
		empdata = employeeDB.getEmployee( self.cursor, self.eid)
		msg = self.eid + " " + empdata['first_name'] + " " + empdata['last_name'] +" "
		allallocations = allocationsDB.getAllocations(self.cursor)
		aid=None
		if allallocations == None:
			msg += "0 0 0"
			self.sendData(msg)
			return
		for allocation in allallocations:
			eids=allocation['eid'].split(',')
			for eid in eids:
				if eid==self.eid:
					aid=allocation['aid']
					cid=allocation['cid']
		if aid != None and cid != None:
			allocationdata = allocationsDB.getAllocation(self.cursor, aid)
			msg+="1 "
			timein = 0
			timeout = 0
			presentDate = datetime.datetime.now().strftime('%Y-%m-%d')
			data = {}
			data['eid'] = empdata['eid']
			data['req_date'] = presentDate
			flag = requestDB.searchRequest(self.cursor,self.db,data)
			if flag == True:
				data = requestDB.getRequest(self.cursor, empdata['eid'], presentDate)
				timein = data['time_in']
				timeout = data['time_out']
			else:
				timein = empdata['time_in']
				timeout = empdata['time_out']
			if allocationdata['direction']=="pickup":
				msg+="pickup "+timein
			else :
				msg+="drop "+timeout
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
				msg = "cabdetails "+cid + " " + driver['first_name'] +" "+ driver['last_name'] +" "+driver['contact_number']+" "+allocationdata['atime']+" "+allocationdata['change_flag']+" "+allocationdata['aid']
				#employeeDB.getEmploye(allocationdata['eid'])[]
				print msg
				self.sendData(msg)
			else :
				self.sendData("empty")
			#self.sendData("done")

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
		allocationsDB.cancelAllocation(self.cursor, aid, self.eid)
		self.db.commit();
		#include adding comments to database as msgList[3]

	def addRequest(self,msgList):
		startdate=msgList[2].split('/')
		enddate=msgList[3].split('/')
		print(str(startdate[0])+" "+str(startdate[1])+" "+str(startdate[2]))
		date1 = datetime.date(int(startdate[0]),int(startdate[1]),int(startdate[2]))
		date2 = datetime.date(int(enddate[0]),int(enddate[1]),int(enddate[2]))
		day = datetime.timedelta(days=1)
		print (str(date1)+" "+str(date2)+" ")
		data={}
		while date1 <= date2:
			data['eid']=self.eid
			data['req_date']=str(date1)
			data['time_in']=msgList[4]
			data['time_out']=msgList[5]
			print("add")
			requestDB.addRequest(self.cursor, self.db, data)
			self.db.commit()
			date1 = date1 + day
		self.db.commit()

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
					#self.sendData( "done" )
				elif msgList[0] == 'cabdetails' :
					print 'cab details'
					self.getCabDetails()
					#self.sendData("cabdetails C01 fname lname 9999999999 12:00:00")
				elif msgList[0] == 'changepassword' :
					print 'change password'
					a=self.changePassword(msgList)
					self.db.commit()
					if a==1:
						self.sendData( "donechangepassword" )
					else:
						self.sendData( "failedchangepassword" )
				elif msgList[0] == 'feedback':
					print 'send drivers'
					self.sendFeedback(msgList)
					self.sendData( "donefeedback" )
				elif msgList[0] == 'cancel':
					print'get allocations'
					self.cancelAllocation(msgList)
					self.db.commit()
					self.sendData("donecancel")
				elif msgList[0] == 'request':
					print'request'
					self.addRequest(msgList)
					self.sendData("donerequest")
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
