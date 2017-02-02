#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
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

def fetch_ranking(aapi, mode, date, max_page=2):
    illust_helper = IllustHelper()

    json_result = aapi.illust_ranking(mode=mode, date=date, req_auth=True)
    last_page = max_page

    new = 0
    total = 0
    while len(json_result.illusts) > 0:
        for illust in json_result.illusts:
            is_update = illust_helper.update(illust).modified_count
            new += 1 if (is_update == 0) else 0
            total += 1

        time.sleep(0.2)
        next_qs = aapi.parse_qs(json_result.next_url)
        if not next_qs: break
        last_page -= 1
        if last_page <= 0: break
        json_result = aapi.illust_ranking(req_auth=True, **next_qs)

    print ">> Get %d/%d new illusts" % (new, total)

def main():
    aapi = AppPixivAPI()
    aapi.login("usersp", "passsp")

    mode = 'day_male_r18'
    yestoday_date = datetime.datetime.now() - datetime.timedelta(days=1)

    fetch_ranking(aapi, mode, yestoday_date.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    main()
