title: 关于TCP的一些问题
date: 2017-01-12
category: 网络
tags: TCP

##### TCP如何记录时间戳

TCP首部（不是头部）有一个选项字段。kind = 10时表示时间戳。此选项总共10字节。len表示的总长，包括kind和len本身。

<center>![mysql_innodb_myisam_index]({static}/images/tcp_timestamp.jpg)</center>

“时间戳值”表示当前系统的时间戳，“时间戳回显应答”是需要确认的数据报对端的发送的时间戳，回传给对端计算数据报传送花费时间。

##### TCP三次握手超时重传次数

这个又系统自己实现决定。Unix默认是5次，可以通过修改TCP_SYNACK_RETRIES改变。

##### 如何保证TCP的高并发

对于Linux，每次有链接进来时，会新开一个线程（当然可以是进程，但是没必要）。此外，Linux有一个呼入连接请求队列，当应用层来不及处理相应的链接，如果队列还有空间，Linux将同意建立链接，并把它加入请求队列。

##### RST包作用

- 正常关闭一个连接使用FIN包，RST包可以用来异常关闭一个连接。收到RST一方将终止改连接，并通知应用层连接复位（不需要给对端任何响应）。
- 连接到一个不存在的端口，也会收到RST报文。比如主动断开连接一段没有等待2MSL时间，被动关闭的一端重传FIN就会收到RST连接。（次数端口不存在）。
- 检测半打开连接。如果服务端异常挂掉，重启后会给客户端回送RST报文，客户端能知道连接也被服务端断开，处于半连接状态。

##### 半打开连接和半关闭连接的区别

半打开连接指主动大开端收到被动打开端的ACK确认，而对方还没收到自己ACK确认，此时给对端直接发送数据，会被丢掉。      

半关闭连接指一方发送FIN并收到了ACK，此时表示自己不再发送数据，但是还是可以正常对端发送过来的数据。