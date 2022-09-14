from Scrapers.SeleniumOLX import SeleniumOLX
from Scrapers.ScrapyOLX import get_products


# Web Scraping with Selenium
SeleniumOLX = SeleniumOLX()
products = SeleniumOLX.search_in_url("https://rn.olx.com.br/moveis?pe=300&ps=100&q=mesa")


# Web Scraping with Scrapy
# products = get_products(url='https://rn.olx.com.br/moveis?pe=300&ps=100&q=mesa')


print(products[:3])