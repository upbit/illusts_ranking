#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pymongo import MongoClient

from to_timestamp import to_timestamp

class IllustHelper():

    def __init__(self, mongodb='mongodb://localhost', db_name='pixiv', collection_name='illusts'):
        self.client = MongoClient(mongodb)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def _format_illust(self, illust):
        # _id
        illust['_id'] = illust['id']

        # create_date_ts
        illust['create_date_ts'] = to_timestamp(illust['create_date'])

        # 删除无用字段
        del illust['user']['is_followed']
        del illust['is_bookmarked']
        del illust['visible']
        del illust['is_muted']

        # 提取 tags.name
        tag_list = [ tag['name'] for tag in illust['tags'] ]
        illust['tags'] = tag_list

        # 提取 meta_pages.image_urls
        if not illust['meta_pages'] in [None, []]:
            meta_pages = {}
            for size in ['square_medium', 'medium', 'large', 'original']:
                meta_pages[size] = [ page['image_urls'][size] for page in illust['meta_pages'] ]
            illust['meta_pages'] = meta_pages

        return illust

    def insert(self, illust):
        obj_illust = self._format_illust(illust)
        return self.collection.insert_one(obj_illust)

    def update(self, illust, upsert=True):
        obj_illust = self._format_illust(illust)
        return self.collection.replace_one({'_id': obj_illust['_id']}, obj_illust, upsert=upsert)

    def get(self, illust_id):
        return [i for i in self.collection.find({"id": illust_id})][0]

def test():
    pass

if __name__ == '__main__':
    test()

