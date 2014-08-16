# -*- coding: utf-8 -*-

# Scrapy settings for village project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'village'

SPIDER_MODULES = ['village.spiders']
NEWSPIDER_MODULE = 'village.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'village (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'village.pipelines.DuplicatePipeline': 1,
    'village.pipelines.JsonWriterPipeline': 2,
    'village.pipelines.SQLiteStorePipeline':5
}