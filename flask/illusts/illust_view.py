#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
from mdb import *

from flask import Blueprint, render_template, redirect, url_for, request, make_response

illust_view = Blueprint('illust_view', __name__, template_folder='templates')

class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

def to_utf8(val):
    try:
        return val.encode('utf-8')
    except:
        return val

@illust_view.route('/', methods=['GET'])
def home_page():
    return redirect(url_for('.rankings', sort_by='total_bookmarks'))

# sort_by: total_bookmarks, total_view
@illust_view.route('/<sort_by>', methods=['GET'], defaults={ 'offset': 0, 'size': 30 })
def rankings(sort_by, offset, size):
    illust_helper = IllustHelper()

    # get illusts from mongodb
    illusts = []
    for raw_illust in list(illust_helper.collection.find().sort(sort_by, -1).skip(offset).limit(size)):
        illust = JsonDict(raw_illust)
        bookmark_rate = float(illust.total_bookmarks) / illust.total_view if illust.total_view > 0 else 0.0
        illust['bookmark_rate'] = bookmark_rate
        illusts.append(illust)

    title = 'Illusts排行榜 - %s' % to_utf8(sort_by)
    content = 'SortBy: %s (%d-%d)' % (sort_by, offset+1, offset+size)
    return render_template('illusts.html', title=title.decode('utf-8'), content=content.decode('utf-8'), illusts=illusts, t=int(time.time()))
