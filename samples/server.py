import socket
import time

s = socket.socket()
#s.allow_reuse_address = True
host = "192.168.43.72"
print "Host Name : ", host
port = 1235
s.bind( (host,port) )
s.listen(5)
c, addr = s.accept()
print "connected"
try:
	msg = str( c.recv(1024) )
	print msg
	print len(msg)
	if msg == "companyinterface":
		c.send("accepted\n")
		c.send(" hello" )
	else :
		c.send("rejected")
		c.close()
except:
	c.close()
c.close()
	
#while True:
#	s.listen(5)
#	c, addr = s.accept()
#	try:
#		print s.getHostName()
#		c.close()
#	except KeyboardInterrupt:
#		c.close()




