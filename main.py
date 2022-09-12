from Scrapers.SeleniumOLX import SeleniumOLX
from Scrapers.ScrapyOLX import get_products


# Web Scraping with Selenium
SeleniumOLX = SeleniumOLX()
SeleniumOLX.search_text('carro')
#SeleniumOLX.search_in_url('https://rn.olx.com.br/rio-grande-do-norte/outras-cidades?q=petisco')
selenium_products = list(SeleniumOLX.get_products_in_page())


# Web Scraping with Scrapy
products = get_products()