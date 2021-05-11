#This time, after we change mac, we'll input :ifconfig <iface> and read the output to verify if the mac has changed. Can use regex101.com to generate the required pattern.

import subprocess								## module used to run os commands using python				
import optparse
import re

def get_user_input():
	
	parse_object=optparse.OptionParser()
	parse_object.add_option("-i","--interface",dest="interface",help="interface to change")
	parse_object.add_option("-m","--mac",dest="mac_address",help="new mac address")
	
	return parse_object.parse_args()

def change_mac_address(UI,UM):						#user interface and user mac address as args

	subprocess.call(["ifconfig", UI, "down"]) 
	subprocess.call(["ifconfig", UI, "hw", "ether", UM])
	subprocess.call(["ifconfig", UI, "up"]) 

def control_new_mac(interface):
	
	ifconfig=subprocess.check_output(["ifconfig",interface])
	new_mac=re.search(r"\w\w:\w\w\:\w\w:\w\w:\w\w:\w\w",str(ifconfig))	
		#regex to scrap out the actual mac address from the output given, also for pytyhon3-> str(ifconfig)
	if new_mac:
		return new_mac.group(0)					#if multiple results found, will print the first one, mostly only one result will be there.		
	else:
		return None

print("mac changer started")
(user_input,arguments)=get_user_input()
change_mac_address(user_input.interface,user_input.mac_address)	
finalized_mac=control_new_mac(user_input.interface)			#for pytyhon3-> str(user_input.interface)

if finalized_mac == user_input.mac_address:
	print("successful")
else:
	print("error")

#input example: :python <projectName>.py -i eth0 -m 00:11:22:33:44:55