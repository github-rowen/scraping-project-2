import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# url = 'http://quotes.toscrape.com/'
url = 'http://quotes.toscrape.com/page/1/'

quotes = []
authors = []
tags = []

links = [url] #list for the collected links, with initial value as the start url
page_num = 0 #this will be use as the index for links list
pager_num = 1 #this will be use for updating link
checking = True #condition to control the while loop
while checking:
	r = requests.get(links[page_num])
	soup = BeautifulSoup(r.content, 'lxml')

	div = soup.find_all('div', class_='quote')
	# extract data
	for item in div:
		quote = item.find('span', class_='text').text.lstrip('“').rstrip('”')
		quotes.append(quote)
		# print(quote.lstrip('“').rstrip('”'))
		author = item.find('small', class_='author').text
		authors.append(author)
		tag = item.find('div', class_='tags').find_all('a', class_='tag')
		a_tag = [x.text for x in tag]
		tags.append(','.join(a_tag))

	print('saving... ' + links[page_num])

	page_num += 1
	pager_num += 1
	try:
		# check if next button is available
		pager = soup.find('li', class_='next').a
		if pager is not None:
			link_a = 'http://quotes.toscrape.com/page/{}/'.format(pager_num) #this will be the next link to scrape
			links.append(link_a)
		
	except:
		print('No more page')
		checking = False #update the value of checking variable to False so that the loop ends

df = pd.set_option('max_rows', None,'max_columns', None)
df = pd.options.display.width=None
df = pd.DataFrame({
	'quotes': quotes,
	'tags': tags,
	'authors': authors
	})
df.to_csv('quotes.csv', index=False)
# print(df)

# print(quotes)
# print(authors)
# print(tags)