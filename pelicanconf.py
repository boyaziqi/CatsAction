#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'CatsAction'
SITENAME = u"CatsAction's blog"
SITESUBTITLE = u''
SITEURL = 'https://boyaziqi.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/boyaziqi'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

foobar = "范孝大"

LOAD_CONTENT_CACHE = False
PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss', 'linenos': 'table'}
DEFAULT_DATE_FORMAT = '%Y-%m-%d  星期%a'

# 以下为本网站自定义设置
THEME = "gum"
GITHUB_URL = 'https://github.com/boyaziqi'
WEIBO_URL = 'http://weibo.com/boyziqi/home?wvr=5'
LINKEDIN_URL = 'https://www.linkedin.com/feed/'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/'
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_PAGINATION = 5
