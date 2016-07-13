from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# Function to generate the required parseable object
def get_soup(aurl):
	html = urlopen(aurl)
	asoup = BeautifulSoup(html,'html.parser')
	return asoup

def get_IC(aurl):
	print(aurl)
	soup = get_soup(aurl)
	stats = soup.find_all('div',{'class':'cellcontent'})
	IC = stats[5].find('table')
	header = IC.find_all('th')[1].get_text()
	if header!= 'International Collaboration':
		print('Not IC!')
	else:
		records = IC.find_all('tr')
		for record in records[1::]:
			fields = record.find_all('td')
			print(fields[0].get_text() + '\t' +fields[1].get_text())


baseurl = "http://www.scimagojr.com/"

url = 'http://www.scimagojr.com/journalrank.php?category=1302&area=1300&year=2010'
soup = get_soup(url)

Journals = soup.find_all('td',{'class':'tit'})
for Journal in Journals:
	print(Journal.get_text() + '\t' + Journal.find('a')['href'])
	get_IC(baseurl + Journal.find('a')['href'])

