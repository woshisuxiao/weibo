#!/usr/bin/env python
# encoding: utf-8
"""
根据用户的user_id抓取用户信息、所有微博、关注/粉丝列表
"""
import json
import logging
from json import JSONDecodeError
from pprint import pprint
import re
from scrapy import Spider, Request
from weibo.items import UserItem, RelationshipItem, TweetItem
from weibo.settings import DEFAULT_REQUEST_HEADERS
from weibo.spiders.tool import clean_html


class WeiboSpider(Spider):
    name = "WeiboSpider"
    # 用户信息
    user_info_url = "https://m.weibo.cn/api/container/getIndex?uid={user_id}&type=uid&value={user_id}"
    # 关注人列表
    follows_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{user_id}&page={page}'
    # 粉丝列表
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{user_id}&since_id={since_id}'

    # 微博列表
    tweet_url = 'https://m.weibo.cn/api/container/getIndex?uid={user_id}&containerid={containerid}&page={page}'

    def start_requests(self):
        user_ids = ["1365309020", "1187354232", "6386642173", "3105898703"]
        for user_id in user_ids:
            yield Request(
                url=self.user_info_url.format(user_id=user_id),
                callback=self.parse_user_info,
                meta={'user_id': user_id}
            )

    def parse_follows(self, response):
        """获取关注列表"""
        cards = json.loads(response.text).get('data').get('cards')
        user_id = response.meta['user_id']
        if cards:  # 判断是否获取完全部关注人
            for card in cards:
                result = card.get('card_group')[1]
                if 'users' in result:
                    result = result['users']
                else:
                    continue
                for item in result:
                    if item.get('id'):
                        followed_id = item.get('id')
                        relationship_item = RelationshipItem()
                        relationship_item['_id'] = '{}-{}'.format(user_id, followed_id)
                        relationship_item['fan_id'] = user_id
                        relationship_item['followed_id'] = followed_id
                        yield relationship_item
                        yield Request(self.user_info_url.format(user_id=followed_id),
                                      callback=self.parse_user_info,
                                      meta={'user_id': followed_id}
                                      )
                # 获取下一页关注的人
                page = re.search('page=(\d+)', response.url)
                next_page = int(page.group(1)) + 1 if page else 2
                yield Request(self.follows_url.format(user_id=user_id, page=str(next_page)),
                              callback=self.parse_follows,
                              meta={'user_id': user_id}
                              )

    def parse_fans(self, response):
        """获取粉丝列表"""
        user_id = response.meta['user_id']
        cards = json.loads(response.text).get('data').get('cards')
        if cards:
            result = cards[0].get('card_group')
            for item in result:
                fans_id = item.get('user').get('id')
                relationship_item = RelationshipItem()
                relationship_item['_id'] = '{}-{}'.format(fans_id, user_id)
                relationship_item['fan_id'] = fans_id
                relationship_item['followed_id'] = user_id
                yield relationship_item
                yield Request(self.user_info_url.format(user_id=fans_id),
                              callback=self.parse_user_info,
                              meta={'user_id': fans_id}
                              )
            # 获取下一页粉丝
            since_id = re.search('since_id=(\d+)', response.url)
            next_since_id = int(since_id.group(1)) + 1 if since_id else 2
            yield Request(self.fans_url.format(user_id=user_id, since_id=next_since_id),
                          callback=self.parse_fans,
                          meta={'user_id': user_id}
                          )

    def parse_user_info(self, response):
        """
        获取用户信息
        """
        try:
            response_data = json.loads(response.text)
        except JSONDecodeError:
            self.log('获取用户信息失败 URL:{}'.format(response.url), level=logging.INFO)
            return
        if response_data['ok'] == 0:
            self.log('获取用户信息失败 URL:{}'.format(response.url), level=logging.INFO)
            return
        user_id = response.meta['user_id']
        user_info = response_data['data']['userInfo']
        user_item = UserItem()
        user_item['_id'] = user_info['id']
        user_item['nick_name'] = user_info['screen_name']
        user_item['brief_introduction'] = user_info['description']
        user_item['fans_num'] = user_info['followers_count']
        user_item['follows_num'] = user_info['follow_count']
        user_item['tweets_num'] = user_info['statuses_count']
        if user_info['gender'] == 'm':
            user_item['gender'] = '男'
        elif user_info['gender'] == 'f':
            user_item['gender'] = '女'
        else:
            user_item['gender'] = '其他'
        user_item['verified'] = user_info['verified']
        if user_info['verified']:
            if user_info['verified_type'] == 1:
                user_item['verified_type'] = '个人认证'
            else:
                user_item['verified_type'] = '企业认证'
            if user_info['verified_type_ext'] == 0:
                user_item['verified_type_ext'] = '黄色V'
            else:
                user_item['verified_type_ext'] = '橙色V'
        user_item['user_level'] = user_info['urank']
        user_item['vip_level'] = user_info['mbrank']
        tabs = response_data['data']['tabsInfo']['tabs']
        if type(tabs) is list:
            containerid = tabs[0]['containerid']
        else:
            containerid = tabs['0']['containerid']
        if 50 < int(user_item['fans_num']):
            if int(user_item['tweets_num']) > 30:
                yield Request(
                    url='https://m.weibo.cn/api/container/getIndex?containerid={}_-_INFO'.format(containerid),
                    callback=self.parse_further_user_info,
                    meta={'item': user_item, 'user_id': user_id}
                )

                tweet_tab = response_data['data']['tabsInfo']['tabs']
                if type(tweet_tab) is list:
                    tweet_tab = tweet_tab[1]
                else:
                    tweet_tab = tweet_tab['1']
                if tweet_tab['title'] == '微博':
                    containerid = tweet_tab['containerid']
                    headers = DEFAULT_REQUEST_HEADERS.copy()
                    headers['Referer'] = "https://m.weibo.cn/u/{}".format(user_id)
                    yield Request(
                        url=self.tweet_url.format(user_id=user_id, containerid=containerid, page=1),
                        headers=headers,
                        callback=self.parse_tweet,
                        meta={'is_first': True, 'user_id': user_id}
                    )

        yield Request(
            url=self.follows_url.format(user_id=user_id, page=1),
            callback=self.parse_follows,
            meta={'user_id': user_id}
        )

        yield Request(
            url=self.fans_url.format(user_id=user_id, since_id=1),
            callback=self.parse_follows,
            meta={'user_id': user_id}
        )

    def parse_further_user_info(self, response):
        response_data = json.loads(response.text)
        if response_data['ok'] == 0:
            self.log('获取更多用户信息失败 URL:{}'.format(response.url), level=logging.INFO)
            pprint(response_data)
            return
        user_item = response.meta['item']
        cards = response_data['data']['cards']
        card_group = []
        for card in cards:
            if 'card_group' in card:
                card_group.extend(card['card_group'])
        for card in card_group:
            if 'item_name' in card:
                if card['item_name'] == '所在地':
                    user_item['location'] = card['item_content']
                elif card['item_name'] == '学校':
                    user_item['school'] = card['item_content']
                elif card['item_name'] == '注册时间':
                    user_item['register_time'] = card['item_content']
                elif card['item_name'] == '阳光信用':
                    user_item['credit'] = card['item_content']
        yield user_item

    def parse_tweet(self, response):
        user_id = response.meta['user_id']
        response_json = json.loads(response.text)
        if 'is_first' in response.meta:
            total = response_json['data']['cardlistInfo']['total']
            all_page = int((total + 10 - 1) / 10)
            all_page = min(10, all_page)
            for page_num in range(2, all_page + 1):
                page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                yield Request(
                    url=page_url,
                    callback=self.parse_tweet,
                    headers=response.request.headers,
                    meta={'user_id': user_id}
                )
        cards = response_json.get("data").get("cards")
        for card in cards:
            # 每条微博的正文内容
            if card.get("card_type") == 9:
                mblog = card["mblog"]
                tweet_item = TweetItem()
                tweet_item['content'] = clean_html(mblog['text'])
                tweet_item['_id'] = 'https://weibo.com/{}/{}'.format(user_id, mblog['bid'])
                tweet_item['publish_time'] = mblog['created_at']
                tweet_item['tools'] = mblog['source']
                tweet_item['like_num'] = mblog['attitudes_count']
                tweet_item['comment_num'] = mblog['comments_count']
                tweet_item['repost_num'] = mblog['reposts_count']
                try:
                    tweet_item['location'] = re.search(r'<span class="surl-text">(.*?)</a>', mblog['text']).group(1)
                except AttributeError:
                    pass
                if 'retweeted_status' in mblog:
                    tweet_item['is_repost'] = True
                    tweet_item['repost_source'] = 'https://weibo.com/{}/{}'.format(
                        mblog['retweeted_status']['user']['id'], mblog['retweeted_status']['bid'])
                    tweet_item['source_create'] = mblog['retweeted_status']['created_at']
                    tweet_item['source_content'] = mblog['retweeted_status']['text']
                    tweet_item['source_repost_num'] = mblog['retweeted_status']['reposts_count']
                    tweet_item['source_comment_num'] = mblog['retweeted_status']['comments_count']
                    tweet_item['source_like_num'] = mblog['retweeted_status']['attitudes_count']
                    tweet_item['source_user_id'] = mblog['retweeted_status']['user']['id']
                    tweet_item['source_user_description'] = mblog['retweeted_status']['user']['description']

                else:
                    tweet_item['is_repost'] = False
                yield tweet_item
