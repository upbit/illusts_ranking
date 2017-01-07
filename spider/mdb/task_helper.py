#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pymongo import MongoClient

class TaskHelper():

    def __init__(self, mongodb='mongodb://localhost', db_name='pixiv', collection_name='tasks'):
        self.client = MongoClient(mongodb)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def user_task(self, user_id, last_create_ts, data=None):
        task = {
            '_id': 'user_%s' % (user_id),
            'type': 'user',
            'id': user_id,
            'last_create_ts': last_create_ts,
            'modify': int(time.time()),
        }
        if data:
            task['data'] = data
        return task

    def insert(self, task):
        return self.collection.insert_one(task)

    def update(self, task, upsert=True):
        return self.collection.replace_one({'_id': task['_id']}, task, upsert=upsert)

    def get_user_tasks(self, limit=3):
        "获取limit个最久没更新的user_task"
        return self.collection.aggregate([
          { '$match': { 'type' : 'user' } },
          { '$sort': { 'modify': 1 } },
          { '$limit': limit },
        ])

def test():
    tasks = TaskHelper()
    task = tasks.get_user_tasks(1).next()
    print task

    new_task = tasks.user_task(task['id'], task['last_create_ts']+1, data=task['data'])
    print new_task

    result = tasks.update(new_task)
    print result.matched_count, result.modified_count, result.upserted_id
    

if __name__ == '__main__':
    test()

