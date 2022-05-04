from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.utils.python import to_bytes

from pymongo import MongoClient


# Базу MongoDB развернул в docker контейнере: docker run -d -p 27017:27017 --name m1 mongo
class LeryaScrapPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.goodscrap

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item


class LeryaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("SAVING PHOTOS")
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{self.crawler.spider.name}/{item["name"]}/{image_guid}.jpg'
