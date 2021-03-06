import json
import re
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instagramm_parse.items import InstagrammPostItem


class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # inst_login = 'maetview'
    # inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1652125310:AepQAKBHk7R5ETXyZBFCvBne9g7WzEw15E8bRIjuj03qhHAIPU/QMBabgTCbYIhJy1UNxqopa26VXkQNuGAwyP6jSeaKNwbEn3pcj9CwvseCYSpc+36gj7fUIrhqn2uCh6nBrwQebbw6VhugTEqFYgGwfFZYfkYT'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1650388687:AUVQAPLsNiCtdG0b660bL/la/fAfzNJ0AaVNGPhAI7fwS9ANR85sT7Kjag60UVTeviSs34AXFch4cAYMc8Pq56W6i7ntwpu2ucSOa3aIY3LRVrPRqB2XvkxeB+KW6C2TQEPNVbnxpAqk8m4yOJg='

    parse_user = [
        'rossignolsnowboards',
        'burtonrussia',
    ]
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    inst_followers_link = 'https://i.instagram.com/api/v1/friendships/'
    # posts_hash = 'd4d88dc1500312af6f937f7b804c68c3'
    posts_hash = '396983faee97f4b49ccbe105b4daf7a0'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_user:
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_data_posts_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_posts_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)},
                headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstagrammPostItem(
                user_id=user_id,
                username=username,
                photo_post=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
            )
            yield item

    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """ Get user ID """
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
