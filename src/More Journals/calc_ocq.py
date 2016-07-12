from pymongo import MongoClient
from subprocess import call
import json
import ast
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
	Getting the list of required journals
"""
global_count = 0
categories = glob.glob("../../data/Categories/JournalLists/*.txt")
for category in categories:
	global_count += 1

	Name = category.split("/").pop()
	Name = re.sub('.txt','.csv',Name)
	journal_name_required = []
	journals = open(category,'r').readlines()
	for journal in journals:
		journal_name_required.append(text_to_id(journal.strip('\n')))

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
		print('Category :' + str(global_count) + ' Initializing: Article-'+str(count))
		try:
			record['publication'] = text_to_id(record['publication'])
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


	"""
		Calcualting Total and Self Citations for each author
		Storing authors of each journal
	"""
	count = 0
	for index in data:
		count += 1
		print('Category : ' + str(global_count) +' Scanning: Article-'+str(count))
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
	print('\n\nCategory : ' + str(global_count) +' OCQ values :\n\n')
	with open('../../output/More Journals/OCQ/'+Name,'w') as outfile:
		for journal in journal_name_required:
			Journal_quotient = 0.0
			try:
				for author in journal_author_list[journal]:
					if author_total_count[author]!= 0:
						Journal_quotient += author_self_count[author]/(1.0*author_total_count[author])
				Normalized_value = Journal_quotient/(len(journal_author_list[journal]))
				OCQ = 1 - Normalized_value
				print(str(journal) + '\t' + str(OCQ))
				outfile.write(str(journal) + ',' + str(OCQ) + '\n')
			except KeyError:
				outfile.write(str(journal) + ',0' + '\n')