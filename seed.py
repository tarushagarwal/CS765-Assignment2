from socket import *
from _thread import *
import json

ip = input()
port = int(input())

s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, port))
s.listen(10)
pl = []
# output_file = 

def on_new_client(clientsocket,addr):
    l_addr = clientsocket.recv(1024)
    msg = json.dumps(pl)#something containing pl
    clientsocket.send(msg.encode())
    pl.append(l_addr)
    while addr in pl:
        msg = clientsocket.recv(1024)#more than size of dead message format
        msg = msg.decode()
        m = msg.split(":")
        assert(m[0] == "Dead Node")
        if (m[1], int(m[2])) in pl:
            pl.remove((m[1],int(m[2])))
    clientsocket.close()


while(True):
    print("Send Client")
    c, addr = s.accept()
    # pl.append(addr)
    start_new_thread(on_new_client,(c,addr))

s.close()