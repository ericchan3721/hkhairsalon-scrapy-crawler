# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HkhairsalonCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    overall_rating = scrapy.Field()
    rate_good = scrapy.Field()
    rate_ok = scrapy.Field()
    rate_bad = scrapy.Field()
    location = scrapy.Field()
    tel = scrapy.Field()
    price_range = scrapy.Field()
    pageviews = scrapy.Field()
    portfolios = scrapy.Field()
    pass
