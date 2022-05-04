import re
import scrapy
from scrapy import Selector
from itemloaders.processors import Compose, MapCompose, TakeFirst


def convert_price(value):
    value = value.replace('\xa0', '').replace(' ', '')
    try:
        value = int(value)
    except:
        return value
    return value


def convert_stats_casto(value):
    sel = Selector(text=value)
    stats_keys = sel.xpath('//dt/span[contains(@class, "specs-table__attribute-name")]/text()').getall()
    stats_values = sel.xpath('//dd/text()').getall()
    for i in range(len(stats_keys)):
        stats_keys[i] = re.sub(r'\s\s+', ' ', stats_keys[i])
    for i in range(len(stats_values)):
        stats_values[i] = re.sub(r'\s\s+', ' ', stats_values[i])

    value_dict = dict(zip(stats_keys, stats_values))
    return value_dict


def convert_stats_lerya(value):
    sel = Selector(text=value)
    stats_keys = sel.xpath("//dt[@class='def-list__term']/text()").getall()
    stats_values = sel.xpath('//dd/text()').getall()
    for i in range(len(stats_keys)):
        stats_keys[i] = re.sub(r'\s\s+', ' ', stats_keys[i])
    for i in range(len(stats_values)):
        stats_values[i] = re.sub(r'\s\s+', ' ', stats_values[i])

    value_dict = dict(zip(stats_keys, stats_values))
    return value_dict


class LeryaScrapItem(scrapy.Item):
    # With Loader:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    stats = scrapy.Field(input_processor=MapCompose(convert_stats_lerya))
    _id = scrapy.Field()

    # Without Loader:
    # name = scrapy.Field()
    # url = scrapy.Field()
    # price = scrapy.Field()
    # photos = scrapy.Field()
    # _id = scrapy.Field()


class CastoScrapItem(scrapy.Item):
    # With Loader:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    stats = scrapy.Field(input_processor=MapCompose(convert_stats_casto))
    _id = scrapy.Field()

    # Without Loader:
    # name = scrapy.Field()
    # url = scrapy.Field()
    # price = scrapy.Field()
    # photos = scrapy.Field()
    # _id = scrapy.Field()
