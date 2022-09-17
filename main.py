from Scrapers.SeleniumOLX import SeleniumOLX
from Scrapers.ScrapyOLX import get_products

from datetime import datetime

url = 'https://rn.olx.com.br/moveis?pe=300&ps=100&q=mesa'

# Web Scraping with Selenium
SeleniumOLX = SeleniumOLX()
products = SeleniumOLX.search_in_url(url=url)


# Web Scraping with Scrapy
products = get_products(url=url)

## If you wanna get products until '09/17 18:00', just do:
last_date_example = datetime(1900, 9, 17, 18, 0) # 1900 because we are desconsidering the year. The website don't give us the year of products
products = get_products(url=url, get_until_this_date=last_date_example)