import scrapy
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess

class MySpider(scrapy.Spider):
    name = "quotes"
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    
    def start_requests(self):
        urls = [
            'https://rn.olx.com.br/?q=carro'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for product in response.css('.sc-12rk7z2-2.gSNULD'):
            yield {
                'title': product.css('h2::text').get()
            }


def get_products():
    items = []
    def collect_items(item, response, spider):
        items.append(item)

    crawler = Crawler(MySpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process = CrawlerProcess()
    process.crawl(crawler)
    process.start()

    return items