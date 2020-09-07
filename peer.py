import csv
import math
import socket

# def connect_seeds():
# 	with open('config.csv') as cfg:
# 		cfg = csv.reader(cfg, delimiter=':')
# 		n = len(cfg)
# 		cfg = random.sample(cfg, (floor(n/2)+1))
# 		for entry in cfg:
# 			pass


def main():
	# connect_seeds()
	seeds = []
	with open('config.csv') as cfg:
		cfg = list(csv.reader(cfg, delimiter=':'))
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
	pl = {}
	for s in seeds:
		pl = pl.union(s.recv(1024))

	#connecting to peers 
	# print(pl)
	pl = list(pl)
	pl = random.sample(pl, random.randint(1,4))
	peers = []
	for peer in pl:
		try: 
			    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err: 
		    print("error creating socket ",err )
		peer.split(':')
		p.connect((peer))



if __name__ == '__main__':
	main()