import json
import os
from dotenv import load_dotenv
import re
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instagramm_parse.items import InstagrammParseItem


class FollowersSpider(scrapy.Spider):
    # handle_httpstatus_list = [401, 302]
    name = 'followers'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # inst_login = os.environ.get('inst_login')
    # inst_pwd = os.environ.get('inst_pwd')
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
                    callback=self.user_data_followers_parse,
                    cb_kwargs={'username': user}
                )
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_data_following_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_followers_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        url_followers = f'{self.inst_followers_link}{user_id}/followers/?{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)},
            headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followers = f'{self.inst_followers_link}{user_id}/followers/?{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)},
                headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        users = j_data.get('users')
        for user in users:
            item = InstagrammParseItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                follower_to=[username],
                following_by=[],
                photo=user.get('profile_pic_url')
            )
            yield item

    def user_data_following_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        url_followers = f'{self.inst_followers_link}{user_id}/following/?{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_following_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)},
            headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_following_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followers = f'{self.inst_followers_link}{user_id}/followers/?{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)},
                headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        users = j_data.get('users')
        for user in users:
            item = InstagrammParseItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                following_by=[username],
                follower_to=[],
                photo=user.get('profile_pic_url')
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
