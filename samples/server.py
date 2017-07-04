import socket
import time

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.allow_reuse_address = True
host = "192.168.2.33"
print "Host Name : ", host
port = 2345
s.bind( (host,port) )
s.listen(5)
c, addr = s.accept()
print "connected"
try:
	msg = str( c.recv(1024) )
	print msg
	print len(msg)
	if msg == "companyinterface":
		c.send("accepted")
		c.send("hello" )
	else :
		c.send("rejected")
except:
	print "Something went wrong"
finally:
	print "finally"
	c.close()
	s.shutdown(socket.SHUT_RDWR)
	s.close()
#while True:
#	s.listen(5)
#	c, addr = s.accept()
#	try:
#		print s.getHostName()
#		c.close()
#	except KeyboardInterrupt:
#		c.close()




