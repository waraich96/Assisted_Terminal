
import os
import textwrap
from colours.colours import *
import readline
import colorama
import sys
import socket
import subprocess
from save_tool.save_tool import SaveToolClass
from courses.course_book import CourseBookClass

# define assistance class
class AssistedTerminalShellClass():

	def __init__( self ):

		# set default attributes
		self.SaveTool = SaveToolClass( parent = self )
		self.CourseBook = CourseBookClass( parent = self )

		self.usingTime = True
		self.timeOn = True

		self.enteredInput = ""

		# special commands
		self.commands = {
			"@help" 		: 		self.doHelp,		
			"@courses" 		:	 	self.CourseBook.selectCourse,
			"@classes" 	:	 	self.CourseBook.selectClass,
		}

		# define special cases
		self.specialCases = {
			"quit": self.sayGoodbye,
			"cd": self.changeDir,
			"nano": self.protectNano,
			"sudo passwd guest": self.changeGuestPasswd,
		}

	# change password
	def changeGuestPasswd(self): os.system("sudo passwd guest")

	# not possible to run nano
	def protectNano(self):
		print(R("Assisted Terminal cannot handle running nano!"))
		print(R("The line buffering causes it to choke... sorry!"))

	# change directory
	def changeDir( self ):
		
		# move to directory
		toDir = " ".join( self.enteredInput.split(" ")[1:] )
		
		# edit the inputted string
		toDir = toDir.replace("~", os.environ['HOME'] )

		# if there is nothing, return to the home menu
		if ( toDir == '' ):	os.chdir(os.environ['HOME'])
		
		# move to directory
		else:
			try: os.chdir(toDir)
			# display error if directory does not exist
			except OSError:	print("bash: cd: " + toDir + ": No such file or directory")

	def doHelp( self ):
		
		# display help text
		print( textwrap.dedent('''

	@help:		View this help text.
	@courses:	Select from a menu of courses what to study from.
	@classes:	Choose a class from the course that you are on.

	TO ADD: @setspeed

		''' ))


	def error( self, e ):
		# display error
		print(colorama.Back.BLACK + R("Oh no! I hit an error!"))
		print(r("\n" + str(e)) , colorama.Back.RESET)



	def prompt( self ):
		
		# turn off time
		if ( self.usingTime and self.timeOn ):	self.timeOn = False

		# display shell UI
		ps1 = "".join([	
						colorama.Fore.MAGENTA, colorama.Style.BRIGHT, 
						"Assisted Terminal SHELL: ",
						colorama.Fore.GREEN, colorama.Style.BRIGHT, 
						os.environ['USER'], '@', socket.gethostname(), 
						colorama.Fore.BLUE,
						" ", os.getcwd(), " $ ", 
						colorama.Fore.MAGENTA, colorama.Style.BRIGHT, 
						". . .",
						colorama.Style.NORMAL, colorama.Fore.RESET,
						"\n"
					  ]).replace( os.environ["HOME"], "~" )
		
		# write text
		sys.stdout.write(ps1)

		# get input without whitespace
		self.enteredInput = input().strip()
		sys.stdin.flush()
		# add input to history
		readline.add_history( self.enteredInput)

	def sayGoodbye( self ):
		# display goodbye text
		print(C("\n\nGoodbye!") )
		print(B("_" * 78 + "\n"))

		# exit
		exit()


	def process( self ):
		
		# check text
		if self.enteredInput == "": return

		# break up text into arguments
		command = self.enteredInput.split(" ")[0]
		if command in self.specialCases.keys():
			# Run the corresponding function that follows the 
			self.specialCases[command]()
			return True
		if self.enteredInput in self.commands.keys():
			# Run the corresponding function that follows the 
			self.commands[self.enteredInput]()
			raise KeyboardInterrupt
		


		''' If they actually entered something, treat it as a command '''
		try:
			# try to run the command
			p = subprocess.Popen(	self.enteredInput, 
									shell = True,
									stdout = subprocess.PIPE, 
									stdin=subprocess.PIPE,
								)

			while ( p ):
				# loop through the messages in the course
				try:
					# display next instructions
					sys.stdout.write( self.CourseBook.somethingToSayInbetween)
					sys.stdout.write(str(str(next(p.stdout)))[2:-3]+"\n")
					
				except StopIteration:
					break

		except OSError: print(self.enteredInput + ": command not found")



	def run( self ):
		''' The main loop of the program is here, creating the shell...'''
		# if nothing is loaded, select course
		if (not self.SaveTool.load() ):
			self.CourseBook.selectCourse()
			self.CourseBook.selectClass()

		# run the program
		while True:
			# try to run the program
			try: self.CourseBook.go()
			except KeyboardInterrupt:
				# stop execution if there is a keyboard interrupt without crashing the program
				self.timeOn = False
				sys.stdout.write("^C\n")
				continue
			# display error text
			except Exception as e:	self.error(e)
