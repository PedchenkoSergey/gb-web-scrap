import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst


def convert_price(value):
    print(value)

    # value = value.replace('\xa0', '')
    # try:
    #     value = int(value)
    # except:
    #     return value
    return value


class LeryaScrapItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()


class CastoScrapItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
