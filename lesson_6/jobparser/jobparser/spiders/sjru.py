import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            next_page = urljoin(response.url, next_page)
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class,'YrERR')]/@href").getall()
        for link in links:
            link = urljoin(response.url, link)
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("div.f-test-vacancy-base-info h1::text").get()
        salary = response.xpath("//div[@class='_3E1tc']/span//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
