import scrapy
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess

from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "pt")

class MySpider(scrapy.Spider):
    name = "quotes"
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    product_l = ".sc-12rk7z2-1.huFwya"
    title_l = 'h2::text'
    img_l = 'img::attr(src)'
    price_l = '.sc-1kn4z61-1.dGMPPn span::text'
    date_l = '.sc-11h4wdr-0.javKJU::text'

    def __init__(self, url):
        self.url = url
    
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.get_products_in_page, headers=self.headers)

    def get_products_in_page(self, response):
        for self.element in response.css(self.product_l):
            yield {
                'product_link': self.element.css('::attr(href)').get(),
                'title': self.element.css(self.title_l).get(),
                'img': self.element.css(self.img_l).get(),
                'date': self.get_date(),
                'price': self.get_price(),
            }

    def get_price(self):
        price = self.element.css(self.price_l).get()[3:].replace('.', '')
        return float(price) if price != '' else price

    def get_date(self):
        self.date = self.element.css(self.date_l).get()
        self.clean_date()
        return self.date

    def clean_date(self):
        if "Hoje" in self.date:
            self.date = datetime.strptime(datetime.now().strftime('%d %b') + self.date[4:], '%d %b, %H:%M')
        elif "Ontem" in self.date:
            yesterday = datetime.now() - timedelta(1)
            self.date = datetime.strptime(yesterday.strftime('%d %b') + self.date[5:], '%d %b, %H:%M')
        else:
            self.date = datetime.strptime(self.date, '%d %b, %H:%M')



def get_products(url):
    items = []
    def collect_items(item, response, spider):
        items.append(item)

    crawler = Crawler(MySpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process = CrawlerProcess()
    process.crawl(crawler, url=url)
    process.start()

    return items