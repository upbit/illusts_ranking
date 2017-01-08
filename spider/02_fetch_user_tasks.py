#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

from pixivpy3 import *
from mdb import *
from api import get_user_illusts, to_timestamp

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def fetch_one(aapi, loop):
    tasks = TaskHelper()
    task = tasks.get_user_tasks(1).next()
    user_id = task['id']
    last_create_ts = task['last_create_ts']
    logging.info("(%d) Get user task(%d, %d) name=%s" % (loop, user_id, last_create_ts, task['data']))

    illust_helper = IllustHelper()
    user_illusts = get_user_illusts(aapi, user_id, last_create_ts, type='illust', req_auth=True)
    # user_illusts = get_user_illusts(aapi, user_id, last_create_ts, type='manga', req_auth=True)
    for illust in user_illusts:
        illust_helper.update(illust)
    logging.debug("(%d) user_id=%d get %d new illusts, last create_date=%s" % (loop, user_id, len(user_illusts), user_illusts[0].create_date))

    new_task = tasks.user_task(user_id, to_timestamp(user_illusts[0].create_date), data=task['data'])
    tasks.update(new_task)

def main():
    aapi = AppPixivAPI()
    aapi.login("usersp", "passsp")

    for loop in range(32):
        fetch_one(aapi, loop)

        sleep_time = 5.0 + random.random() * 60
        logging.debug("(%d) sleep(%.1f)" % (loop+1, sleep_time))
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()
