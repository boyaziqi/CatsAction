title: 面试知识点回答整理2
subtitle: 分布式部署
date: 2017-01-22
status: draft
category: interview
tags: hash,cache

#### Python CI知识
工具有Jenkins，buildbot，Travis，Tox。我们选择了Buildbot，是因为它是Python开发的，而且开源。
Travis CI对闭源软件不免费。后续写一篇利用buildbot+tox实现自动化测试及CI的文章。

#### Python 测试包
pytest，unitest，mock, nose, doctest, tox

#### Python2和Python3的区别
- string编码。Python3默认是Unicode，Python2是ASCII。
- Python没有xrange，只有range。
- 字典keys，views，iterms返回迭代器。
- Python3类都是新式类。
- 标准库有变化。

#### Redis持久化
有两种方式：快照（RDB文件）和追加写记录（AOF文件）

#### protobuf知识
- 类型：message，service
- 数据类型：string，int，enum，float，bool，byte。
- 修饰符：required，optional，repeated。

#### IO模型
select，poll，epoll

#### 短连接的实现方式（腾讯面试题）

#### Django设计思想
观察者模式，也叫发布订阅模式。Django的信号就是。

#### 选择Django的原因
- 功能完善，要素齐全。自带模板引擎和管理后台。
- 对数据库支持全面和完善的ORM。
- 自带缓存模块。
- 完善的用户认证和可扩展。
- 灵活的Middleware。
- 文档齐全，社区生态好。

#### 如何测试数据库
创建一个临时数据库表，测试完成后删除。

#### 针对数据中心重构了哪些代码
- 增加了一张缓存表。
- 封装了一些共用SDK，如上游调用的一些工具, 共同的结算。
- 拆分代码为几大功能模块。

#### 微服务之间如何通信
- RPC
- 进程间通信（消息队列）
- HTTP

#### 为什么选择了RPC及gRPC？
- 对输入和输出校验，集成了认证
- 写起来清晰，像调用本地的方法。
- 开发即文档，不需要再写单独的文档接口。

#### 选择gRPC而不是Thrift的理由
gRPC文档更完善，而且Protobuf语法友好。

#### 项目中遇到的困难、挑战和解决方法
- 统计数据库的问题
- too many open file（ulimit -n 65535调整最大文件限制数）。官方bug，线程池创建回收竞态。
- 服务拆分问题

#### 想找一份什么样的工作
- 云平台开发的工作
- 底层的开发，而不是纯面向业务
- 哈哈