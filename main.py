from Scrapers.SeleniumOLX import SeleniumOLX
from Scrapers.ScrapyOLX import get_products

from datetime import datetime
import json

with open('url.txt', 'r') as f:
    url = f.read()

# # Web Scraping with Selenium
# SeleniumOLX = SeleniumOLX()
# products = SeleniumOLX.search_in_url(url=url)

# ## If you wanna get products until '09/17 18:00', just do:
# last_date_example = datetime(1900, 9, 17, 18, 0) # 1900 because we are desconsidering the year. The website don't give us the year of products
# products = SeleniumOLX.search_in_url(url=url, get_until_this_date=last_date_example)



# Web Scraping with Scrapy
products = get_products(url=url)

# If you wanna get products until '09/17 18:00', just do:
#last_date_example = datetime(1900, 9, 17, 18, 0) # 1900 because we are desconsidering the year. The website don't give us the year of products
#products = get_products(url=url, get_until_this_date=last_date_example)


def save_to_json(products):
    with open('extracted_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4, default=str)

save_to_json(products)