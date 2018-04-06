# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    """
    用户信息
    """
    _id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    location = Field()  # 所在地
    brief_introduction = Field()  # 简介
    # birthday = Field()  # 生日
    school = Field()  # 学校
    register_time = Field()  # 注册时间
    credit = Field()  # 信用
    tweets_num = Field()  # 微博数
    follows_num = Field()  # 关注数
    fans_num = Field()  # 粉丝数
    verified = Field()  # 有没有认证
    verified_type = Field()  # -1 为没认证。0为个人认证，其余为企业认证
    verified_type_ext = Field()  # _ext为1时(橙色V)， _ext为0（黄色v）_ext
    user_level = Field()  # 等级
    vip_level = Field()  # 会员等级


class TweetItem(Item):
    """
    微博信息
    """
    _id = Field()  # 微博URL
    content = Field()  # 微博内容
    publish_time = Field()  # 发表时间
    location = Field()  # 定位坐标
    tools = Field()  # 发表工具/平台
    like_num = Field()  # 点赞数
    comment_num = Field()  # 评论数
    repost_num = Field()  # 转载数
    is_repost = Field()  # 是否是转载微博
    repost_source = Field()  # 如果是转载微博，原始微博的URL


class RelationshipItem(Item):
    """
    用户关系，只保留与关注的关系
    """
    fan_id = Field()  # 粉丝
    followed_id = Field()  # 被关注者的ID
