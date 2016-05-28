from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

baseurl = 'http://www.scimagojr.com/'

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
			print(element.find('a').get_text() +' '+baseurl +element.find('a')['href'])
	links = page[2].findAll('a')
	for link in links:
		text = link.get_text()
		if text == 'Next >' :
			#print(baseurl + link['href'])
			get_next_link(baseurl + link['href'])

# Loading the first page of results for all queries as first URL
for url in url_list:
	get_next_link(baseurl + url)