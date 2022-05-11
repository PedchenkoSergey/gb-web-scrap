from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes

from pymongo import MongoClient


class InstagrammParsePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.instagram

    def process_item(self, item, spider):
        collection = self.db['users']
        if spider['name'] == 'followers':
            db_user = collection.find({'username': item.get('username')})
            if db_user:
                if item.get('follower_to'):
                    collection.update_one(
                        {'username': db_user.get('username')},
                        {'$set': {
                            'follower_to': list(set(db_user.get('follower_to').extend(item.get('follower_to')))),
                            'following_by': [],
                            'user_id': item.get('user_id'),
                            'photo': item.get('photo')

                        }}
                    )
                    db_user_follower = collection.find({'username': item.get('follower_to')[0]})
                    if db_user_follower:
                        collection.update_one(
                            {'username': item.get('follower_to')[0]},
                            {'$set': {'following_by': list(
                                set(db_user_follower.get('following_by').append(db_user.get('username'))))}}
                        )
                    else:
                        collection.insert_one({
                            'username': item.get('follower_to')[0],
                            'following_by': [db_user.get('username')]
                        })
                if item.get('following_by'):
                    collection.update_one(
                        {'username': db_user.get('username')},
                        {'$set': {
                            'following_by': list(set(db_user.get('following_by').extend(item.get('following_by')))),
                            'follower_to': [],
                            'user_id': item.get('user_id'),
                            'photo': item.get('photo')
                        }}
                    )
                    db_user_following = collection.find({'username': item.get('following_by')[0]})
                    if db_user_following:
                        collection.update_one(
                            {'username': item.get('following_by')[0]},
                            {'$set': {'follower_to': list(
                                set(db_user_following.get('follower_to').append(db_user.get('username'))))}}
                        )
                    else:
                        collection.insert_one({
                            'username': item.get('following_by')[0],
                            'following_by': [db_user.get('username')]
                        })

        elif spider['name'] == 'followers':
            collection.insert_one(item)
        return item


# Should install Pillow: pip install pillow:
class InstagrammPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("SAVING PHOTOS")
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{self.crawler.spider.name}/{item["username"]}/{image_guid}.jpg'
