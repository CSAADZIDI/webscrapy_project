import scrapy
import re
from webscraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # iterate books on the page and follow each product link
        for book in response.css("article.product_pod"):
            rel_url = book.css("h3 a::attr(href)").get()
            yield response.follow(rel_url, callback=self.parse_book)

        # follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        item = BookItem()

        # Title
        item['title'] = response.css('div.product_main h1::text').get(default='').strip()

        # Main price (p.price_color: "£51.77")
        price_text = response.css('p.price_color::text').get()
        if price_text:
            m = re.search(r'£\s*([0-9]+(?:\.[0-9]+)?)', price_text)
            item['price'] = float(m.group(1)) if m else None
        else:
            item['price'] = None

        # Availability: there is extra whitespace/newlines inside the tag, so join text nodes
        avail_parts = response.css('p.instock.availability::text').getall()
        avail_text = ' '.join([p.strip() for p in avail_parts]).strip()
        item['availability'] = avail_text
        m = re.search(r'\((\d+)\s+available\)', avail_text)
        item['stock'] = int(m.group(1)) if m else (1 if 'In stock' in avail_text else 0)

        # Rating -> class is like "star-rating Three"
        rating_class = response.css('p.star-rating::attr(class)').get(default='')
        # rating_word should be the second class (One/Two/Three/Four/Five)
        rating_word = rating_class.replace('star-rating', '').strip().split()[0] if rating_class else ''
        RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        item['rating'] = RATING_MAP.get(rating_word, None)

        # Category (breadcrumb): typical location ul.breadcrumb li:nth-child(3) a
        item['category'] = response.css('ul.breadcrumb li:nth-child(3) a::text').get(default='').strip()

        # Description: the paragraph immediately after the #product_description header
        item['description'] = response.css('#product_description + p::text').get(default='').strip()

        # Image: site uses a relative path like ../../media/cache/..., use urljoin
        img_rel = response.css('#product_gallery img::attr(src)').get()
        item['image_url'] = response.urljoin(img_rel) if img_rel else None

        # Product information table (UPC, prices, tax, number of reviews, etc.)
        for row in response.css('table.table.table-striped tr'):
            heading = row.css('th::text').get(default='').strip()
            value = row.css('td::text').get(default='').strip()

            if heading == 'UPC':
                item['upc'] = value
            elif heading == 'Product Type':
                item['product_type'] = value
            elif heading.startswith('Price (excl'):
                item['price_excl_tax'] = float(value.replace('£', '').strip()) if value else None
            elif heading.startswith('Price (incl'):
                item['price_incl_tax'] = float(value.replace('£', '').strip()) if value else None
            elif heading == 'Tax':
                item['tax'] = float(value.replace('£', '').strip()) if value else None
            elif heading == 'Availability':
                # keep the table availability too (may duplicate)
                item['availability'] = value
            elif heading == 'Number of reviews':
                try:
                    item['number_of_reviews'] = int(value)
                except:
                    item['number_of_reviews'] = 0

        # product page url
        item['product_page_url'] = response.url

        yield item