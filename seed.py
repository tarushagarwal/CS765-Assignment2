from socket import *
from _thread import *
import json

ip = input()
port = int(input())

s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, port))
s.listen(10)
pl = []

def on_new_client(clientsocket,addr):
    l_addr = clientsocket.recv(1024)
    l_addr = json.loads(l_addr.decode())
    msg = json.dumps(pl)
    clientsocket.send(msg.encode())
    pl.append(tuple(l_addr))
    l_addr = tuple(l_addr)
    print("new connection request from : " + l_addr[0] + ':' + str(l_addr[1]))
    while l_addr in pl:
        msg = clientsocket.recv(1024)
        msg = msg.decode()
        msg = msg.split('|')
        msg.pop(-1)
        for item in msg:
            if item == '':
                continue
            m = item.split(":")
            print(item) # printing dead node
            if (m[1], int(m[2])) in pl:
                pl.remove((m[1],int(m[2])))
    clientsocket.close()

while(True):
    c, addr = s.accept()
    start_new_thread(on_new_client,(c,addr))

s.close()