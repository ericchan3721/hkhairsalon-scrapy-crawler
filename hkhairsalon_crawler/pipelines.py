# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class HkhairsalonCrawlerPipeline:

    def process_item(self, item, spider):
        with open(spider.hk_hair_salon_csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            csv_writer.writerow(item)
        return item

    def open_spider(self, spider):
        header_keys = ['name', 'overall_rating', 'rate_good', 'rate_ok', 'rate_bad', 'location', 'tel', 'price_range', 'pageviews', 'portfolios']
        with open(spider.hk_hair_salon_csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header_keys)
            csv_writer.writeheader()
