import scrapy


class FollowersSpider(scrapy.Spider):
    name = 'followers'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1650388687:AUVQAPLsNiCtdG0b660bL/la/fAfzNJ0AaVNGPhAI7fwS9ANR85sT7Kjag60UVTeviSs34AXFch4cAYMc8Pq56W6i7ntwpu2ucSOa3aIY3LRVrPRqB2XvkxeB+KW6C2TQEPNVbnxpAqk8m4yOJg='
    parse_user = 'techskills_2022'
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '396983faee97f4b49ccbe105b4daf7a0'

    def parse(self, response):
        pass
