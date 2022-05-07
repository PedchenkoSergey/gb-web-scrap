import json
import re
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy


class FollowersSpider(scrapy.Spider):
    name = 'followers'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1650388687:AUVQAPLsNiCtdG0b660bL/la/fAfzNJ0AaVNGPhAI7fwS9ANR85sT7Kjag60UVTeviSs34AXFch4cAYMc8Pq56W6i7ntwpu2ucSOa3aIY3LRVrPRqB2XvkxeB+KW6C2TQEPNVbnxpAqk8m4yOJg='
    parse_user = [
        'techskills_2022',
        ]
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
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
