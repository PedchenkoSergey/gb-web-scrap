from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.utils.python import to_bytes

from pymongo import MongoClient


class InstagrammParsePipeline:
    def process_item(self, item, spider):
        return item


class InstagrammPhotosPipeline(ImagesPipeline):
    pass
