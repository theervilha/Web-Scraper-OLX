from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class SeleniumOLX:
    product = (By.CSS_SELECTOR, ".sc-12rk7z2-2.gSNULD")

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())#, chrome_options=option)
    
    def search_text(self, search_text):
        url = f'https://rn.olx.com.br/?q={search_text}'
        self.driver.get(url)

    def search_in_url(self, url):
        self.driver.get(url)
    
    def get_products_in_page(self):
        self.elements = self.driver.find_elements(*self.product)
        #title = elements[0].find_element(By.CSS_SELECTOR, 'h2').text 
