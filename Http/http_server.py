import socket
import threading
import re
import string
import random
import smtplib
import datetime
from DBInterface import DBConnection, loginDB, employeeDB

import signal  # Signal support (server shutdown on signal receive)
import time    # Current time

class Http_Server (threading.Thread):
	
	def __init__(self, conn, msg, db):
		threading.Thread.__init__(self)
		self.conn = conn
		self.db = db
		self.cursor = self.db.getCursor()
		self.msg = msg
		self.www_dir = 'Http/www' # Directory where webpage files are stored

	def _gen_headers(self,  code):
		# determine response code
		h = ''
		if (code == 200):
			h = 'HTTP/1.1 200 OK\n'
		elif(code == 404):
			h = 'HTTP/1.1 404 Not Found\n'
			# write further headers
		current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		h += 'Date: ' + current_date +'\n'
		h += 'Server: HumSafar-HTTP-Server\n'
		h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request
		return h
	 
	def run(self):
		self.process_request(self.msg)
	
	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join( random.choice(chars) for _ in range(size) )
	
	def sendEmail(self, eid, username, password):
		fromAddr = 'humsafarcabs@yahoo.com'
		toAddr = employeeDB.getEmail( self.cursor, eid )
		subj='HumSafar Verification'
		date= str(datetime.datetime.now().strftime('%d/%m/%Y'))
		
		message_text="Hello,\n\nHumSafar password for "+username+" is "+password
		message_text+="\n\nLogin using the username and password to start the service"
		msg = "From: HumSafar <%s>\nTo: <%s>\nMIME-Version: 1.0\nContent Type: text/html\nSubject: %s\nDate: %s\n\n%s" % ( fromAddr, toAddr, subj, date, message_text )	 	
		
		username = str('humsafarcabs@yahoo.com')  
		password = str('kannan119504')  
		print 'sending email to ' + toAddr + ' from ' + fromAddr
		server = smtplib.SMTP("smtp.mail.yahoo.com",587)
		server.starttls()
		print 'attempting login'
		server.login(username,password)
		print 'sending mail'
		server.sendmail(fromAddr, toAddr,msg)
		print 'sent'
		server.quit() 
	
	def sendFile(self, file_requested):
		try:
			file_handler = open(file_requested,'rb')
			response_content = file_handler.read() # read file content
			file_handler.close()
			response_headers = self._gen_headers(200)

		except Exception as e: #in case file was not found, generate 404 page
			print ("Warning, file not found. Serving response code 404\n", e)
			response_headers = self._gen_headers(404)
			response_content = "<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
		
		server_response =  response_headers.encode() # return headers for GET and HEAD
		server_response +=  response_content  # return additional conten for GET only
		#print str(server_response)
		self.conn.send(server_response)
	
	def createAccount(self, eid, username, password):
		data={}
		data['username'] 	= username
		data['password'] 	= password
		data['type']		= 'emp'
		data['eid']			= eid
		loginDB.insertLogin(self.cursor, data)
		employeeDB.setUsername(self.cursor, eid, username)		
		   
	def process_request(self, data):
		string = bytes.decode(data) #decode it to string
		
		request_method = string.split(' ')[0]
		if (request_method == 'GET') | (request_method == 'HEAD'):
		         #file_requested = string[4:]

		         # split on space "GET /file.html" -into-> ('GET','file.html',...)
			file_requested = string.split(' ')
			file_requested = file_requested[1] # get 2nd element

		         #Check for URL arguments. Disregard them
			file_requested = file_requested.split('?')[0]  # disregard anything after '?'

			if (file_requested == '/'):
				file_requested = '/index.html' # load index.html by default
			
			file_requested = self.www_dir + file_requested
			print ("Serving web page [",file_requested,"]")

			self.sendFile(file_requested)
				
			print ("Closing connection with client")
			self.conn.close()
		
		elif request_method == 'POST' :
			extractedData = re.search('eid=(.*)&username=(.*)',string)
			eid = str( extractedData.group(1) )
			username = str( extractedData.group(2) )
			password = self.id_generator()
			print 'EID : ' + eid + ' Username : ' + username + ' Password : ' + password
			
			status = employeeDB.getEmployee(self.cursor, eid)
			if status == None:
				self.sendFile(self.www_dir+'/invalidEid.html')
				self.conn.close()
				return
			status = loginDB.checkEid(self.cursor, eid)
			if status == True:
				self.sendFile(self.www_dir+'/alreadyRegistered.html')
				self.conn.close()
				return
			status = loginDB.checkUsername( self.cursor, username)
			if status == True:
				self.sendFile(self.www_dir+'/existingUsername.html')
				self.conn.close()
				return
			self.createAccount(eid, username, password)
			self.sendFile(self.www_dir+'/registered.html')
			self.sendEmail(eid, username, password)
			self.db.commit()
		else:
			print("Unknown HTTP request method:", request_method)
			self.conn.close()
         
	
