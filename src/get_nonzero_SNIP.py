import re

RIP = []
DCP = []
lst = []
with open("../output/SNIP2") as file :
	lines = file.readlines()
	for line in lines :
		lst.append(line.split(":"))

print lst

