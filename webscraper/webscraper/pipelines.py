# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlite3

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

class CleanAndConvertPipeline:
    def process_item(self, item, spider):
        # price fields -> float
        for price_field in ('price', 'price_excl_tax', 'price_incl_tax', 'tax'):
            if item.get(price_field):
                try:
                    item[price_field] = float(str(item[price_field]).replace('£', '').strip())
                except:
                    item[price_field] = None

        # availability -> extract number if present: "In stock (22 available)"
        avail = item.get('availability') or ""
        m = re.search(r'\((\d+)\s+available\)', avail)
        item['stock'] = int(m.group(1)) if m else (1 if 'In stock' in avail else 0)

        # rating number
        item['rating'] = item.get('rating', 0)

        # keep description blank if None
        if item.get('description') is None:
            item['description'] = ""

        return item

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("books.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            price REAL,
            price_excl_tax REAL,
            price_incl_tax REAL,
            tax REAL,
            upc TEXT,
            product_type TEXT,
            availability TEXT,
            stock INTEGER,
            number_of_reviews INTEGER,
            category TEXT,
            rating INTEGER,
            description TEXT,
            image_url TEXT,
            product_page_url TEXT
        )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (
                title, price, price_excl_tax, price_incl_tax, tax, upc,
                product_type, availability, stock, number_of_reviews,
                category, rating, description, image_url, product_page_url
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            item.get('title'),
            item.get('price'),
            item.get('price_excl_tax'),
            item.get('price_incl_tax'),
            item.get('tax'),
            item.get('upc'),
            item.get('product_type'),
            item.get('availability'),
            item.get('stock'),
            item.get('number_of_reviews'),
            item.get('category'),
            item.get('rating'),
            item.get('description'),
            item.get('image_url'),
            item.get('product_page_url'),
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
