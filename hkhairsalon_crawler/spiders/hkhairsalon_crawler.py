import scrapy
from datetime import datetime
import re
import hkhairsalon_crawler.items as items

class HairSalonSpider(scrapy.Spider):

    name = 'hairsalon_spider'
    start_from_item_id = 0
    
    def __init__(self, type='1', start_index=0, **kwargs):
        # set crawl parameters
        self.type = type
        self.start_index = start_index
        self.start_urls = [f'https://hkhairsalon.com/shop/list.php?type={type}&start={start_index}']
        # set filename for each crawl
        if (type == '1'):
            self.filename_prefix = "stylist"
        else:
            self.filename_prefix = "salon"
        self.hk_hair_salon_csv_filename = 'hkhairsalon_' + self.filename_prefix + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + '.csv'
        # super.init
        super().__init__(**kwargs)

    def parse(self, response):
        # return super().parse(response)

        if len(response.css('div.product-box')) > 0:
            print(f'Crawling a page with params {self.start_index}-{str(int(self.start_index) + 8)}')

            for list_data in response.css('div.product-box'):
                name = list_data.css('div.item-content > h3.item-title > a::text').get();
                overall_rating = list_data.css('div.item-img > ul.item-rating > li > span::text').get().split(' / ')[0]
                rate_good = list_data.css('div.item-content > ul.rate-list > li:nth-child(1) > span.rate-good::text').get()
                rate_ok = list_data.css('div.item-content > ul.rate-list > li:nth-child(2) > span.rate-ok::text').get()
                rate_bad = list_data.css('div.item-content > ul.rate-list > li:nth-child(3) > span.rate-bad::text').get()
                
                # loop through & extract contact info
                contact_info = {}
                contact_info_selector = list_data.css('div.item-content > ul.contact-info > li')
                if contact_info_selector is not None:
                    for data_row in contact_info_selector:
                        # get key
                        contact_info_data_key = self.get_data_key(data_row.css('i::attr(class)').get())
                        # print(contact_info_data_key + " : " + data_row.css('i::text').get())

                        # get data
                        if (contact_info_data_key == 'location'):
                            contact_info[contact_info_data_key] = re.sub(r"\r|\n|\r\n|\t|\t\n|\n\t", "", data_row.xpath('string(.)').extract()[0]).strip()
                        elif (contact_info_data_key == 'pageviews'):
                            contact_info[contact_info_data_key] = re.sub(r"\D", "", data_row.css('::text').get())
                        elif (contact_info_data_key == 'portfolios'):
                            contact_info[contact_info_data_key] = data_row.css('a > span::text').get()
                        else:
                            contact_info[contact_info_data_key] = data_row.css('::text').get()

                # print(contact_info)

                # use scrapy.Item
                crawled_item = items.HkhairsalonCrawlerItem()
                crawled_item['name'] = name
                crawled_item['overall_rating'] = overall_rating
                crawled_item['rate_good'] = rate_good
                crawled_item['rate_ok'] = rate_ok
                crawled_item['rate_bad'] = rate_bad

                for data in ['location', 'tel', 'price_range', 'pageviews', 'portfolios']:
                    if data in contact_info:
                        crawled_item[data] = contact_info[data]
                    else:
                        crawled_item[data] = ''

                yield crawled_item

            # update next page to be crawled
            self.start_index += 8

            next_page_url = response.css('ul.pagination-layout1 > li:last-child > a::attr(href)').get()
            next_page_full_url = "https://hkhairsalon.com/shop/" + next_page_url
            have_next_page = response.css('ul.pagination-layout1 > li:last-child > a > i::attr(class)').get()
            is_last_pagination_active = response.css('ul.pagination-layout1 > li:last-child::attr(class)').get()


            # if have_next_page == 'flaticon-right-arrow' and have_next_page is not None:
            #     yield response.follow(next_page_full_url, callback=self.parse)

            if is_last_pagination_active != 'active':
                yield response.follow(next_page_full_url, callback=self.parse)
        
        else:
            print('No more content on this page # ')
            print('Done!')

    def get_data_key(self, style_attr_value):
        # print('get_data_key: ' + style_attr_value)
        return {
            'fas fa-map-marker-alt': 'location',
            'flaticon-phone-call': 'tel',
            'fas fa-dollar-sign': 'price_range',
            'fas fa-eye': 'pageviews',
            'fas fa-file': 'portfolios',
        }.get(style_attr_value)