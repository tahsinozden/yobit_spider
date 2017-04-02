import scrapy
import json
import operator
from pprint import pprint
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
# ..ListItem means get the module from the parent folder
from ..ListItem import ListItem
from ..DataAnalyzer import Analyzer

class QuotesSpider(scrapy.Spider):
    name = "yobit"
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.TRADE_BASE_URL = 'https://yobit.net/en/trade'
        self.all_data = []

    def start_requests(self):
        urls = [
            'https://yobit.net/en/',
        ]
        item = ListItem()
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            # request.meta['item'] = item
            yield request

    # closed hook of the spider
    def spider_closed(self, spider):
        spider.logger.info('=== Spider closed: %s', spider.name)
        # print("====================== done")
        # spider.logger.info(self.all_data)
        # with open('res.json', 'w') as out:
        #     out.write(json.dumps(self.all_data))
        with open('res.json', 'w') as out:
            out.write(json.dumps(self.all_data, sort_keys=True,
                          indent=4, separators=(',', ': ')))

        data = self.all_data
        # spider.logger.info("printing data " + data)
        analyzer = Analyzer('XMS', 'BTC', data)
        spider.logger.info(analyzer.analyze())

    def parse(self, response):

        all_pages = response.xpath('///table[@id="trade_market"]/tbody/tr/td/text()').extract()
        # print(all_pages)
        lst_trade_links = []
        for i in range(0, len(all_pages), 5):
        # for i in range(0, 10, 5):
            src = all_pages[i]
            dst = all_pages[i+1]

            if "$" in dst:
                dst = "USD"

            elif "R" in dst:
                dst = "RUR"

            else:
                dst = "BTC"

            # src = "XMS"
            # dst = "BTC"
            lst_trade_links.append("".join([self.TRADE_BASE_URL, "/", src, "/", dst]))

        # print("============== all links")
        # print(lst_trade_links)

        for link in lst_trade_links:
            request = scrapy.Request(link, callback=self.build_items)
            yield request


    def build_items(self, response):
        # print('============== printing the spider')
        # print(trs)
        list_items = []
        src_cur = response.url.split('/')[-2]
        dst_cur = response.url.split('/')[-1]
        all_trs = response.xpath('///table[@class="trade_history_table"]/tbody/tr/td/text()').extract()
        # print(all_trs)
        for i in range(1, len(all_trs), 4):
            lst_item = ListItem()
            lst_item['time'] = all_trs[i]
            lst_item['action'] = all_trs[i+1]
            lst_item['price'] = all_trs[i+2]
            lst_item['src_name'] = src_cur
            lst_item['dst_name'] = dst_cur
            list_items.append(dict(lst_item))

        # print(list_items)
        # add it to the all items
        self.all_data.append(list_items)


