title: Redis在项目中的使用
date: 2018-01-10
status: draft
category: Redis
tags: Redis, Golang

## 实现关注列表

#### 一. 需求描述
一个医美小程序，需要在我的页面，展示关注的医生、医院、项目信息。

#### 二：解决方案
可以将关注医生ID信息存储在Redis列表，但是不能获取关注时间。所以可以通过Redis有序集合存储，用户ID作为