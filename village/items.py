# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VillageItem(scrapy.Item):
    village_id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    build_date = scrapy.Field()
    developer = scrapy.Field()
    property_company = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

