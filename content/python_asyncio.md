title: Python异步编程详解
date: 2017-08-04
category: Python
tags: 异步编程, 协程, Epoll, asyncio, 协程

## 前述

本篇会先讲解异步编程的实现方式，然后讲解操作系统的多路复用机制。最好讲讲Python对异步编程的支持和最新的Python协程方案。

本篇假设你已经理解下面的概念：

- 阻塞、非阻塞

- 同步、异步的概念。

- 并行和并发

- 进程和线程

## 异步编程

要实现异步编程，除了多进程和多线程，我们还可以基于操作系统的多路复用机制。

异步编程最大的困难：异步任务何时执行完毕？接下来要对异步调用的返回结果做什么操作？

上面的问题可以通过**事件循环 + 回调**方式解决。

回调会有一个回调地狱的问题。

除了回调地狱的问题，回调最大的问题是栈撕裂和状态管理困难。

那为了解决回调的问题，协程就产生了。协程底层其实还是事件和回调，只不过做了一定的封装，让用户可以用写同步代码的方式写异步代码。

## 协程

回调有状态管理的问题，那如果程序（例程）知道自己干了什么，正在干什么，将来干什么呢？换言之，程序得知道当前所处的状态，而且要将这个状态在不同的回调之间延续下去。

上面的问题，就引出协程实现核心思想，它得自己维护自己状态，而且可以通知其他协程。

**协程，即协作式的例程。**

它是非抢占式的多任务子例程的概括，可以允许有多个入口点在例程中确定的位置来控制程序的暂停与恢复执行。

例程是什么？编程语言定义的可被调用的代码段，为了完成某个特定功能而封装在一起的一系列指令。一般编程语言都用函数或方法来体现。

## EPoll
操作系统支持多路复用。所谓多路复用，就是同时监听很多文件描述符，只要其中某个文件描述符状态改变就给予通知。多路复用的好处就是一次等待多个时间就绪，合理利用CPU性能。

常用的多路复用机制有`Select`、`Poll`、`EPoll`。

##### Select

```C
int select (int n, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
```

select调用会阻塞，某个文件描述符就绪或者超时才返回。select由于每次都需要将文件描述符拷贝到内核空间遍历一遍，所以性能不高。而且支持的文件描述符数量有限制（通常是1024）。

##### Poll

```C
int poll (struct pollfd *fds, unsigned int nfds, int timeout);
```
poll和select差不多，只是文件描述符实现不同。虽然poll没有文件描述符数量的限制，但是数量太多仍然有select一样的性能问题。

##### EPoll

```C
int epoll_create(int size)；//创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；
int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);
```
epoll有三个函数，它等待的函数是`epoll_wait`，而注册监听描述符的是`epoll_ctl`，因此避免了重复将文件描述符拷贝到内核空间。epoll也没有文件限制。

epoll优点：

1）避免了每次等待调用都将文件描述符拷贝到内核空间，只需要拷贝一次。

2）当文件描述符就绪时，会被加入相应的事件等待队列，wait函数只需扫描对应事件的文件描述符，避免了像select一样每次都扫描所有的文件描述符。

3）没有文件描述符数量限制。

参考资料：

[Linux多了复用区别](https://www.cnblogs.com/anker/p/3265058.html)

[Linux多路复用](https://segmentfault.com/a/1190000003063859)

## 后述

*参考[深入理解Python异步编程（上）](https://mp.weixin.qq.com/s/GgamzHPyZuSg45LoJKsofA?)*