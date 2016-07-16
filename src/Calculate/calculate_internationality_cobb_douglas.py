'''
Cobb-Douglas Production Function
 Y = (x1)^a + (x2)^a + (x3)^a ...
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Jlist = []

# SNIP

list_of_cols = [0,1]
SNIP = pd.read_excel(io="../../output/IEEE_SNIP_IPP.xlsx", parse_cols=list_of_cols,header=0)

SNIP2 = SNIP.copy()
for item in SNIP["Journal"] :
		SNIP2.replace(to_replace = item,value = str(item.lower()),inplace = True) #chaning Journal name to lowercase

SNIP = SNIP2[pd.notnull(SNIP2["SNIP"])] #removing NaN values
SNIP.reset_index(inplace = True, drop = True)

for item in SNIP["Journal"] :
	Jlist.append(item)

print len(Jlist)


# ourSNIP
list_of_cols = [1,3]
oSNIP = pd.read_csv("../../output/SNIP_ours_ACM_IEEE.csv", usecols=list_of_cols,header=0)

Jlist_temp = []
for item in oSNIP["Journal"] :
	if item in Jlist :
		Jlist_temp.append(item)

Jlist = Jlist_temp
print len(Jlist)

# NLIQimpoer
list_of_cols = [0,1]
NLIQ = pd.read_csv("../../output/NLIQ_ACM_IEEE.csv", usecols=list_of_cols,header=0)

NLIQ = NLIQ[NLIQ["NLIQ"] != 0]
NLIQ.reset_index(inplace = True, drop = True)

Jlist_temp = []
for item in NLIQ["Journal"] :
	if item in Jlist :
		Jlist_temp.append(item)

Jlist = Jlist_temp
print len(Jlist)

# IC
list_of_cols = [0,15]
IC = pd.read_csv("../../output/IC.csv", usecols=list_of_cols,header=0)

IC2 = IC.copy()
for item in IC["Journal"] :
		IC2.replace(to_replace = item,value = str(item.lower()),inplace = True) #chaning Journal name to lowercase

IC = IC2
IC = IC[IC["2010"] != 0]
IC.reset_index(inplace = True, drop = True)


Jlist_temp = []
for item in IC["Journal"] :
	if item.lower() in Jlist :
		Jlist_temp.append(item)

Jlist = Jlist_temp
print len(Jlist)

# OCQ
list_of_cols = [0,1]
OCQ = pd.read_csv("../../output/OCQ.csv", usecols=list_of_cols,header=0)

OCQ.reset_index(inplace = True, drop = True)


Jlist_temp = []
for item in OCQ["Journal"] :
	if item.lower() in Jlist :
		Jlist_temp.append(item)

Jlist = Jlist_temp
print len(Jlist)

# Cobb-Douglas Part
Jvalues = {} #[SNIP,oSNIP,NLIQ,IC]
Y = {}

Slist = []
oSlist = []
Nlist = []
Ilist = []
Olist = []

for J in Jlist :

	S = SNIP[SNIP["Journal"] == J]["SNIP"].values[0]
	Slist.append(S)
	oS = oSNIP[oSNIP["Journal"] == J]["SNIP"].values[0]
	oSlist.append(oS)
	N = NLIQ[NLIQ["Journal"] == J]["NLIQ"].values[0]
	Nlist.append(N)
	I = IC[IC["Journal"] == J]["2010"].values[0]
	Ilist.append(I)
	O = OCQ[OCQ["Journal"] == J]["OCQ"].values[0]
	Olist.append(O)
	
Smax = max(Slist)
oSmax = max(oSlist)
Nmax = max(Nlist)
Imax = max(Ilist)
Omax = max(Olist)

for J in Jlist :

	S = SNIP[SNIP["Journal"] == J]["SNIP"].values[0]
	oS = oSNIP[oSNIP["Journal"] == J]["SNIP"].values[0]
	N = NLIQ[NLIQ["Journal"] == J]["NLIQ"].values[0]
	I = IC[IC["Journal"] == J]["2010"].values[0]
	O = OCQ[OCQ["Journal"] == J]["OCQ"].value[0]
	
	Jvalues[J] =  [S/Smax,oS/oSmax,N/Nmax,I/Imax,O/Omax]#,oSNIP.get_value(J,"SNIP")]

	for i in range(0,4) :
		Y[J] = Jvalues[J][i] ** 0.1

count = len(Y)
for key, value in sorted(Y.iteritems(), key=lambda (k,v): (v,k)):
    print "%d. %s: %s" % (count,key,value)
    count -= 1





