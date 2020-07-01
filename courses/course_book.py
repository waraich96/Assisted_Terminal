import json
from colours.colours import *
import glob
import sys
import textwrap
import time
import os
try:
	import curses
except:
	pass

# define the course book
class CourseBookClass(object):

	def __init__( self, parent, filename = "" ):
		
		# define initial state
		self.parent = parent
		self.punctionStops = "\n.,!?-"
		path = os.path.dirname(os.path.realpath(__file__))
		self.coursePointer = 0
		self.newCoursePointer = 0
		self.courseIsLoaded = False
		self.selectedCourseNum = 0
		self.currentCourse = {}
		self.seenEntries = {}
		self.somethingToSayInbetween = ""

		# get courses
		self.availableCourses = [file for file in 
					sorted(glob.glob(os.path.join(path, '.*.json')))]
		# make courses look nice
		self.cleanedAvailableCourses = [l.split('/')[-1].replace('.json','').replace('lesson_','_').replace('_',' ').title()	for l in self.availableCourses  ]

	def say( self, text ):
		
		# add lines at the end of a messge
		if ( not text.endswith('\n\n') ): text += '\n\n'

		# loop through the text and print the characters
		for character in text:
			sys.stdout.write(character)
			sys.stdout.flush()
			# add delay if required
			if self.parent.usingTime and self.parent.timeOn:
				# wait slightly longer for punctuation than for most characters
				if character in self.punctionStops:
					time.sleep(0.12)
				else:
					time.sleep(0.04)

	def isInDir( self, directory = None ):
		# check if something is in a directory
		if directory == None: return True
		# or go to the default directory
		else: return os.getcwd() == directory.replace("~", os.environ["HOME"])

	def selectCourse( self ):
		# check if a course is loaded
		if (not self.courseIsLoaded):	print(M("\nIt looks like a course has not yet been loaded."))
		else:
			# print current course
			print(M("\nYou already have ") + C(self.currentCourse["name"]) + M(" loaded."))
			print(M("Load something else?"))

			# start not entered
			entered = False
			while ( not entered ):
				# check whether to load course
				answer = input("(y/n): ").lower()
				if answer == "yes" or answer == "y":
					# set default values
					self.courseIsLoaded = False
					self.coursePointer = 0
					self.newCoursePointer = 0
					entered = True
					pass
				elif answer == "no" or answer == "n":
					return
				else:
					print(R("\nPlease enter yes or no."))
		# select course
		print(M('''
Please select one of the available courses by entering the corresponding number.
Enter the number '0' to go back to what you were doing.\n'''))		

		# print out list of available courses
		for l in self.cleanedAvailableCourses: print("\t" + l)
		print("\n\n")

		
		while ( not self.courseIsLoaded ):
			# get course number
			print(M("course #:"))
			self.selectedCourseNum = input()

			# end if there is a certain input
			if ( self.selectedCourseNum == "0" or self.selectedCourseNum == "quit" ):	return
			
			# check if course is a number
			try: self.selectedCourseNum = int( self.selectedCourseNum ) - 1
			except:
				print(R("That does not look like a valid input. Please try again."))
				continue
			
			# check if course is a valid selection
			if ( self.selectedCourseNum >= 0 and self.selectedCourseNum < len(self.availableCourses) ):
				print(B("_"*79 + "\n"))
				self.loadCourse( self.availableCourses[self.selectedCourseNum] )
				return
			else:
				print(R("That does not look like a valid input. Please try again."))
				continue


	def goToNextCourse( self ):
		# print messages
		print(M("It looks like you are all done with this course!"))
		print(M("I'm going to move you to the next one. You are now on course:\n"))

		# increment course
		nextCourseNum = self.selectedCourseNum + 1

		# check if final course is complete
		if ( nextCourseNum > len( self.availableCourses ) ):
			# display messages
			print( Y("Actually -- there are no more courses!") )
			print( Y("You're all done for now... go practice Linux!") )

			# save progress
			self.parent.SaveTool.save( "done" )

			# exit
			exit()
		else:
			# display next course
			nextCourseName = self.cleanedAvailableCourses[nextCourseNum-1]
			print("\t" + nextCourseName + "\n\n")

			# set default variables
			self.coursePointer = 0
			self.newCoursePointer = 0
			self.selectedCourseNum += 1
			self.loadCourse( self.availableCourses[nextCourseNum] )

	def loadCourse( self, courseIdentifier ):
		
		# try to open file
		try: self.file_handle = open(courseIdentifier, 'r')
		except IOError:
			# The file does not exist.
			raise Exception("This file does not exist!")
		
		# load course
		self.currentCourse = json.loads( self.file_handle.read() )
		self.selectedCourseNum = int(self.currentCourse['name'].split(".")[0]) - 1
		self.courseIsLoaded = True

	def selectClass( self ):
		if ( self.currentCourse == {} ):
			# if there is no course, try again
			print(R("There is currently no course loaded!"))
			print(R("Enter `@courses` to select one to load."))
			return 
		
		# display current course
		print(M('''
The current course that is loaded is: ''') + C(self.currentCourse["name"])+ M('''".

Please select one of the classes you would like to jump to.
The course you are currently looking at is highlighted in '''+ y('yellow') + M('''.
Enter the number '0' to go back to what you were doing.\n''')))

		# Display all of the classes that are available in that course.
		for i in range( len(self.currentCourse["classes"])):
			number = str(i + 1)
			if i == self.coursePointer:
				print("\t" + Y( number + ". " +self.currentCourse["classes"][i]["title"]))
			else:
				print("\t" + number + ". " + self.currentCourse["classes"][i]["title"])
		print("\n"*2)
		
		selected = False
		
		# loop through classes
		while ( not selected ):
			print(M("class #:"))
			selectedClassNum = input()

			# get the class number
			if ( selectedClassNum == "0" or selectedClassNum == "quit" ):
				return

			# check if this is a number
			try: selectedClassNum = int( selectedClassNum ) - 1
			except:
				print(R("That does not look like a valid input. Please try again."))
				continue

			# check if selection is in range
			if ( selectedClassNum >= 0 and selectedClassNum < len(self.currentCourse["classes"]) ):

				# set pointers
				self.coursePointer = selectedClassNum
				self.newCoursePointer = selectedClassNum
				# create a line
				print(B("_"*79 + "\n"))
				return
			else:
				# display error text
				print(R("That does not look like a valid input. Please try again."))
				continue



	def go( self ):
		
		# Save all our progress so far.
		self.parent.SaveTool.save( \
			{ 	"currentCourse" : self.availableCourses[self.selectedCourseNum],
				"coursePointer" : self.coursePointer } )

		currentCourse = self.currentCourse["classes"][self.coursePointer]

		# Begin to load everything from the course and current class...
		if ( "text" in currentCourse.keys() ): text = currentCourse["text"]

		# check if command is correct
		if ( "wantedCommand" in currentCourse.keys() ): 
			wantedCommand = currentCourse["wantedCommand"]

			# load the correct directory
			if ( "correctDir" in currentCourse.keys() ): 
				correctDir = currentCourse["correctDir"]
				if correctDir.endswith('/'): correctDir = correctDir[:-1]
			else: correctDir = None

			# check if there is a specific phrase required
			if ( "incorrect" in currentCourse.keys() ): incorrect = currentCourse["incorrect"]
			# check if class is incomplete or requires more
			if "in_between_text" in self.currentCourse["classes"][self.coursePointer].keys(): self.somethingToSayInbetween = R( self.currentCourse["classes"][self.coursePointer]["in_between_text"] )
			else: self.somethingToSayInbetween = ""

		else:
			# This is the very end of the course. Say your last words and move on.
			self.say(C( text ))

			self.goToNextCourse()
			return


		while ( self.newCoursePointer == self.coursePointer ):
			
			# Prompt for this class.
			time.sleep(1)
			self.say(C( text ))


			# Determine what we really want the user to type in.
			expectedArg = wantedCommand.split()
			expectedArgNum = len(expectedArg)


			# While they have not entered their command, keep prompting.
			while (wantedCommand not in self.seenEntries):

				self.parent.prompt()

				if ( self.isInDir( correctDir ) ):

					# Analyze what they entered and determined if it is correct
					args = self.parent.enteredInput.split()
					argNum = len(args)

					# check if arguments are correct
					if ( argNum != expectedArgNum ):
						# display incorrect text
						self.parent.process()
						print( Y("\n" + textwrap.dedent(incorrect) + "\n") )
						continue
						
					correct = True
					# check that all the arguments are correct
					for arg in range(expectedArgNum):
						if expectedArg[arg] == "???":
							if expectedArgNum == argNum:
								continue
							else: correct = False
						if expectedArg[arg] != args[arg]:
							correct = False
					# if everything is correct, move on
					if correct:
						self.newCoursePointer += 1
						self.parent.timeOn = True
				else:
					
					# display text about being in the wrong directory
					self.parent.process()

					if ( not self.isInDir( correctDir ) ):
						print(R( "\nYOU ARE IN THE WRONG DIRECTORY" ))
						print(R( "To continue, please change directory to '" + correctDir + "'\n\n" ))

					continue
				
				self.parent.process()

				# check pointer
				if ( self.newCoursePointer == self.coursePointer ):	print( Y("\n" + textwrap.dedent(incorrect) + "\n") )
				else: return 
			
			# reset attributes
			self.somethingToSayInbetween = ""
			self.seenEntries = []

		else:
			# update pointer
			self.coursePointer = self.newCoursePointer
