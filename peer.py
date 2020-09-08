import csv
import math
import socket
import thread
import random
# def connect_seeds():
# 	with open('config.csv') as cfg:
# 		cfg = csv.reader(cfg, delimiter=':')
# 		n = len(cfg)
# 		cfg = random.sample(cfg, (floor(n/2)+1))
# 		for entry in cfg:
# 			pass


seeds = []
peers = []
pl = {}
listener = socket(AF_INET, SOCK_STREAM)
selfAddr = listener.getsockname()
# listener.bind(ip, port)
listener.listen(10)
messageList = []

def generateMsg():
	pass

def forwardMsg(msg):
	if msg in messageList:
		pass
	for peer in peers:
		peer.send(msg)

def testLiveness():
	pass	

def confirmLiveness(msg):
	return msg+':'+selfAddr # check once

def receiver():
	connect_to = listener.recv() #for_updating_seeds_upon_finding out dead node
	while True:
		msg = listener.recv(1024)
		if():
			continue
			#if null string received means connection dead but we still need to send livenesss requests and wait for response 
		elif():
			#for gossip
		else:
			#for liveness

def main():
	# connect_seeds()
	with open('config.csv') as cfg:
		cfg = list(csv.reader(cfg, delimiter=':')) # delimiter : why?
		n = len((cfg))
		cfg = random.sample((cfg), (math.floor(n/2)+1))
		for entry in cfg:
			try: 
			    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			except socket.error as err: 
			    print("error creating socket ",err )
			s.connect((entry[0], entry[1]))
			seeds.append(s)
	
	#get PL
	for s in seeds:
		s.send()#listener port number)
		msg = s.recv(1024)
		msg = msg.decode()
		msg = json.loads(msg)
		pl = pl.union(msg)

	# pl =pl.unique() ???
	#connecting to peers 
	# print(pl)
	pl = list(pl)
	pl = random.sample(pl, random.randint(1,4))

	for peer in pl:
		try: 
		    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err: 
		    print("error creating socket ",err )
		ip,port = peer.split(':')
		p.connect((ip,port))
		thread.start_new_thread(receiver, (p, [ip,port]))
		peers.append(p)

	thread.start_new_thread( generateMsg )
	thread.start_new_thread( testLiveness )

	while True:
		c, addr = listener.accept()
	    thread.start_new_thread(receiver,(c,addr))
		#accept listening port
	    peers.append(c)




if __name__ == '__main__':
	main()