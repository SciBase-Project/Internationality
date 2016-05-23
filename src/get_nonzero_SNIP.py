import re
import numpy

J = []
RIP = []
DCP = []
SNIP = []
lst = []

SNIP_values = {'Jname':[],'RIP':[],'DCP':[],'SNIP':[]}

with open("../output/SNIP2") as file :
	lines = file.readlines()
	for line in lines :
		lst.append(line.split(":"))

print lst

for item in lst :
	J.append(item[0][:len(item[0])-4])
	RIP.append(float(item[1][1:len(item[1])-4]))
	DCP.append(float(item[2][1:len(item[2])-1]))


'''
median_dcp = numpy.median(numpy.array(DCP))
print median_dcp

print RIP
print DCP
'''
count = 0
J_nonzero = []
for i in range(len(J)) :
	if RIP[i] != 0 and DCP[i] != 0 :
		print J[i]
		J_nonzero.append(J[i])
		count +=1

print count

with open("../output/nonzero_SNIP_journals.txt",'w') as file :
	for item in J_nonzero :
		file.write(item)
		file.write("\n")
'''
for i in range(0, len(J)) :
    rip = RIP[i]
    dcp = DCP[i]
    rdcp = 1.0 * dcp / median_dcp

    if rdcp == 0 : snip = 0
    else : snip = rip / rdcp

    print "[DEBUG] ", J[i], "RIP:", rip, "DCP:", dcp, "SNIP:", snip
    SNIP_values['Jname'].append(J[i])
    SNIP_values['RIP'].append(rip)
    SNIP_values['DCP'].append(dcp)
    SNIP_values['SNIP'].append(snip)
'''
