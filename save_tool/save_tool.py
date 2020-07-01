import json
import base64
import os
from colours.colours import *

# define save tool
class SaveToolClass():

	def __init__( self, parent ):
		
		# set default attributes
		self.saveFileName = 'tmp/assisted_terminal.log'
		self.loadedData = None
		self.parent = parent
		
		# check if the path exists before trying to open
		if ( os.path.exists( self.saveFileName ) ):	self.saveHandle = open( self.saveFileName, 'r' )
		else: self.saveHandle = open( self.saveFileName, 'w' )


	def load( self ):
		# load courses
		if ( self.saveHandle.closed ):	self.saveHandle = open( self.saveFileName, 'r' )
		if ( self.saveHandle.mode != 'r' ):
			self.saveHandle.close()
			self.saveHandle = open( self.saveFileName, 'r' )

		# decode the data to a dictionary 
		try: self.loadedData = json.loads( base64.b64decode( self.saveHandle.read() ))
		except ValueError: return False

		# check that data has loaded
		if self.loadedData != {}:
			
			# display text
			print(M('''
It looks like you've used this tool before! I'll bring you right back to where 
you left off. If you'd like to revisit older course or classes, enter `@help`!'''))

			# load attributes
			self.parent.CourseBook.loadCourse( self.loadedData["currentCourse"] )
			self.parent.CourseBook.coursePointer = self.loadedData["coursePointer"]
			self.parent.CourseBook.newCoursePointer = self.loadedData["coursePointer"]

			return True


	def save( self, data ):

		# open if necessary
		if ( self.saveHandle.closed ): self.saveHandle = open( self.saveFileName, 'w' )
		if ( self.saveHandle.mode != 'w' ):
			self.saveHandle.close()
			self.saveHandle = open( self.saveFileName, 'w' )

		# save data
		self.saveHandle.seek(0)
		self.saveHandle.write(json.dumps( data ))

	# delete file magic method
	def __del__( self ): self.saveHandle.close()
