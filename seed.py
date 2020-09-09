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
    try:
        l_addr = clientsocket.recv(1024)
        l_addr = json.loads(l_addr.decode())
        # print(type(l_addr))
        # print(l_addr)
        # l_addr = l_addr.decode()
        msg = json.dumps(pl)#something containing pl
        clientsocket.send(msg.encode())
        pl.append(tuple(l_addr))
        l_addr = tuple(l_addr)
        print("new connection request from : " + l_addr[0] + ':' + str(l_addr[1]))
        while l_addr in pl:
            msg = clientsocket.recv(1024)#more than size of dead message format
            msg = msg.decode()
            print("::::::::: ", end=' ')
            msg = msg.split('|')
            print(msg)
            msg.pop(-1)
            for item in msg:
                if item == '':
                    continue
                m = item.split(":")
                # assert(m[0] == "Dead Node")
                print(item)
                if (m[1], int(m[2])) in pl:
                    pl.remove((m[1],int(m[2])))
        clientsocket.close()
    except err:
        print(err)
        print("connection closed with: " + l_addr[0] + ':' + str(l_addr[1]))
        pl.remove((l_addr[0],int(l_addr[1])))

while(True):
    # print("Send Client")
    c, addr = s.accept()
    # pl.append(addr)
    start_new_thread(on_new_client,(c,addr))

s.close()

#try-catch, output file, number of listeners, print statement