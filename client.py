import socket
import time

s = socket.socket()
#host = "192.168.2.33"
host = "192.168.2.33"
port = 2345
try:
	s.connect( (host,port) )
	s.send("companyinterface login akshos kannan")
	reply = str( s.recv(1024) )
	print reply
	s.send("hello")
except:
	print "Something went wrong"
finally:
	s.close()
s.close()
