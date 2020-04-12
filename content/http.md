title: HTTP头部知识
date: 2017-04-02
category: HTTP
tags: HTTP

## 前述

本篇文章对HTTP头部选项做一个归类，并对常见的字段做一下介绍。

## 分类

- 通用头部

- 请求头部

- 相应头部

- 实体头部

下面按每个分类介绍一些主要的头部。

## 通用头部

*Date*

*Connection*

*Cache-Control*

## 请求头部

1，标识类

*Host*

*User-Agent*

2，Accept类

*Accept*

*Accept-Encodeing*

*Accept-Language*

*Accept-Charset*

3，缓存相关类

*If-Match*

*If-Modified-Sine*

*If-Range*

4，认证相关类

*Authorization*

5，其他

*Range*

*Referer*

## 相应头部

1，标识相关

*Allow*

*Refresh*

*Server*

2，缓存相关

*Age*

其他在实体头部分类

3，认证相关

*Proxy-Authenticate*

*WWW-Authenticate*

4，代理相关

*Location*

5，其他

*Set-Cookie*

## 实体请求头

请求和实体都可以包含。

1，内容相关类

*Content-Type*

*Content-Length*

*Content-Location*

2，缓存相关

多用于响应头部。

*Expire*

*Etag*

*Last-Modified*