Title: 关于pelican 主题gum bug的处理
Date: 2015-01-05
Modified: 2017-04-10 18:11
category: python
tags: pelican, blog, jinjia2, html

最近在用pelican搭建个人静态博客时，在安装主题时，发现官方提供的主题gum不能正常渲染出tags和pages，下面简单记录处理过程。想了解pelican的安装，可以查看我的[pelican安装与部署]({filename}/pelican.md)
#### 1：安装pelican主题
下面以安装gum为例
```shell
git clone https://github.com/getpelican/pelican-themes.git
cp -r ~/pelican-themes/gum /you-blog-directory
```
接下来在配置文件pelicanconf.py中指定主题`theme = gum`。其实可以不用把主题复制到你的博客目录，你只需在theme后指定主题所在目录，让pelican正确解析到就行。不过为了修改和git版本跟踪，这里把它复制到博客目录。

#### 2：gum主题tags和pages的渲染问题。
找到gum模板文件sidebar.html。发现它把pages写成PAGES了，导致侧边栏Pages总未展示。官方主题有好几个都有这个问题，我估计是仿照一个主题写的缘故。
```
<h4>Tags</h4>
{% if tags %}
	<ul class="blank">
	{% for tag in tag_cloud %}
	    <li class="tag-{{ tag.1 }}"><a href="{{ SITEURL }}/{{ tag.0.url }}">{{ tag.0|e }}</a></li>
	{% endfor %}
</ul>
{% endif %}
```
上面是gum对于tags的渲染，需要修改成如下
```
<a href="{{ SITEURL }}/tags.html"><h4>Tags</h4></a>
{% if tags %}
	<ul class="blank">
	{% for tag, _ in tags %}
	    <li class="tag-{{ tag }}"><a href="{{ SITEURL }}/{{ tag.url }}">{{ tag|e }}</a></li>
	{% endfor %}
</ul>
{% endif %}
```
至于为何修改成这样，请参考官方文档[Creating themes](http://docs.getpelican.com/en/stable/themes.html)

#### 3: 对tags和categories界面展示的优化
tags.html和categories.html模板展示博客的tags列表和分类列表。gum原来的模板并未展示每个tag或category对应的文章，于是我做了如下修改
```
{% extends "base.html" %}
{% block title %}{{ SITENAME }} - Tags{% endblock %}
{% block content %}
<h4><i class="icon-tags icon-large"></i>Tags for {{ SITENAME }}</h4>
<ul>
{% for tag, articles in tags %}
<li class="tag-{{ tag }}">
	<a href="{{ SITEURL }}/{{ tag.url }}">
		<i class="icon-tag icon-large"></i>{{ tag|e }}
	</a>
    <ul>
        {% for article in articles %}
            <li><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></li>
        {% endfor %}
    </ul>
</li>
{% endfor %}
</ul>
{% endblock %}
```
gum主题原来的模板
```
{% extends "base.html" %}
{% block content %}
<ul>
<li class="nav-header"><h4><i class="icon-tags icon-large"></i>Tags</h4></li>
{% for tag in tag_cloud %}
<li class="tag-{{ tag.1 }}">
	<a href="{{ SITEURL }}/{{ tag.0.url }}">
		<i class="icon-tag icon-large"></i>{{ tag.0|e }}
	</a>
</li>
{% endfor %}
</ul>
{% endblock %}
```
categories.html我就不粘贴代码了，思路都一样。并且原模板对于categories.html也没有bug。
    
由于附图不方便文章布局，对于上面修改后的页面效果，可以自行修改预览。
