# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import json
import scrapy
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class DuplicatePipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['village_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['village_id'])
            return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

 
class SQLiteStorePipeline(object):
    filename = 'data.sqlite'
 
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
 
    def process_item(self, item, spider):
        self.conn.execute('insert into village values(?,?,?,?,?,?,?,?)', 
                          (item['village_id'], item['name'], item['address'], item['build_date'],
                          	item['developer'], item['property_company'], item['latitude'], item['longitude']))
        return item
 
    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table village(village_id text primary key, name text, address text, build_date text,
        	developer text, property_company text, latitude float, longitude float)""")
        conn.commit()
        return conn