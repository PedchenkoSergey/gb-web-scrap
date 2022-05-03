# Scrapy settings for lerya_scrap project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lerya_scrap'
IMAGES_STORE = 'photos'

SPIDER_MODULES = ['lerya_scrap.spiders']
NEWSPIDER_MODULE = 'lerya_scrap.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2520 Yowser/2.5 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

LOG_ENABLED = True
LOG_LEVEL = "DEBUG"

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'cookie':'DY_SS_LOGIN_NECESSARY=true; DY_SS_CART_SYNC_NECESSARY=false; dtCookie=v_4_srv_4_sn_A5426A31762C54C6FDC5960DF6DC0C12_perc_1983_ol_1_app-3Ab82b63450c1d92de_0; disp_react_aa=1; disp_plp_promo_ab=A; ggr-widget-test=0; flowbox-gallery-pdp=0; _ym_uid=1651564656178758680; _ym_d=1651564656; _gcl_au=1.1.727165527.1651564656; iap.uid=a05db06565354c4b8db04191bad03c57; _ym_isad=2; tmr_lvid=81c18f091e0f0fa1ec8db83a01070bc7; tmr_lvidTS=1651564656110; ___dmpkit___=d934ee73-ebec-465d-a546-910fdb30bb86; _gaexp=GAX1.2.ouICWlkpTuKpvosrUFwQ2g.19166.1!mAlGV6AUTqahU-DeeZgLtQ.19183.3; x-api-option=cce-262; _ga=GA1.2.944447653.1651564656; _gid=GA1.2.1540952042.1651564656; DY_SS_CART_SYNC_NECESSARY=true; aplaut_distinct_id=ueBF01RDcFGN; _regionID=34; lastConfirmedRegionID=34; uxs_uid=b24f8fe0-cab6-11ec-84a1-a93496134829; cookie_accepted=true; GACookieStorage=GA1.2.944447653.1651564656; qrator_ssid=1651568454.887.sEeO9SbOJz5nxO2T-n1kfcg14mahqdrqh946e3eictp7j5jbi; storageForShopListActual=true; user-geolocation=0%2C0; tmr_detect=0%7C1651568466761; _dc_gtm_UA-20946020-1=1; BIGipServer~Public~yprulmwsaema_https_pool=!h+7BjUDrznqrQmxWscy7HZW/J2zRgFykyTD8BfU6tcf357nBKvRdr1fF17zZD6KCMg5i9IvyAO4JqRAeZlneHQcJPN0NTpA4np1CU++3; qrator_jsid=1651568454.493.VY2Af6bY919uXYAw-6hbj36ikusr0vuk9aer3ku67lvqtb2p3; tmr_reqNum=47'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lerya_scrap.middlewares.LeryaScrapSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'lerya_scrap.middlewares.LeryaScrapDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'lerya_scrap.pipelines.LeryaScrapPipeline': 300,
   'lerya_scrap.pipelines.LeryaPhotosPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
