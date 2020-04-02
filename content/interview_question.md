title: 面试问题整理
subtitle: 分布式部署
date: 2017-01-22
status: draft
category: interview
tags: hash,cache

1. HTTP, HTTPS, TCP原理和工作过程，要求掌握细节。
2. epoll, poll, select的区别。epoll的详细工作机制。
3. MySQL主从，集群原理。MySQL存储引擎，索引，锁，优化（越深入越好）。
4. Redis数据结构，主从复制，哨兵，集群原理（需要深入了解机制和Redis数据结构底层实现）。
5. 操作系统线程和进程的区别。
6. 算法和数据结构：B+树，链表，二分查找，快速排序。

7. 医美云项目

#### 如何防止重放击

1， 时间戳+口令key+请求内容摘要

HMAC(key+timastamp+request_content)

问题：这种情况，timestamp和request_content是暴露的，加上大部分API用的都是常见的摘要算法（MD5，SHA256），黑客只需要破解key就可以攻破。

2, 基于非对称签名

sign(请求摘要+key+timestamp)

这种情况用户需要非对称的加密的私钥和key才能复制。缺点是非对称秘钥管理困难，而且相对比较慢。

如果需要觉得禁止重复，需要存储上一次请求时间戳或者随机key，然后对比。

如果怕数据泄露，可以采用AES-CBC模式加密。

#### API接口校验和签名设计

基于token认证，实现权限筛选。(oAuth2)

#### 安全层面设计
