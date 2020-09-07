from socket import *
import thread

ip = input()
port = int(input())

s = socket(AF_INET, SOCK_STREAM)
s.bind(ip, port)
s.listen(10)
pl = []


def on_new_client(clientsocket,addr):
    msg = #something containing pl
    clientsocket.send(msg)
    while addr in pl:
        msg = clientsocket.recv()#size of dead message)
        #do some checks and if msg == someWeirdSignal: break:
    #     print addr, ' >> ', msg
    #     msg = raw_input('SERVER >> ')
    #     #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    #     clientsocket.send(msg)
    # clientsocket.close()
        m = msg.split(":")
        assert(m[0] == "Dead Node")
        if (m[1], m[2]) in pl:
            pl.remove((m[1], m[2]))
    clientsocket.close()


while(True):
    c, addr = s.accept()
    pl.push_back((addr))
    thread.start_new_thread(on_new_client,(c,addr))