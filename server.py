import socket
from CompanyInterface import companyInterface

def server():
	serverSocket = socket.socket()
	serverSocket.setsockopt(socket.TCP_NODELAY, socket.SO_REUSEADDR, 1)
	host = "192.168.2.33"
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
			if interfaceType == 'companyinterface': //spawn a thread for each client
				companyInterface.CompanyInterface( clientConnection, msgList ).start()
	except:
		print 'something went wrong : server'
	finally:
		clientConnection.close()
		serverSocket.shutdown(socket.SHUT_RDWR)
		serverSocket.close()


server()
