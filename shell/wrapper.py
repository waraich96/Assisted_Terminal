import os
import sys
sys.path.append('..')
from colours.colours import *
from shell.shell import AssistedTerminalShellClass

# define wrapper
class AssistedTerminalWrapperClass():

	def __init__( self ):		
		os.system("clear")
		# display welcome text
		print(B("_" * 79 + "\n\n" ) + c(\
" ... this tool was developed by Bahawal Waraich for his final year project\n"+
			  	B("_" * 79 + "\n\n")))


	def run( self ):
		# run
		AssistedTerminalShell = AssistedTerminalShellClass()
		AssistedTerminalShell.run()
