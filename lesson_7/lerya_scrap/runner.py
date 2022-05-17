from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from lerya_scrap.spiders.lerya import LeryaSpider
from lerya_scrap.spiders.casto import CastoSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(LeryaSpider, query='santehnika/')
    runner.crawl(CastoSpider, query='gardening-and-outdoor/gardening-equipment/lawn-mowers')

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
