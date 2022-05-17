import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from urllib.parse import urljoin

from lerya_scrap.items import LeryaScrapItem


class LeryaSpider(scrapy.Spider):
    handle_httpstatus_list = [401]
    name = 'lerya'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://leroymerlin.ru/catalogue/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        print("!!!LEROY START!!!")
        print(f"Leroy response: {response.status}")
        next_page = response.xpath("//a[@ data-qa-pagination-item='right']/@href").get()
        if next_page:
            next_page = urljoin(response.url, next_page)
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        # With Loader:
        loader = ItemLoader(item=LeryaScrapItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@slot, 'title')]/text()")
        loader.add_xpath('price', "//span[contains(@slot, 'price')]/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[contains(@media, '(min-width: 1024px)')]/@data-origin")
        loader.add_xpath('stats', "//dl")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # Without Loader:
        # name = response.xpath("//h1[contains(@slot, 'title')]/text()").get()
        # price = response.xpath("//span[contains(@slot, 'price')]/text()").get()
        # photos = response.xpath("//picture[@slot='pictures']/source[contains(@media, '(min-width: 1024px)')]/@data-origin").getall()
        # url = response.url
        # yield LeryaScrapItem(name=name, price=price, photos=photos, url=url)


