import socket
import time

s = socket.socket()
host = "192.168.2.29"
port = 1237

s.connect( (host,port) )
print s.recv(1024)
#print 'Sending first data'
#s.send( "Hello how are you? ")
s.close()

