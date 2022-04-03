import numpy as np
from bs4 import BeautifulSoup
import requests
import time

page_start = 1
n_pages = 500
seconds_pause = 2

for page_number in range(page_start, n_pages + 1):
    try:
        # Get html from that page
        page_url = 'https://www.politifact.com/factchecks/list/?page={}&ruling=pants-fire'.format(page_number)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pf_html = soup.prettify()

        # Save raw html
        file = open('./data/politifact/pants-fire/{}.html'.format(page_number),'w') 
        file.write(pf_html)
        file.close()

        # Pause
        print('scraped page {}'.format(page_number))
        time.sleep(seconds_pause)
    except Exception as e:
        print('\nfailed to scrape page {}\n{}\n'.format(page_number, e))