from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "pt")

class SeleniumOLX:
    product_l = (By.CSS_SELECTOR, ".sc-12rk7z2-1.huFwya")
    title_l = (By.CSS_SELECTOR, 'h2')
    img_l = (By.CSS_SELECTOR, 'img')
    price_l = (By.CSS_SELECTOR, '.sc-1kn4z61-1.dGMPPn span')
    date_l = (By.CSS_SELECTOR, '.sc-11h4wdr-0.javKJU')

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def search_in_url(self, url, **kwargs):
        self.get_until_this_date = kwargs.get('get_until_this_date')

        self.generate_next_five_pages(url)
        self.products = []
        for url in self.urls:
            self.driver.get(url)
            try:
                self.get_products_in_page()
            except Exception:
                return self.products

        return self.products
        
    def generate_next_five_pages(self, url, num_pages=5):
        start_i = url.find('?')+1
        if "o=" not in url and start_i != '-1':
            self.urls = [f'{url[:start_i]}o={i}&{url[start_i:]}' for i in range(1, num_pages+1)]
        elif "o=" not in url and start_i == '-1':
            self.urls = [f'{url}?o={i}' for i in range(1, num_pages+1)]
        elif "o=" in url:
            self.urls = [re.sub('o=.*?&', f'o={i}&' , url, flags=re.DOTALL) for i in range(1, num_pages+1)]
    
    def get_products_in_page(self):
        for self.element in self.driver.find_elements(*self.product_l):
            product_date = self.get_product_date()

            # If passed a limit date to get products, verify.
            if self.get_until_this_date:
                if product_date <= self.get_until_this_date:
                    raise Exception('All products were taken by the deadline.')

            self.products.extend([{
                'product_link': self.element.get_attribute('href'),
                'title': self.element.find_element(*self.title_l).text,
                'img': self.element.find_element(*self.img_l).get_attribute('src'),
                'price': self.get_product_price(),
                'date': product_date,
            }])

    def get_product_date(self):
        self.date = self.element.find_element(*self.date_l).text
        self.clean_date()
        return self.date
    
    def get_product_price(self):
        price = self.element.find_element(*self.price_l).text[3:].replace('.', '')
        return float(price) if price != '' else price

    def clean_date(self):
        if "Hoje" in self.date:
            self.date = datetime.strptime(datetime.now().strftime('%d %b') + self.date[4:], '%d %b, %H:%M')
        elif "Ontem" in self.date:
            yesterday = datetime.now() - timedelta(1)
            self.date = datetime.strptime(yesterday.strftime('%d %b') + self.date[5:], '%d %b, %H:%M')
        else:
            self.date = datetime.strptime(self.date, '%d %b, %H:%M')

