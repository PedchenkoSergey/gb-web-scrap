import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
