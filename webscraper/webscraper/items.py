# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    category = scrapy.Field()
    stock = scrapy.Field() 
    rating = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    product_page_url = scrapy.Field()

