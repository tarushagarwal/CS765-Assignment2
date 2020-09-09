Make sure the outputfile is empty before runing a new instance of gossip network


Run seed.py with python3 to create a seed node where we would have to manually give IP and port as input after reading from config file.
The seed node maintains a peer list and opens the outputfile to write.
We used '|' as marker for ending of messages to handle simultaneously arriving messages.

Run peer.py to create an instance of peer node and input any ip on local network. It also outputs to same file as the seeds and other peers as submission format said only one output file.
Peer node maintain message list( hash of messages), peer list, seed list. And there are locks implemented on each message being checked and appended to message list as two same message arriving simultaneously were getting printed simultaneously.

Description - Start n seed node this will lead to formation of n socket but no connections yet. They all have empty peer list and opened the output file. When a peer node is created it accesses the config file and select (n/2) + 1 seed nodes randomly and send s them connection request and its listening address on which other nodes can send this node data. A seed node accpets the connection request and calls handler function for new peer node. In this function we  recieve the listening address and then send the peer list to the new peer and appends this peer into peer list. this thread of peer is now ready to recieve any message from the peer(peer only send dead report to seeds). The seed checks the dead node reported by peer and removes it from peer list and closes it connection and thread.
For peer it selects some random seeds and connects with them and send all of them it's listening address. It recieves peer list form all seeds combines them and select few peers to connect with and start and reciever thread with all of them. there are two other thread for generating gossip message and liveness check being run independently that send message to all peers using the broadcast function. Now this peer is always accepting connection of future peers trying to connect with it and opens a reciever thread for them. Now a reciever thread tqakes appropriate action for each message it recieves like calling forward function for gossip message, liveness reply for liveness request and setting livenesst test count to zero for  liveness reply. While liveness request thread calls report dead node independent of all reciever threads.

All print statements are followed with a write to file statement hence not highlighted in comments