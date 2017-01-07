#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from illusts.index import index
from illusts.illust_view import illust_view

app = Flask(__name__)

# blueprints
app.register_blueprint(index)
app.register_blueprint(illust_view, url_prefix='/illusts')

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'flask server for view mongodb illusts'
)

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8888)
