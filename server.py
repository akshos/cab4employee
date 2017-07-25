import socket
from CompanyInterface import companyInterface
from AgencyInterface import agencyInterface
from EmployeeInterface import employeeInterface
from DBInterface import DBConnection

threadList = []

db = DBConnection.DBConnection("localhost", "cab4employee", "", "cab4employee")
db.connect()

def server():
	serverSocket = socket.socket()
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1 )
	#serverSocket.setsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF, 100 )
	host = "192.168.2.33"
	port = 2345						
	serverSocket.bind( (host,port) )
	global db
	try:
		while True:
			global threadList
			clientThread = None
			serverSocket.listen(5)
			clientConnection, clientAddress = serverSocket.accept()
			print "received connection from : ", clientAddress
#			msg = str( clientConnection.recv(1024) )
#			print 'Recieved initial message : ' + msg
#			msgList = msg.split()
#			interfaceType = msgList[0]
#			print "interface type : ", interfaceType
#			if interfaceType == 'companyinterface': #spawn a thread for each client
#				clientThread = companyInterface.CompanyInterface( clientConnection, msgList, db ).start()
#			elif interfaceType == 'agencyinterface':
#				clientThread = agencyInterface.AgencyInterface( clientConnection, msgList, db ).start()
#			elif interfaceType == 'employeeinterface':
#				clientThread = employeeInterface.EmployeeInterface( clientConnection, msgList, db ).start()
#			else :
#				clientConnection.close()
#			if clientThread != None:
#				threadList.append( clientThread )
			msg = str( clientConnection.recv(1024) )
			print 'Recieved initial message : ' + msg
			msgList = msg.split()
			if len(msgList) == 0:
				print 'Blank request..'
				clientConnection.close()
				continue
			interfaceType = msgList[0]
			print "interface type : ", interfaceType
			if interfaceType == 'companyinterface': #spawn a thread for each client
				clientThread = companyInterface.CompanyInterface( clientConnection, msgList, db ).start()
			elif interfaceType == 'agencyinterface':
				clientThread = agencyInterface.AgencyInterface( clientConnection, msgList, db ).start()
			elif interfaceType == 'employeeinterface':
				clientThread = employeeInterface.EmployeeInterface( clientConnection, msgList, db ).start()
			else :
				print 'invalid interface type'
				clientConnection.close()
			if clientThread != None:
				threadList.append( clientThread )
#				break
	except KeyboardInterrupt:
		raise
	#except:
		#print 'something went wrong : server'
	finally:
		serverSocket.shutdown(socket.SHUT_RDWR)
		serverSocket.close()

print '#######################'
print '# Cab4Employee SERVER #'
print '#######################'

while True:
	try:
		server()
	except KeyboardInterrupt:
		print 'Stopping server...'
		for tread in threadList:
			thread.exit()
		break

for t in threadList:
	t.join()
