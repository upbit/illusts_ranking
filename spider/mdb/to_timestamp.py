#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime

def to_timestamp(val):
    dt = datetime.datetime.strptime(val[:-6], '%Y-%m-%dT%H:%M:%S') - datetime.timedelta(hours=1) # jp has +09:00 timezone, conv to +08:00
    return int(time.mktime(dt.timetuple()))
