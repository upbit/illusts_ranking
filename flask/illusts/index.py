#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request, make_response

index = Blueprint('index', __name__, template_folder='templates')

@index.route('/', methods=['GET'])
def index_page():
    return redirect(url_for('illust_view.home_page'))
