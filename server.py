import socket
from CompanyInterface import companyInterface
from AgencyInterface import agencyInterface

def server():
	serverSocket = socket.socket()
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1 )
	#serverSocket.setsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF, 100 )
	host = "192.168.1.8"
	port = 2345
	serverSocket.bind( (host,port) )
	try:
		while True:
			serverSocket.listen(5)
			clientConnection, clientAddress = serverSocket.accept()
			print "received request from : ", clientAddress
			msg = str( clientConnection.recv(1024) )
			msgList = msg.split()
			interfaceType = msgList[0]
			print "interface type : ", interfaceType
			if interfaceType == 'companyinterface': #spawn a thread for each client
				companyInterface.CompanyInterface( clientConnection, msgList ).start()
			elif interfaceType == 'agencyinterface':
				agencyInterface.AgencyInterface( clientConnection, msgList ).start()
	except:
		print 'something went wrong : server'
	finally:
		serverSocket.shutdown(socket.SHUT_RDWR)
		serverSocket.close()


server()
