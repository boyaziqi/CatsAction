title: RPC知识和常见框架对比
date: 2018-08-10
category: RPC
tags: gRPC, Thirft, Dubbo, Netty

## 前述

本篇先讲解RPC的基本概念和简单原理，然后对比常见的RPC框架。本篇知识点都是简单罗列，有些直接摘抄至官网，后期会针对比如HTTP2，gRPC等知识点深入写相应的章节。

## 什么是RPC

RPC，即远程过程调用。它的目的是让调用远程服务向调用本地服务一样，屏蔽传输方式，序列化方式和通信细节。

关于RPC，参考[RPC架构简单详解](https://blog.csdn.net/u013521220/article/details/66530188)和[RPC框架选择](https://www.jianshu.com/p/b0343bfd216e)

一个典型的RPC框架，需要解决如下通电。

1）call id映射。调用方如何把需要调用的方法名告诉远程服务。

2）序列号和反序列化。调用的方法参数，如何传输到远程服务。

3）如何传输。如何将call id和序列化的参数传送到远程服务。

不同的RPC框架对上面三点的解决方法不同，不过对于第一点，无外乎都是维护一个方法名的映射，因此区别主要第二点和第三点。下面讲常用RPC框架会具体谈到。

## 常见RPC框架 

常见的RPC框架包括bRPC，Dubbo，Thrift，gRPC，JSON-RPC，下面主要介绍Thrift、gRPC、Dubbo。

##### Thirft

[Thirft原理和使用](https://www.cnblogs.com/chenny7/p/4224720.html)

[Apache Thrift](https://www.ibm.com/developerworks/cn/java/j-lo-apachethrift/index.html)

Thirft传输层支持多种协议，支持文本和二进制传输。服务端支持多种模型（单线程，多线程，阻塞和非阻塞）。

##### gRPC

对于gRPC，它使用的传输协议是HTTP2，序列化和反序列化协议是protobuf。gRPC有一下特点。

- 支持流式链接（不是TCP流，指数据流，比如一次请求发送多个包）。服务端端和客户端都支持面向流的数据。这是HTTP2特性决定的。

- 支持同步和异步。

- 支持截止时间超时机制。  

- 支持流控。

- 支持AUTH2和SSL等多种安全认证机制。

这里简单列举gRPC知识，后期单独写相应的章节。

参考[深入了解gRPC](https://zhuanlan.zhihu.com/p/27595419)

[Protobuf 语法指南](https://colobu.com/2015/01/07/Protobuf-language-guide/#%E5%8C%85%EF%BC%88Package%EF%BC%89)

[gRPC中文官方文档](http://doc.oschina.net/grpc?t=60133)


##### Dubbo

Dubbo是阿里开源的RPC框架。

[Dubbo官方文档](http://dubbo.apache.org/zh-cn/docs/user/preface/background.html)

##### HTTP2

HTTP2是二进制协议，支持流控，支持数据流等特性。

[http2](https://hpbn.co/http2/)

[http2详解](https://juejin.im/post/5b88a4f56fb9a01a0b31a67e#heading-61)

## gRPC VS Thirft

[gRPC vs Thrift](https://blog.csdn.net/dazheng/article/details/48830511)

## 后述

本篇简单罗列了RPC概念和常见的RPC框架，后期会针对某些知识点深入写相应文章。