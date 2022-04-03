from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

CURR_TYPE = "pants-fire"

page_start = 1
n_pages = 500

count = 0
df = pd.DataFrame(columns = ['Type', 'Name', 'Statement', 'Where', 'Date', 'Link'])

for page_number in range(page_start, n_pages + 1):
	page_name = "./data/politifact/{}/{}.html".format(CURR_TYPE, page_number)
	file = open(page_name, "r")

	soup = BeautifulSoup(file, 'html.parser')

	news_articles = soup.find_all("li", {"class": "o-listicle__item"})
	count += len(news_articles)

	for news_article in news_articles:
		texts = news_article.find_all(text=True)
		try:
			while True:
				texts.remove("\n")
		except ValueError:
			pass

		for i in range(len(texts)):
			texts[i] = texts[i].strip()

		print(texts)


		name = texts[0]
		try:
			date_and_where = texts[1].split(' on ')[1].split(" in ")
			date = date_and_where[0]
		except:
			date = ""
		try:
			where = date_and_where[1]
			where = re.sub(r'[^\w\s]', '', where)
			where = re.sub('(an |a |and |the |is |in )', "", where)
		except:
			where = ""
		statement = texts[2]


		for a in news_article.find_all('a', href=True):
			if "factchecks" in a['href']:
				link = "https://www.politifact.com" + a['href']

		df = df.append({'Type': CURR_TYPE, 'Name' : name, 'Statement' : statement, 'Where' : where, 'Date' : date, 'Link' : link}, 
                ignore_index = True)
print(count)
# df.to_csv("./csv/politifact_statements_{}.csv".format(CURR_TYPE))
				

