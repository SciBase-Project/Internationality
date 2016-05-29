from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

baseurl = 'http://www.scimagojr.com/'

file = open('../../output/IC.csv','w')

# various keyword journals being searched for
url_list = ['journalsearch.php?q=IEEE&tip=jou&exact=no&page=0','journalsearch.php?q=ACM&tip=jou&exact=no&page=0']

# Loading the list of journals for which data has to be scraped
with open('../../data/IEEE_ACM_Journal_Map.json','r') as infile:
	jmap = json.load(infile)
journal_variations = jmap.keys()
Required = []
# Getting only the journal names
for key in jmap.keys():
	if jmap[key] not in Required:
		Required.append(jmap[key])

# Function to return a BeautifulSoup object of the requested page url
def get_soup(aurl):
	html = urlopen(aurl)
	asoup = BeautifulSoup(html.read(),'html.parser')
	return asoup

# Travels through all the pages of search results
def get_next_link(aurl):
	soup = get_soup(aurl)
	page = soup.find('div',{'id':'derecha_contenido'}).find_all('p')
	page.pop()
	for element in page[3::]:
		if element.find('a').get_text().lower() in Required:
			file.write('\n'+element.find('a').get_text())

			# Finding the required tags from javascript codes using regex
			siblings =get_soup(baseurl +element.find('a')['href']).find("div",{"id":"flashcontent7"}).next_sibling.next_sibling
			narrowed = re.findall(r'<graphs>.*</graphs>',str(siblings),re.DOTALL)
			final = narrowed[0].split('xid')
			for year in final[1::]:
				if str(year.split('"')[2].split('<')[0].split('>')[1] ) == '':
					file.write(',0.0')
					#print(',0.0',end='')
				else:
					file.write(','+str(year.split('"')[2].split('<')[0].split('>')[1] ))
				#print(year.split('"')[1] +' '+str(year.split('"')[2].split('<')[0].split('>')[1] ))

	links = page[2].findAll('a')
	for link in links:
		text = link.get_text()
		if text == 'Next >' :
			get_next_link(baseurl + link['href'])

file.write('Journal Name')
for i in range(1996,2015):
	file.write(','+str(i))
# Loading the first page of results for all queries as first URL
for url in url_list:
	get_next_link(baseurl + url)