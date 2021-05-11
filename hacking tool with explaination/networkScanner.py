'''
Network scanner:
Create an arp request, broadcast it (to evryone connected on the same network), get the responses and process it:-
Can open windows to check as it would be on the same network.
'''

import scapy.all as scapy
import optparse

def get_user_input():
	parse_object = opt.parseOptionParser()
	parse_object.add_option("-i", "--ipaddress", dest="ip_address", help="enter IP address")

	(user_input,arguments) = parse_objects.parse_args()
	
	if not user_input.ip_address:    											#used 'if not' as an alterantive of 'if-else'
		print("enter IP")

	return user_input


def scan_my_network(ip):
	#creating arp request
	arp_request_packet=scapy.ARP(pdst=ip)	#creates a request packet, actually we are not supposed to change the args,but we do to get info about others. 10.0.2.1/24 is the IP range.
	# :scapy.ls(scapy.ARP()) display the attributes/arguments of scapy.ARP, IPField(pdst) = 0.0.0.0 (by deafault) as you can see, which we need to change.


	#Broadcasting
	broadcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")						#if not by default
	#Again do :scapy.ls(scapy.Ether()) , dst=destination for arp request(ff:ff:ff:ff:ff:ff which is by default means broadcast it all over the network), src=source of arp request
	combined_packet = broadcast_packet/arp_request_packet	#We need to combine the request and broadcast packets, hence it combines the 2 packets.	
	#sr function used for sending packets and receiving answers. It returns a couple of packet and answers, and (also) the unanswered packets.
	
	#getting responses and processing it
	(answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)		#returns a tuple, hence used ( , )						
	#timeout is used or else it will wait for the unanswered packet, and it might get stuck, hence we want it to move on.
	answered_list.summary()														#displays the result in a good format to read.

user_ip_address=get_user_input()
scan_my_network(user_ip_address.ip_address)	

#Now in terminal , :python <projectName>.py -i <fullIpRange/10.0.2.1/24>
#If not working in python3 try, updating scapy (pip install scapy)