#!/usr/bin/env python
# encoding: utf-8
import pandas
import os
import pandas as pd


def export(command, file_name):
    os.system(command)
    csv = pd.read_csv('{}.csv'.format(file_name), encoding='utf-8', engine='python')
    writer = pd.ExcelWriter('{}.xlsx'.format(file_name), engine='xlsxwriter', options={'strings_to_urls': False})
    csv.to_excel(writer, index=False)
    writer.close()
    os.remove('{}.csv'.format(file_name))
    print('{}导出Excel数据完毕'.format(file_name))


information_command = 'mongoexport -h localhost -d Weibo -c User --type csv -o user.csv -f _id,nick_name,gender,location,brief_introduction,school,register_time,credit,tweets_num,follows_num,fans_num,verified,verified_type,verified_type_ext,user_level,vip_level'
tweet_command = 'mongoexport -h localhost -d Weibo -c Tweet --type csv -o tweet.csv -f _id,content,publish_time,location,tools,like_num,comment_num,repost_num,is_repost,repost_source,source_create,source_content,source_repost_num,source_comment_num,source_like_num,source_user_id,source_user_description'

export(information_command, 'user')
export(tweet_command, 'tweet')
