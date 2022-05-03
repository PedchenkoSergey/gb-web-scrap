import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lerya_scrap.items import LeryaScrapItem


class LeryaSpider(scrapy.Spider):
    handle_httpstatus_list = [401]
    name = 'lerya'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = [f"https://leroymerlin.ru/catalogue/santehnika/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://leroymerlin.ru/catalogue/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        print("!!!LEROY START!!!")
        print(f"Leroy response: {response.status}")
        pass
        # links = response.xpath("//a[@data-marker='item-title']")
        # for link in links:
        #     yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeryaScrapItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('price', "//span[contains(@class,'js-item-price')]/text()")
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-frame')]/@data-url")
        loader.add_value('url', response.url)
        yield loader.load_item()
