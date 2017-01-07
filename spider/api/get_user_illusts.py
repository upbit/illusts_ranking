#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pixivpy3 import *

from to_timestamp import to_timestamp

def get_user_illusts(aapi, user_id, last_timestamp=0, req_auth=False):
    illusts = []
    json_result = aapi.user_illusts(user_id, req_auth=req_auth)
    while len(json_result.illusts) > 0:
        illusts.extend(json_result.illusts)

        # 最后一个作品的上传时间小于上次抓取时间，退出
        last_illust = json_result.illusts[-1]
        if last_timestamp > to_timestamp(last_illust.create_date):
            break

        # 继续翻页
        time.sleep(0.2)
        next_qs = aapi.parse_qs(json_result.next_url)
        if not next_qs: break
        json_result = aapi.user_illusts(req_auth=req_auth, **next_qs)

    return illusts

def test():
    aapi = AppPixivAPI()
    user_illusts = get_user_illusts(aapi, 660788, 1460942026, False)
    for illust in user_illusts:
        print illust.id, illust.title

    print user_illusts[0].create_date

if __name__ == '__main__':
    test()
