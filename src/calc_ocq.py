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
	Making the records accessible by their index attribute
	All journal varitations have same publication attribute
"""
count = 0
for record in records:
	count += 1
	print('Initializing: Article-'+str(count))
	try:
		# Unifying variations in the name of a journal
		if record['publication'] in journal_variations:
			record['publication'] = journal_name_map[record['publication']]
	except KeyError:
		pass
	# Indexing based on the article index
	data[record['index']] = record
	# Removing default author names
	data[record['index']]['authors'] = []
	for author in record['authors']:
		if author = '':
			continue
		author = text_to_id(author)
		# Storing the cleaned author names
		data[record['index']]['authors'].append(author)

		if author not in author_paper_count:
			author_total_count[author] = 0
			author_self_count[author] = 0
			author_paper_count[author] = 1
		else:
			author_paper_count[author] += 1
		if record['publication'] in journal_name_required:
			if author not in journal_author_list[record['publication']]:
				journal_author_list[record['publication']].append(author)
records = []



"""
	Calcualting Total and Self Citations for each author
	Storing authors of each journal
"""
count = 0
for index in data:
	print('Scanning: Article-'+str(count))
	for reference in data[index]['references']:
		if reference == '':
			continue
		# Increasing stats for each author in citing article
		for author in data[index]['authors']:
			if author = '':
				continue
			author_total_count[author] += 1

			if author in data[reference]['authors']:
				author_self_count[author] += 1



"""
	Calculating OCQ for all interested journals
	Printing the result and storing it in a file
"""
print('\n\nOCQ values :\n\n')
with open('','w') as outfile:
	for journal in journal_name_required:
		Journal_quotient = 0.0
		# Calculatin the cumulative citation quotient of a journal from all its authors
		for author in journal_author_list[journal]:
			# Ensuring no divide error occurs
			if author_total_count[author]!= 0:
				Journal_quotient += author_self_count[author]/(1.0*author_total_count[author])
		# Averaging the cumulative Quotient value
		Normalized_value = Journal_quotient/(len(journal_author_list[journal]))
		OCQ = 1 - Normalized_value
		print(str(journal) + '\t' + str(OCQ))
		outfile.write(str(journal) + '\t' + str(OCQ) + '\n')