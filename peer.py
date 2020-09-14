import csv
import math
from socket import *
import _thread as thread
import random
import time
import json
from threading import *

seeds = []									#list of seeds connected
peers = []									# list of peers connected to
peerList = set()
listener = socket(AF_INET, SOCK_STREAM)		# the socket that recieves all messages of this peer from other peers
ip = input("Enter IP: ")					# any ip as long as it is network, port assigned randomly
listener.bind((ip, 0))
listener.listen(10)							
selfAddr = list(listener.getsockname())		#acquire self address where it will listen to be shared wtih other peers
messageList = []							#hashed message list
livenessTestCount = {}
print(selfAddr)								#not required maybe
lock = Lock()

f = open('outputpeer.txt', 'a+')

def broadcastMsg(msg):						#broadcast message to be sent to peers like gossip, liveliness request
	msg = (msg + '|').encode()
	for p in peers:
		p.send(msg)


def generateMsg():							#thread to generates gossip and calls broadcast function for the ten gossip messages
	count = 0
	while count<10:
		toSend = str(time.strftime("%Y/%m/%d %H-%M-%S", time.gmtime())) + ':' + str(selfAddr[0]) + ',' + str(selfAddr[1]) + ':' + str(count+1)		#only requires self address to send
		broadcastMsg(toSend)
		count += 1
		time.sleep(5)

def forwardMsg(msg, conn):					#forwards the recieved messages after checking in message list (used locks to handle simultaneously recieved messages)
	lock.acquire()
	if hash(msg) in messageList:			#checking in message list
		lock.release()
		return
	messageList.append(hash(msg))			#appending in message list
	lock.release()
	senderAddr = conn.getsockname()			#requires the address of peer who forwaded the message
	print(msg + " local timestamp: " + str(time.strftime("%Y/%m/%d %H-%M-%S", time.gmtime())) + senderAddr[0] + ',' + str(senderAddr[1]))
	f.write(msg + " local timestamp: " + str(time.strftime("%Y/%m/%d %H-%M-%S", time.gmtime())) + senderAddr[0] + ',' + str(senderAddr[1]) + '\n')
	f.flush()
	msg = (msg + '|').encode()
	for p in peers:							#forwarding it to all peers except the sender
		if p != conn:
			p.send(msg)


def reportDead(Addr):						#reporting an dead node to all seeds
	toSend = 'Dead Node:'+str(Addr[0])+':' + str(Addr[1])+':' +str(time.strftime("%Y/%m/%d %H-%M-%S", time.gmtime())) + ':' + str(selfAddr[0]) +','+str(selfAddr[1])
	print(toSend)
	f.write(toSend + '\n')
	f.flush()
	for seed in seeds:
		seed.send((toSend + '|').encode())


def testLiveness():										#liveliness request threads
	while True:
		time.sleep(13)									#every 13 seconds
		toSend = 'Liveness Request:'+str(time.strftime("%Y/%m/%d %H-%M-%S", time.gmtime()))+':'+str(selfAddr[0]) +','+str(selfAddr[1])
		toRemove = []
		for key,value in livenessTestCount.items():		#if some peer hasn't replied for 3 consecutive liveness request remove it from the dict and report it dead 
			if value == 3:								#this peer was already removed from peer list when it recieved null string from the closed socket
				toRemove.append(key)
				reportDead(key)
				continue
			livenessTestCount[key] += 1
		for key in toRemove:
			livenessTestCount.pop(key)
		broadcastMsg(toSend)							#send liveness request to remaining peers
	pass	

def confirmLiveness(msg, conn):				#liveness reply message
	toSend = 'Liveness Reply'+':'+msg[1]+':'+msg[2]+':'+str(selfAddr[0]) +','+str(selfAddr[1]) + '|'
	conn.send(toSend.encode())

def receiver(listener):									#recieve all kind of messages and call the required threads
	while True:
		msg = listener.recv(1024)						
		msg = msg.decode()
		if(msg == ''):
			listener.close()
			peers.remove(listener)
			break
			#if null string received means connection dead but we still need to send livenesss requests and wait for response but calling recv again gives error	

		msg = msg.split('|') 							# if multiple message come together we used this as seprator
		msg.pop(-1)										# remove the |

		for item in msg:
			temp = item
			item = item.split(':')
			if(item == ''):
				continue
			if(item[0] == 'Liveness Request' ):			#another peer is asking for liveness confirmation
				confirmLiveness(item, listener)
			elif(item[0] == 'Liveness Reply'):			#A peer sent a liveness confirmation reply, the liveness test count is set to zero
				ip, port = item[-1].split(',')
				livenessTestCount[(ip, int(port))] = 0
			else:										# normal gossip forwarding
				forwardMsg(temp, listener)

def main():
	# connect_seeds()
	with open('config.csv') as cfg:
		cfg = list(csv.reader(cfg, delimiter=':')) 				# our chosen delimiter
		n = len((cfg))
		cfg = random.sample((cfg), (math.floor(n/2)+1)) 		# 1 + n/2 random seeds
		for entry in cfg:
			try: 
				s = socket(AF_INET, SOCK_STREAM)
			except error as err:
				print("error creating socket ",err )
			s.connect((entry[0], int(entry[1])))
			seeds.append(s)										# store seeds connected to in seed list

	
	#get PL
	peerList = []
	for s in seeds:
		data = json.dumps(selfAddr)
		s.send(data.encode()) 			#sending listener port number
		msg = s.recv(1024)				#recieved peerlist from one seed
		msg = msg.decode()	
		msg = json.loads(msg)
		peerList.extend(msg)			#union of all peer lists

	#connecting to peers 
	peerList = set(tuple(i) for i in peerList)
	print("List of Peer Nodes received: ", end='')
	print(peerList)
	# f.write(peerList)
	noOfPeers = len(peerList)
	if noOfPeers>1:
		upperLimit = min(noOfPeers, 4)
		peerList = random.sample(peerList, random.randint(1,upperLimit)) #chosing peers to connect to

	for peerAddr in peerList:
		try: 
			p = socket(AF_INET, SOCK_STREAM)
		except error as err: 
			print("error creating socket ",err )
		p.connect(peerAddr)
		peers.append(p)
		livenessTestCount[peerAddr] = 0									#count the continous liveness request missed by the specific peer
		data = json.dumps(tuple(selfAddr))
		p.send(data.encode())											#sending our own listener address to other peer
		thread.start_new_thread(receiver, (p,))							#reciever thread from the new peer
		

	thread.start_new_thread( generateMsg, () )							#thread that generate gossip message for all peers 
	thread.start_new_thread( testLiveness, () )							#thread that sends liveness request to each peer

	while True:
		c, addr = listener.accept()										# accept new peer request
		peers.append(c)
		peerAddr = c.recv(1024) 										#for_updating_seeds_upon_finding out dead node
		peerAddr = json.loads(peerAddr.decode())
		livenessTestCount[tuple(peerAddr)] = 0
		thread.start_new_thread(receiver,(c,))							#start reciever thread for the new peer 





if __name__ == '__main__':
	main()