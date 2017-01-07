#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

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

def main():
    tasks = TaskHelper()
    task = tasks.get_user_tasks(1).next()
    user_id = task['id']
    last_create_ts = task['last_create_ts']

    logging.info("Get user task(%d, %d) name=%s" % (user_id, last_create_ts, task['data']))

    aapi = AppPixivAPI()
    aapi.login("usersp", "passsp")

    illust_helper = IllustHelper()

    user_illusts = get_user_illusts(aapi, user_id, last_create_ts, req_auth=True)
    for illust in user_illusts:
        illust_helper.update(illust)

    logging.debug("user_id=%d get %d new illusts, last create_date=%s" % (user_id, len(user_illusts), user_illusts[0].create_date))

    new_task = tasks.user_task(user_id, to_timestamp(user_illusts[0].create_date), data=task['data'])
    tasks.update(new_task)

if __name__ == '__main__':
    main()
