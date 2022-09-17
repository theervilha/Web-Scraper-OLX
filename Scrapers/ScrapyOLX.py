import scrapy
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.exceptions import CloseSpider

from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "pt")

import time
import re

class MySpider(scrapy.Spider):
    name = "products"
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    product_l = ".sc-12rk7z2-1.huFwya"
    title_l = 'h2::text'
    img_l = 'img::attr(src)'
    price_l = '.sc-1kn4z61-1.dGMPPn span::text'
    date_l = '.sc-11h4wdr-0.javKJU::text'

    def __init__(self, urls, **kwargs):
        self.urls = urls
        self.get_until_this_date = kwargs.get('get_until_this_date')
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.get_products_in_page, headers=self.headers)

    def get_products_in_page(self, response): 
        for self.element in self.get_products(response):
            product_date = self.get_product_date()

            # If passed a limit date to get products, verify.
            if self.get_until_this_date:
                if product_date <= self.get_until_this_date:
                    raise CloseSpider('All products were taken by the deadline.')

            yield {
                'product_link': self.element.css('::attr(href)').get(),
                'title': self.element.css(self.title_l).get(),
                'img': self.element.css(self.img_l).get(),
                'date': product_date,
                'price': self.get_product_price(),
            }
    
    def get_products(self, response):
        return response.css(self.product_l)

    def get_product_date(self):
        self.date = self.element.css(self.date_l).get()
        self.clean_date()
        return self.date

    def get_product_price(self):
        price = self.element.css(self.price_l).get()[3:].replace('.', '')
        return float(price) if price != '' else price

    def clean_date(self):
        if "Hoje" in self.date:
            self.date = datetime.strptime(datetime.now().strftime('%d %b') + self.date[4:], '%d %b, %H:%M')
        elif "Ontem" in self.date:
            yesterday = datetime.now() - timedelta(1)
            self.date = datetime.strptime(yesterday.strftime('%d %b') + self.date[5:], '%d %b, %H:%M')
        else:
            self.date = datetime.strptime(self.date, '%d %b, %H:%M')



def generate_next_five_pages_from_url(url, num_pages=5):
    start_i = url.find('?')+1
    if "o=" not in url and start_i != '-1':
        return [f'{url[:start_i]}o={i}&{url[start_i:]}' for i in range(1, num_pages+1 )]
    elif "o=" not in url and start_i == '-1':
        return [f'{url}?o={i}' for i in range(1, num_pages+1 )]
    elif "o=" in url:
        return [re.sub('o=.*?&', f'o={i}&' , url, flags=re.DOTALL) for i in range(1, num_pages+1 )]

def get_products(url, **kwargs):
    urls = generate_next_five_pages_from_url(url)

    items = []
    def collect_items(item, response, spider):
        items.append(item)

    crawler = Crawler(MySpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process = CrawlerProcess()
    process.crawl(crawler, urls=urls,  **kwargs)
    process.start()

    return items