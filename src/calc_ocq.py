from pymongo import MongoClient
from subprocess import call
import json
import ast
import unicodedata
import re


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



"""
	Getting all the required records from the database
"""

# Starting MongoDB
call(["brew","services","start","mongodb"])

# Connecting to the local database network
client = MongoClient('localhost',27017)

# Getting the required database
db = client['acm_aminer']

# Getting the collection
collection = db['publications']

# Getting all the records in the collection
records = list( collection.find() )

# Ending MongoDB service
call(["brew","services","stop","mongodb"])



"""
	Initializing the required data structures
"""
author_self_count = {}
author_total_count = {}
author_paper_count = {}
journal_author_list = {}
data = {}



"""
	Getting the required journal names with their variations
"""

# Connecting the file storing the jorunal name variations with their respective unique name
with open('../data/IEEE_ACM_Journal_Map.json','r') as infile:
	journal_name_map = json.load(infile)

# Creating a list containing all journals name variations
journal_variations = journal_name_map.keys()

#Creating a list of all required journal names (the final ones)
journal_name_required = []
for journal in journal_variations:
	if journal_name_map[journal] not in journal_name_required:
		journal_name_required.append(journal_name_map[journal])
		journal_author_list[journal_name_map[journal]] = []



"""
	Making the records accessible by their index attribute
	All journal varitations have same publication attribute
"""
count = 0
for record in records:
	count += 1
	print('Initializing: Article-'+str(count))
	try:
		# Unifying variations in journal's name
		if record['publication'] in journal_variations:
			record['publication'] = journal_name_map[record['publication']]
	except KeyError:
		pass

	data[record['index']] = record
	temp = []
	# Cleaning the author names, allowing index using them
	try:
			for author in record['authors']:
				if author == '':
					continue
				author = text_to_id(author)
				temp.append(author)
				if author not in author_paper_count:
					author_total_count[author] = 0
					author_self_count[author] = 0
					author_paper_count[author] = 1
				else:
					author_paper_count[author] += 1
				if record['publication'] in journal_name_required:
					if author not in journal_author_list[record['publication']]:
						journal_author_list[record['publication']].append(author)
	except KeyError:
		pass
	data[record['index']]['authors'] = temp
records = []



"""
	Calcualting Total and Self Citations for each author
	Storing authors of each journal
"""
count = 0
for index in data:
	count += 1
	print('Scanning: Article-'+str(count))
	# Visiting all citations by a paper
	for reference in data[index]['references']:
		if reference == '':
			continue
		# Increasing stats for all the authors in the paper
		for author in data[index]['authors']:
			if author == '':
				continue
			author_total_count[author] += 1
			try:
				# If author exists in the cited paper also
				if author in data[reference]['authors']:
					author_self_count[author] += 1
			except KeyError:
				pass



"""
	Calculating OCQ for all interested journals
	Printing the result and storing it in a file
"""
print('\n\nOCQ values :\n\n')
with open('../output/OCQ.csv','w') as outfile:
	for journal in journal_name_required:
		Journal_quotient = 0.0
		for author in journal_author_list[journal]:
			if author_total_count[author]!= 0:
				Journal_quotient += author_self_count[author]/(1.0*author_total_count[author])
		Normalized_value = Journal_quotient/(len(journal_author_list[journal]))
		OCQ = 1 - Normalized_value
		print(str(journal) + '\t' + str(OCQ))
		outfile.write(str(journal) + ',' + str(OCQ) + '\n')