from DBInterface import DBConnection, employeeDB, employeeAddressDB, allocationsDB
import threading
from datetime import datetime

class CarPool:
	
	def __init__(self):
		self.currentTime = datetime.now().time()
	
	def connectDB( self ): #connect to the sql database and create cursor object
		self.db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
		self.db.connect()
		self.cursor = self.db.getCursor()
	
	def getEidsList(self):
		self.postalCodeList = employeeAddressDB.getDistinctPostalCodes()
		
	def doAllocations(self):
		self.currentTime = datetime.now().time()
		print str(self.currentTime)
		return
