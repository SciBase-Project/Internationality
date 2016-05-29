import pymongo
import ast
from subprocess import call
import json

call(["brew","services","start","mongodb"])
# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the  
db = client.acm_aminer
# list of journal names
journal_names = open('../output/ACM_Elsevier_journal_list_curated_v2','r').readlines()
#author_names = open("../data/")

with open('../data/IEEE_ACM_Journal_Map.json','r') as infile:
	jmap = json.load(infile)
journal_variations = jmap.keys()
Required = []

for key in jmap.keys():
	if jmap[key] not in Required:
		Required.append(jmap[key])


data = {}
self_cites = {}
total_cites = {}
paper_count = {}

#indexing based on the index of an article

article_list = list(db['publications'].find())

call(["brew","services","stop","mongodb"])

for article in article_list:
	data[article['index']] = dict(article)
	try:
		if article['publication'] in journal_variations :
			data[article['index']]['publication'] = jmap[article['publication']]
			article['publication'] = jmap[article['publication']]
			#data[article['publication']] = jmap[article['publication']]
	except KeyError:
		pass
	try:
		if article['publication'] not in total_cites:
			total_cites[article['publication']] = 0
			self_cites[article['publication']] = 0
			paper_count[article['publication']] = 1

		else:
			paper_count[article['publication']] += 1
			
	except KeyError:
		pass

article_list={}
for element in data:
	for reference in list(data[element]['references']):
		if reference == '':
			continue
		try:
			total_cites[data[element]['publication']] += 1
			jname = data[reference]['publication']
		except KeyError:
			continue
		total_cites[data[element]['publication']] += 1
		if jname == data[element]['publication']:
			self_cites[jname] += 1
			


with open('../output/NLIQ.txt','w') as outfile:
	for name in Required:
		try:
			selfc = self_cites[name.strip('\n').lower()]
			total = total_cites[name.strip('\n').lower()]
			if total!=0:
				quotient = (total - selfc)/(total*1.0)
			else:
				quotient = 0
			print(name.strip('\n')+'\t'+str(total)+'\t'+str(selfc)+'\t'+str(quotient) +'\t'+str(paper_count[name.strip('\n').lower()]))
			
			outfile.write(name.strip('\n')+ ',' +str(quotient) + ',' + str(paper_count[name.strip('\n').lower()])+'\n')
		
		except KeyError:
			pass
