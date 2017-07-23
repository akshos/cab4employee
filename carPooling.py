from DBInterface import DBConnection, employeeDB, employeeAddressDB, allocationsDB, requestDB
import threading
import datetime

class CarPool:
	
	def __init__(self):
		self.currentTime = datetime.datetime.now().time()
		self.connectDB()
		self.advanceTime = 1

	def connectDB( self ): #connect to the sql database and create cursor object
		self.db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
		self.db.connect()
		self.cursor = self.db.getCursor()
	
	def getEidsList(self):
		self.postalCodeList = employeeAddressDB.getDistinctPostalCodes()
	
	def setSearchTime(self):
		self.currentTime = datetime.datetime.now().time()
		print str(self.currentTime)
		hr = self.currentTime.hour
		hr = (hr + self.advanceTime)%24
		mn = self.currentTime.minute
		self.searchTime = datetime.time( hour=hr, minute=mn )
		print str(self.searchTime)
		
	def createTimeInView(self):
		hr = self.searchTime.hour;
		mn = self.searchTime.minute;
		starthr = 0
		startmn = 0
		endhr = 0
		endmn = 0
		if mn >= 0 and mn < 30:
			starthr = hr-1
			startmn = 45
			endhr = hr
			endmn = 15
		elif mn >= 30 and mn < 59:
			starthr = hr
			startmn = 15
			endhr = hr
			endmn = 45
		startTime = datetime.time( hour=starthr, minute=startmn )
		endTime = datetime.time( hour=endhr, minute=endmn )
		print str( startTime )
		print str( endTime )			
		employeeDB.createEidWithTimeIn( self.cursor, str(startTime), str(endTime) )
		employeeAddressDB.createTimeInAddress( self.cursor )
		self.db.commit()
	
	def createTimeOutView(self):
		hr = self.searchTime.hour;
		mn = self.searchTime.minute;
		starthr = 0
		startmn = 0
		endhr = 0
		endmn = 0
		if mn >= 0 and mn < 30:
			starthr = hr-1
			startmn = 45
			endhr = hr
			endmn = 15
		elif mn >= 30 and mn < 59:
			starthr = hr
			startmn = 15
			endhr = hr
			endmn = 45
		startTime = datetime.time( hour=starthr, minute=startmn )
		endTime = datetime.time( hour=endhr, minute=endmn )
		print str( startTime )
		print str( endTime )			
		employeeDB.createEidWithTimeOut( self.cursor, str(startTime), str(endTime) )
		employeeAddressDB.createTimeOutAddress( self.cursor )
		self.db.commit()
	
	def createPresentRequests(self):
		presentDate = datetime.datetime.now().strftime('%Y-%m-%d')
		print 'present date ' + presentDate
		requestDB.createPresentRequests(self.cursor, str(presentDate) )
			
	def getPickupTime(self, direction):
		hr = self.searchTime.hour
		if direction == 'pickup':
			hr = hr - 1
		mn = self.searchTime.minute
		pickupTime = datetime.time( hour=hr, minute=mn )
		return str( pickupTime )
	
	def createTimeInAllocations(self):
		allocationID = "AL" + datetime.datetime.now().strftime('%Y%m%d%H%M')
		postalCodes = employeeAddressDB.getTimeInPostalCodes(self.cursor)
		aidCount = 0
		print postalCodes
		for code in postalCodes:
			eidList = employeeAddressDB.getTimeInEidList( self.cursor, code )
			eidlen = len(eidList)
			count = ( eidlen/4 )
			if eidlen%4 != 0:
				count += 1
			print eidList
			for j in range(0,count):
				data = {}
				data['aid'] = str( allocationID + str(aidCount) )
				aidCount += 1
				base = j*4
				data['eid'] = ""
				for i in range( 0, 4 ):
					if (base+i) >= eidlen :
						break
					data['eid'] += str(eidList[base+i]) + ","	
				data['eid'] = (data['eid'])[:-1]
				data['cid'] = "None"
				data['did'] = "None"
				data['atime'] = self.getPickupTime( 'pickup' )
				data['change_flag'] = "0"
				data['iftaken'] = "0"
				data['direction'] = "pickup"
				allocationsDB.insertAllocations( self.cursor, data )
				print str(data)
				self.db.commit()
	
	def createTimeOutAllocations(self):
		allocationID = "AL" + datetime.datetime.now().strftime('%Y%m%d%H%M')
		postalCodes = employeeAddressDB.getTimeOutPostalCodes(self.cursor)
		aidCount = 0
		print postalCodes
		for code in postalCodes:
			eidList = employeeAddressDB.getTimeOutEidList( self.cursor, code )
			eidlen = len(eidList)
			count = ( eidlen/4 )
			if eidlen%4 != 0:
				count += 1
			print eidList
			for j in range(0,count):
				data = {}
				data['aid'] = str( allocationID + str(aidCount) )
				aidCount += 1
				base = j*4
				data['eid'] = ""
				for i in range( 0, 4 ):
					if (base+i) >= eidlen :
						break
					data['eid'] += str(eidList[base+i]) + ","	
				data['eid'] = (data['eid'])[:-1]
				data['cid'] = "None"
				data['did'] = "None"
				data['atime'] = self.getPickupTime( 'drop' )
				data['change_flag'] = "0"
				data['iftaken'] = "0"
				data['direction'] = "drop"
				allocationsDB.insertAllocations( self.cursor, data )
				print str(data)
				self.db.commit()
	
	def doAllocations(self):
		self.setSearchTime()	
		print 'Search time : ' + str(self.searchTime)
		self.createPresentRequests()
		self.createTimeInView()
		self.createTimeOutView()
		self.createTimeInAllocations()
		self.createTimeOutAllocations()
		return
		

