import unicodedata
import re
import ast
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

records = {}
file = open('../../data/ALL.csv','r')
source = file.readlines()
file.close()

for data in source:
	JName = text_to_id(data.strip('\n').split(',')[0])
	records[JName] = data.strip('\n').split(',')[5]

source = []
All_journals = records.keys()

categories = glob.glob("../../data/Categories/JournalLists/*.txt")

for category in categories:
	Name = category.split('/').pop()
	journals = open(category,'r').readlines()
	with open("../../output/More Journals/SNIP/"+Name,'w') as outfile:
		for journal in journals:
			journal = text_to_id(journal.strip('\n'))
			if journal in All_journals:
				outfile.write(journal+','+records[journal]+'\n')
			else:
				outfile.write(journal+',-\n')
