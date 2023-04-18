# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    price_sale = scrapy.Field()
    sold = scrapy.Field()

class TgddPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    name = scrapy.Field()
    memory = scrapy.Field()
    color = scrapy.Field()
    originPrice = scrapy.Field()
    discountPrice = scrapy.Field()
    discountRate = scrapy.Field()
    screen = scrapy.Field()
    operatingSystem = scrapy.Field()
    frontCamera = scrapy.Field()
    behindCamera = scrapy.Field()
    chip = scrapy.Field()
    ram = scrapy.Field()
    sim = scrapy.Field()
    pin = scrapy.Field()
    imageUrl = scrapy.Field()
    rate = scrapy.Field()
    point = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()

class PhongvuPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    producer = scrapy.Field()
    price = scrapy.Field()
    price_sale = scrapy.Field()
    image = scrapy.Field()
    insurance = scrapy.Field()
    category = scrapy.Field()
    short_name = scrapy.Field()
    color = scrapy.Field()
    screen = scrapy.Field()
    pixels = scrapy.Field()
    ROM = scrapy.Field()
    OS = scrapy.Field()
    RAM = scrapy.Field()
    rate = scrapy.Field()
    point = scrapy.Field()
