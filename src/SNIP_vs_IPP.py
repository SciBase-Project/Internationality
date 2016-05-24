import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


list_of_cols = [0,1,2]
SNIP = pd.read_excel(io="../data/IEEE_SNIP_IPP.xlsx", parse_cols=list_of_cols,header=0)
list_of_cols = [1,3]
oSNIP = pd.read_csv("../output/SNIP_IEEE.csv", usecols=list_of_cols,header=0)
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
SNIP3 = pd.DataFrame()

for item in SNIP["Journal"] :
	lst1.append(str(item.lower()))

for item in oSNIP["Journal"] :
	lst2.append(str(item))

for item in lst1 :
	if item in lst2 :
		lst.append(item)


for item in SNIP["Journal"] :
	SNIP2.replace(to_replace=item,value= str(item.lower()),inplace =True)


SNIP2.reset_index(inplace=True)
#print SNIP3

oSNIP_v_SNIP = {}

count = 0

for item in SNIP2.itertuples() :
	if item[2] in lst :
		oSNIP_v_SNIP[item[2]] = []
		oSNIP_v_SNIP[item[2]].append(item[3])
		#print item
		#count += 1


count = 0

for item in oSNIP.itertuples() :
	if item[1] in lst :
		oSNIP_v_SNIP[item[1]].append(item[2])
		#print item
		#count += 1

print oSNIP_v_SNIP


#jnames = []
#for journal in jnames:
#	selected_journal.append( SNIP[SNIP["Source Title"]==journal] )

#selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
#selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
#selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)
x = []
y = []

for item in oSNIP_v_SNIP :
	x.append(oSNIP_v_SNIP[item][0])
	y.append(oSNIP_v_SNIP[item][1])

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

#plt.scatter(x,y,color="red")
#plt.scatter(SNIP["SNIP"],SNIP["IPP"],color="red")
#plt.legend()
#plt.show()





