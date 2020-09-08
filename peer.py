import csv
import math
from socket import *
import _thread as thread
import random
import time
import json

seeds = []
peers = []
peerList = set()
listener = socket(AF_INET, SOCK_STREAM)
listener.listen(10)
selfAddr = list(listener.getsockname())
messageList = []
livenesssTestCount = {}
print(type(selfAddr))
print(selfAddr)
# addrToSocket = {}


def broadcastMsg(msg):
	msg = msg.encode()
	for p in peers:
		p.send(msg)


def generateMsg():
	count = 0
	while count<10:
		toSend = str(time.strftime("%x,%X", time.gmtime())) + ':' + str(selfAddr[0]) + ':' + str(count+1)
		broadcastMsg(toSend)
		count += 1
		time.sleep(5)

def forwardMsg(msg, conn):
	if msg in messageList:
		pass
	messageList.append(hash(msg))
	msg = msg.encode()
	for p in peers:
		if p != conn:
			p.send(msg)
		#add to ML


def reportDead(Addr):
	toSend = 'Dead Node:'+Addr[0]+':' + Addr[1]+':' +str(time.strftime("%x,%X", time.gmtime())) + ':' + selfAddr[0] +','+str(selfAddr[1])
	for seed in seeds:
		seed.send(toSend.encode())


def testLiveness():
	while True:
		time.sleep(13)
		toSend = 'Liveness Request:'+str(time.strftime("%x,%X", time.gmtime()))+':'+str(selfAddr[0]) +','+str(selfAddr[1])
		for key,value in livenesssTestCount.items():
			if value == 3:
				livenesssTestCount.remove(key)
				reportDead(key)
				continue
			livenesssTestCount[key] += 1
		broadcastMsg(toSend)
	pass	

def confirmLiveness(msg):
	return 'Liveness Reply'+':'+msg[1]+':'+msg[2]+':'+str(selfAddr[0]) +','+str(selfAddr[1])# check once

def receiver():
	peerAddr = listener.recv(1024) #for_updating_seeds_upon_finding out dead node
	while True:
		msg = listener.recv(1024)
		if(msg == ''):
			listener.close()
			peers.remove(listener)
			break
			#if null string received means connection dead but we still need to send livenesss requests and wait for response but calling recv again gives error
		msg = msg.split(':')
		if(msg[0] == 'Liveness Request' ):
			confirmLiveness(msg)
		elif(msg[0] == 'Liveness Reply'):
			livenesssTestCount[msg[-2].split(',')] -= 1
		else:
			forwardMsg(msg, listener)

def main():
	# connect_seeds()
	with open('config.csv') as cfg:
		cfg = list(csv.reader(cfg, delimiter=':')) # delimiter : why?
		n = len((cfg))
		cfg = random.sample((cfg), (math.floor(n/2)+1))
		for entry in cfg:
			try: 
				s = socket(AF_INET, SOCK_STREAM)
			except error as err: 
				print("error creating socket ",err )
			s.connect((entry[0], int(entry[1])))
			seeds.append(s)

	
	#get PL
	peerList = set()
	for s in seeds:
		data = json.dumps(selfAddr)
		s.send(data.encode())#listener port number
		msg = s.recv(1024)
		msg = msg.decode()
		msg = json.loads(msg)
		print(msg)
		print(type(msg))
		peerList.union(set(tuple(i) for i in msg))
		# peerList.union(set(msg))

	# pl =pl.unique() ???
	#connecting to peers 
	# print(pl)
	peerList = list(peerList)
	noOfPeers = len(peerList)
	if noOfPeers>1:
		upperLimit = min(noOfPeers, 4)
		peerList = random.sample(peerList, random.randint(1,upperLimit))

	for peerAddr in peerList:
		try: 
			p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err: 
			print("error creating socket ",err )
		p.connect(peerAddr)
		peers.append(p)
		livenesssTestCount[peerAddr] = 0
		thread.start_new_thread(receiver, (p, peerAddr))
		
		# addrToSocket[(ip,port)] = p

	thread.start_new_thread( generateMsg, () )
	thread.start_new_thread( testLiveness, () )

	while True:
		c, addr = listener.accept()
		peers.append(c)
		livenesssTestCount[addr] = 0
		thread.start_new_thread(receiver,(c,addr))
		#accept listening port
		
		# addrToSocket[addr] = c 




if __name__ == '__main__':
	main()