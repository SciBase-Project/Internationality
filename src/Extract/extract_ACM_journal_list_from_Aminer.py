import re
from collections import defaultdict

J_ALL = []
with open('../../output/ACM_AMINER_JOURNAL_LIST_ALL.txt') as file :
	lines = file.readlines() 
	#print lines
	for line in lines :
		J_ALL.append(line.strip('\n').lower())

#print J_ALL

J_ACM = []
with open('../../output/IEEE_journal_list.txt') as file :
	lines = file.readlines()
	for line in lines :
		J_ACM.append(line.strip('\n').lower())
#print J_ACM
'''
J_short = []
with open('../../output/ACM_ONLY_journal_list_shortforms.txt') as file :
	lines = file.readlines()
	for line in lines :
		J_short.append('('+line.strip().lower()+')')
print J_short

J_ACM.append(J_short)
'''
J_matched = []
J_dict = defaultdict(list)
print "__________________________________________________________________"

print "__________________________________________________________________"

for J in J_ACM :
	for JA in J_ALL :
		try :
			if re.search(J,JA) :
				#print JA
				if JA not in J_matched :
					J_matched.append(JA)
					#print JA
					if JA not in J_dict[J] :
						J_dict[J].append(JA)
		except TypeError :
			continue

print len(J_matched)

for item in J_dict :
	print item

print J_dict