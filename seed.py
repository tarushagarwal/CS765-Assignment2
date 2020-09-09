from socket import *
from _thread import *
import json

ip = input("Enter IP: ")                                    #takes ip and port as input
port = int(input("Enter Port: "))

s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, port))
s.listen(20)                                                # maximum peers it can listen to
pl = []                                                     # list of peers connected to it
f = open('outputfile.txt', 'a+')                            # opens the outputfile

def on_new_client(clientsocket,addr):
    l_addr = clientsocket.recv(1024)                        #recieveing the listening address of the new peer
    l_addr = json.loads(l_addr.decode())
    msg = json.dumps(pl)                                    #sending the peer list
    clientsocket.send(msg.encode())
    pl.append(tuple(l_addr))                                #adding listening address of new peer in peer list
    l_addr = tuple(l_addr)
    print("new connection request from : " + l_addr[0] + ':' + str(l_addr[1]))              #printing the new connection request
    f.write("new connection request from : " + l_addr[0] + ':' + str(l_addr[1]) + '\n')
    f.flush()
    while l_addr in pl:                                 #if the node is dead it's l_addr is removed form the list therefore the while loop fails
        msg = clientsocket.recv(1024)
        msg = msg.decode()
        msg = msg.split('|')                            # for splitting simultaneously recieved messages
        msg.pop(-1)
        for item in msg:
            if item == '':
                continue
            m = item.split(":")
            print(item)                                 # printing dead node message
            f.write(item + '\n')
            f.flush()
            if (m[1], int(m[2])) in pl:
                pl.remove((m[1],int(m[2])))
    clientsocket.close()                                # Exits while loop only after the peer is dead hence we close the connection now

while(True):
    c, addr = s.accept()                                #accepts a new peer node and start a new thread for it
    start_new_thread(on_new_client,(c,addr))

s.close()