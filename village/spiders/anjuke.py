# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from village.items import VillageItem
from scrapy.selector import HtmlXPathSelector 
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AnjukeSpider(CrawlSpider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]
    start_urls = []
    start_urls.append('http://shanghai.anjuke.com/community')    
    for i in xrange(1,1200,1):
    	start_urls.append(u'http://shanghai.anjuke.com/community/W0QQpZ%d'%i)
    
    rules = (Rule(SgmlLinkExtractor(allow=(r'http://shanghai.anjuke.com/community/view/\d+$')),
								    callback='village_parse'),)

    def village_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = VillageItem()
        item['name'] = hxs.xpath('//h1[@id="commtitle"]/a/text()').extract()[0]
        infos = hxs.xpath('//ul[@class="chamber-infolist"]/li')
        for index, link in enumerate(infos):
        	if index == 0:
		        item['address'] = link.xpath('text()').extract()[0].split("：")[1]
        	elif index == 3:
        		item['build_date'] = link.select('text()').extract()[0].split("：")[1]
        	elif index == 4:
        		item['developer'] = link.select('text()').extract()[0].split("：")[1]
        	elif index == 6:
        		item['property_company'] = link.select('text()').extract()[0].split("：")[1]

        item['village_id'] = response.url.split("/")[5]
        location =  hxs.xpath('//a[@id="propview_map"]/img/@src').extract()[0].partition('?')[2].split('&')[0].split('=')[1]
        item['longitude'] = location.split(',')[0]
        item['latitude'] = location.split(',')[1]

        return item