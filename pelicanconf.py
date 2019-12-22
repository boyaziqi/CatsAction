#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'CatsAction'
SITENAME = u"CatsAction's blog"
SITESUBTITLE = u"It's a wonderful world"
SITEURL = 'https://boyaziqi.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
  ('LeetCode', 'https://leetcode-cn.com/', '力扣中国站点'),
  ('CoolShell', 'https://coolshell.cn/about', '陈皓酷壳'),
  ('Yikun', 'https://yikun.github.io/', '姜毅坤博客'),
  ('牛客网', 'https://www.nowcoder.com/', '牛客网'),
)
LINKS_PROFILE_LABEL = None

# Social widget
SOCIAL_PROFILE_LABEL = u'Stay in Touch'
SOCIAL = (
  ('Email', 'catsaction@126.com', 'My Email Address'),
  ('Github', 'https://github.com/boyaziqi', 'catsaction Github Repository'),
  ('LinkedIn', 'https://www.linkedin.com/feed/', 'My LinkedIn'),
)

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "neighbors",
    "tipue_search",
]

DIRECT_TEMPLATES = ["index", "tags", "categories", "archives", "search", "404"]
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

LOAD_CONTENT_CACHE = False
PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss', 'linenos': 'table'}
DEFAULT_DATE_FORMAT = '%Y-%m-%d %A'
# DATE_FORMATS = {"en": '%Y-%m-%d %A'}

# 以下为本网站自定义设置
THEME = "elegant"
# DISPLAY_PAGES_ON_MENU = True
# DISPLAY_CATEGORIES_ON_MENU = False
LANDING_PAGE_TITLE = "It's a wonderful world"
foobar = "范孝大"
