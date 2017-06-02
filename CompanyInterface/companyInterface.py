
class CompanyInterface:

	def __init__( self, connection ):
		self.msg = "Company Interface"
		self.connection = connection
		
	def printMsg( self ):
		print self.msg


