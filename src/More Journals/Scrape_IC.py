from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

count = 0

# Function to generate the required parseable object
def get_soup(aurl):
	html = urlopen(aurl)
	asoup = BeautifulSoup(html,'html.parser')
	return asoup

def get_IC(aurl):
	# print(aurl)
	global file
	soup = get_soup(aurl)
	values = {}
	for i in range(1999,2016):
		values[str(i)] = str(0.00)
	stats = soup.find_all('div',{'class':'cellcontent'})
	IC = stats[5].find('table')
	header = IC.find_all('th')[1].get_text()
	if header!= 'International Collaboration':
		print('Not IC!')
	else:
		records = IC.find_all('tr')
		for record in records[1::]:
			fields = record.find_all('td')
			values[fields[0].get_text()] = fields[1].get_text()
			# print(fields[0].get_text() + '\t' +fields[1].get_text())
	for value in values:
		file.write(','+ str(values[value]))
		# print(','+values[value],end='')
		# print(value + ' ' + values[value])


def get_link(aurl):
	global count
	global file
	soup = get_soup(aurl)
	links = soup.find('div',{'class':'pagination_buttons'}).find_all('a')
	Journals = soup.find_all('td',{'class':'tit'})
	for Journal in Journals:
		count += 1
		# print(Journal.get_text(),end='')
		file.write('\n' + str(Journal.get_text()))
		get_IC(baseurl + Journal.find('a')['href'])
	if links[1]['class'][0] != 'disabled':
		print(links[1]['href'])
		new_url = baseurl + links[1]['href']
		get_link(new_url)

file = open('../../output/More Journals/IC.csv','w')

file.write('Jounral Name')
for i in range(1999,2016):
	file.write(',' + str(i))

baseurl = "http://www.scimagojr.com/"
url = 'http://www.scimagojr.com/journalrank.php?area=1700&year=2010&type=j&category=1705'
get_link(url)
file.close()




