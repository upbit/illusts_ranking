#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from pixivpy3 import *
from mdb import *

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
    aapi = AppPixivAPI()

    total = 0
    seed_uid = 7314824
    json_result = aapi.user_following(seed_uid)
    while len(json_result.user_previews) > 0:
        for preview in json_result.user_previews:
            user = preview.user
            logging.debug("user_id=%d name=%s" % (user.id, user.name))

            task = tasks.user_task(user.id, 0, data=user.name)
            try:
                tasks.insert(task)
                total += 1
            except Exception, e:
                logging.warning("user_id=%d exist: %s" % (user.id, e))

        time.sleep(1.1)
        next_qs = aapi.parse_qs(json_result.next_url)
        if not next_qs: break
        json_result = aapi.user_following(**next_qs)

    logging.info(">> Import %d user tasks." % (total))

if __name__ == '__main__':
    main()
