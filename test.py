import csv
import random
# import math

# print(random.sample(['a','b','c','d','e','f','g'], random.randint(1,4)))
# with open('config.csv') as cfg:
# 	cfg = list(csv.reader(cfg, delimiter=':'))
# 	n = len((cfg))
# 	cfg = random.sample((cfg), (math.floor(n/2)+1))
# 	for entry in cfg:
# 		print(cfg)

with open('config.csv') as cfg:
		cfg = list(csv.reader(cfg, delimiter=':')) # delimiter : why?
		n = len((cfg))
		# cfg = random.sample((cfg), (math.floor(n/2)+1))
		for entry in cfg:
			print(entry)