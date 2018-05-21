# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from weibo.items import RelationshipItem, UserItem, TweetItem


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client['Weibo_more']
        self.User = db['User']
        self.Tweet = db['Tweet']
        self.Relationship = db['Relationship']

    def process_item(self, item, spider):
        """
        判断item的类型，并作相应的处理，再入数据库
        """
        try:
            if isinstance(item, RelationshipItem):
                self.insert(self.Relationship, dict(item))
            elif isinstance(item, UserItem):
                self.insert(self.User, dict(item))
            elif isinstance(item, TweetItem):
                self.insert(self.Tweet, dict(item))
        except:
            pass

    def insert(self, collection, item):
        try:
            collection.insert(item)
        except Exception as e:
            print(e)
