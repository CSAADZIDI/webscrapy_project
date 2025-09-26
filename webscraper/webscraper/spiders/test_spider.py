import scrapy
from webscraper.items import BookItem

class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        item = BookItem()
        item['title'] = "Hello"
        yield item
