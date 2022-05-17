# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagrammParseItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    follower_to = scrapy.Field()
    following_by = scrapy.Field()
    photo = scrapy.Field()
    _id = scrapy.Field()


class InstagrammPostItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo_post = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    _id = scrapy.Field()
