import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


list_of_cols = [0,1,2]
SNIP = pd.read_excel(io="../output/IEEE_SNIP_IPP.xlsx", parse_cols=list_of_cols,header=0)
#list_of_cols = [1,3]
#oSNIP = pd.read_csv("../output/SNIP_IEEE.csv", usecols=list_of_cols,header=0)
#list_of_cols = [0,1]
#oSNIP = pd.read_csv("../output/NLIQ copy.csv", usecols=list_of_cols,header=0)

list_of_cols = [0,15]
oSNIP = pd.read_csv("../output/IC.csv", usecols=list_of_cols,header=0)

'''
list_of_cols = [0,1,2]
SNIP = pd.read_excel(io="../data/ACM_SNIP_IPP.xlsx", parse_cols=list_of_cols,header=0)
list_of_cols = [1,3]
oSNIP = pd.read_csv("../output/SNIP_ACM.csv", usecols=list_of_cols,header=0)
'''
#print oSNIP
#jname = "AAC: Augmentative and Alternative Communication"
#selected_journal = SNIP[SNIP["Source Title"]==jname] #make sure it exists!
#selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
#selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
#selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)

#selected_journal.plot()
#plt.legend()
#plt.show()

lst = []
lst1 = []
lst2 = []
SNIP2 = SNIP.copy()

for item in SNIP["Journal"] :
	lst1.append(str(item.lower()))

for item in oSNIP["Journal"] :
	lst2.append(str(item.lower()))


for item in lst1 :
	if item in lst2 :
		lst.append(item)


for item in SNIP["Journal"] :
	SNIP2.replace(to_replace=item,value= str(item.lower()),inplace =True)


SNIP2.reset_index(inplace=True)
print SNIP2

oSNIP_v_SNIP = {}

count = 0

for item in SNIP2.itertuples() :
	if item[2] in lst :
		oSNIP_v_SNIP[item[2]] = []
		oSNIP_v_SNIP[item[2]].append(item[3])
		oSNIP_v_SNIP[item[2]].append(item[4])
		#print item
		#count += 1


count = 0
'''
for item in oSNIP.itertuples() :
	if item[1] in lst :
		oSNIP_v_SNIP[item[1]].append(item[2])
		#print item
		#count += 1
'''

for item in oSNIP.itertuples() :
	#print item
	if str(item[1]).lower() in lst :
		#print item[1].lower()
		oSNIP_v_SNIP[str(item[1]).lower()].append(item[2])
		#print item
		#count += 1


#jnames = []
#for journal in jnames:
#	selected_journal.append( SNIP[SNIP["Source Title"]==journal] )

#selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
#selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
#selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)
x = []
y = []
z = []

for item in oSNIP_v_SNIP :
	x.append(oSNIP_v_SNIP[item][0])
	z.append(oSNIP_v_SNIP[item][1])
	#y.append(0.8641 + 1.741*oSNIP_v_SNIP[item][2])
	y.append(oSNIP_v_SNIP[item][2])

print oSNIP_v_SNIP
print len(x)

'''
with open("../output/SNIP_original.csv","w") as file:
	for item in oSNIP_v_SNIP :
		file.write(item)
		file.write(",")
		file.write(str(oSNIP_v_SNIP[item][0]))
		file.write("\n")


with open("../output/SNIP_ours.csv","w") as file:
	for item in oSNIP_v_SNIP :
		file.write(item)
		file.write(",")
		file.write(str(oSNIP_v_SNIP[item][1]))
		file.write("\n")
'''

#plt.scatter(y,z,color="red")
plt.scatter(x,y,color="blue",label='')
#plt.scatter(SNIP["SNIP"],SNIP["IPP"],color="red")
plt.legend()
plt.show()






