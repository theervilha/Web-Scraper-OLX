from Scrapers.SeleniumOLX import SeleniumOLX


# Web Scraping with Selenium
SeleniumOLX = SeleniumOLX()
SeleniumOLX.search_text('carro')
#SeleniumOLX.search_in_url('https://rn.olx.com.br/rio-grande-do-norte/outras-cidades?q=petisco')
SeleniumOLX.get_products_in_page()