import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lerya_scrap.items import CastoScrapItem


class CastoSpider(scrapy.Spider):
    name = 'casto'
    allowed_domains = ['castorama.ru']

    # start_urls = ['http://castorama.ru/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://castorama.ru/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        print("!!!CASTO START!!!")
        print(f"Casto response: {response.status}")
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoScrapItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@class, 'product-essential__name')]/text()")
        loader.add_xpath('price', "//span[@class='regular-price']/text()")
        loader.add_xpath('photos', "//img[contains(@class, 'top-slide__img')]/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
