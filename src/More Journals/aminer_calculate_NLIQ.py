import pymongo
import ast
from subprocess import call
import json
import unicodedata
import re
import glob

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('_',' ',text)
    return text


call(["brew","services","start","mongodb"])

# connecting to the database
client = pymongo.MongoClient("localhost", 27017)

# getting the table of the  
db = client.acm_aminer

# Initalizing the required structures
data = {}
self_cites = {}
total_cites = {}
paper_count = {}

# Accessing all article records in the database
article_list = list(db['publications'].find())

call(["brew","services","stop","mongodb"])

#indexing based on the index of an article
count = 0
for article in article_list:
	count += 1
	print("Initializing for article : " + str(count))
	data[article['index']] = dict(article)
	try:
		article['publication'] = text_to_id(article['publication'])
		data[article['index']]['publication'] = article['publication']
		if article['publication'] not in total_cites:
			total_cites[article['publication']] = 0
			self_cites[article['publication']] = 0
			paper_count[article['publication']] = 1

		else:
			paper_count[article['publication']] += 1
			
	except KeyError:
		pass

# Calcualting the values
count = 0
article_list={}
for element in data:
	count += 1
	print("Calculating for article : " + str(count))
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
			
# Finding the list of categories and files containing their journal lists
categories = glob.glob("../../data/Categories/JournalLists/*.txt")

# Storing NLIQ values for journals in each category separately
for category in categories:
	journals = open(category,'r').readlines()
	Name = category.split("/").pop()
	Name = re.sub('.txt','.csv',Name)
	print("Storing data for category : "+Name)
	with open('../../output/More Journals/NLIQ/'+Name,'w') as outfile:
		for journal in journals:
			journal = text_to_id(journal.strip('\n'))
			try:
				selfc = self_cites[journal]
				total = total_cites[journal]
				if total!=0:
					quotient = (total - selfc)/(total*1.0)
				else:
					quotient = 0
				print(journal+'\t'+str(total)+'\t'+str(selfc)+'\t'+str(quotient) +'\t'+str(paper_count[journal]))
				
				outfile.write(journal.strip('\n')+ ',' +str(quotient) + ',' + str(paper_count[journal])+'\n')
			
			except KeyError:
				outfile.write(journal.strip('\n')+ ',' +'0' + ',' + '0'+'\n')
