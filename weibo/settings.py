# -*- coding: utf-8 -*-

# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

DEFAULT_REQUEST_HEADERS = {
    "cookie": "SCF=AsJyCasIxgS59OhHHUWjr9OAw83N3BrFKTpCLz2myUf2BtJx74k6LmO67sUIRsbW2p6T2Wkbu-Ydn7vzesDPwaU.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfexCAdmDP14J1IQ4VfRHl5JpX5K-hUgL.Fo-0eheN1Kn71h-2dJLoIEqLxK-L12BL1heLxK-L12qLBoq_TCH8SbHWxFHWeEH8SCHFxb-4S7tt; SUB=_2A253f9auDeThGeBO7FoU-SnPzDmIHXVUg_rmrDV6PUJbkdANLUzMkW1NRa0QkCRygGMUOd6EmsMym95ZFVFBkzqk; SUHB=0nl-8vRPwpZPk4; OUTFOX_SEARCH_USER_ID_NCOO=1780588551.4011402; _T_WM=7553afc4b9cb284a15b7711d482ac814; ALF=1525077442; M_WEIBOCN_PARAMS=uicode%3D20000174; ___rl__test__cookies=1522988918251; H5_INDEX_TITLE=%E7%94%A8%E6%88%B76078597375; H5_INDEX=2",
    "user-agent": "OUTFOX_SEARCH_USER_ID_NCOO=1780588551.4011402; browser=d2VpYm9mYXhpYW4%3D; _T_WM=767a89eeec1856d21bf83f366492de34; ALF=1528973264; SCF=AsJyCasIxgS59OhHHUWjr9OAw83N3BrFKTpCLz2myUf2NPpOwZs9hVnbSFeufTzEnrDFfMwbM2F5sHWZcjnZqrI.; SUB=_2A253_rrTDeRhGeBN6VUX9SvEzT-IHXVVAMabrDV6PUJbktANLUzlkW1NRJ24IFLP_76Z5VhKSihhN6uoT9nTRcnU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYACoMUZFHDoS6U9MYf.vu5JpX5K-hUgL.Foq0eoMcSK-RSoe2dJLoI7yV9cyfwgvV97tt; SUHB=0QS5VG1P74Mf40; H5_INDEX_TITLE=nghuyong; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032536164011%26uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword; ___rl__test__cookies=1526614601368; H5_INDEX=0_all"
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'weibo.middlewares.WeiboSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'weibo.middlewares.MyCustomDownloaderMiddleware': 543,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'scrapy_proxies.RandomProxy': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# PROXY_LIST = './weibo/proxy_list.txt'
# PROXY_MODE = 0
# RETRY_TIMES = 3
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weibo.pipelines.MongoDBPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

LOG_LEVEL = 'DEBUG'
LOG_FILE = 'weibo_more.log'
