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
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoScrapItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@class, 'product-essential__name')]/text()")
        loader.add_xpath('price', "//span[@class='regular-price']/span/span/span[1]/text()")
        loader.add_xpath('photos', "//img[contains(@class, 'top-slide__img')]/@data-src")
        loader.add_xpath('stats', "//div[contains(@class, 'product-specifications')]/dl")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1[contains(@class, 'product-essential__name')]/text()").get()
        # price = response.xpath("//span[@class='regular-price']/span/span/span[1]/text()").get()
        # photos = response.xpath("//img[contains(@class, 'top-slide__img')]/@data-src").getall()
        # url = response.url
        # yield CastoScrapItem(name=name, price=price, photos=photos, url=url)
