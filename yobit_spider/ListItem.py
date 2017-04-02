import scrapy

class ListItem(scrapy.Item):
    time = scrapy.Field()
    action = scrapy.Field()
    price = scrapy.Field()
    src_name = scrapy.Field()
    dst_name = scrapy.Field()