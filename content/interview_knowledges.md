title: 面试知识点回答整理
subtitle: 分布式部署
date: 2017-01-22
status: draft
category: interview
tags: hash,cache

#### 一致性哈希
一致性Hash算法将整个哈希值空间组织成一个虚拟的圆环，如假设某哈希函数H的值空间为0-2^32-1。首先将服务器hash（通过ip或主机名)
映射到Hash环上。定位数据资源的时候，将数据key用相同的hash方法算出hash值，并找到key在hash环上的位置。顺时针查找，遇到的第一台服务器即为
数据定位的服务器。一致性hash有很好的扩展性和容错性，即增加和减少一台服务器时，影响的只是对应区段的数据映射。不过一致性hash也会造成数据倾斜（数据节点太少且分布不均）。
可以通过增加虚拟节点和

#### IO复用
IO复用也是一种阻塞式调用，不过它阻塞于多个描述符，即可以同时等待多个描述符就位。只要其中之一满足条件，调用就返回。<br>
常见的IO复用类型有select，poll和epoll。
###### *区别*
- select和epoll最大连接数限制为1024（32位）和2048（64位）。
- select和epoll采用轮询方式查看就绪的sockets。
- epoll内存拷贝次数少。select和poll每次都需要将用户态拷贝到内核空间，epoll却只需要一次。

#### 阻塞，非阻塞，异步，同步

#### 360电话面试问题

#### HTTP常用头
###### *Request Headers*
- Accept：text/html
- Accept-encoding: gzip
- Accept-Language: en-US
- Cache-control: max-age=0
- Cookie
- Refer：https://www.baidu.com/xxxxxxxxxx
- User-agent：Mozilla/5.0 

###### *Resonse Headers*
- Accpet-ranges：bytes
- Content-length：24211
- Content-type：text/html
- Content-encoding：br
- Age：1037016
- Date：Thu, 15 Feb 2018 20:31:45 GMT
- Expires：Fri, 01 Feb 2019 17:33:57 GMT
- Last-modified：Mon, 12 Dec 2016 14:45:00 GMT
- Vary：Accept-Encoding
- Server: gws
- Set-cookie:
- X-frame-options: SAMEORIGIN
- X-xss-protection：1; mode=block
- Etag：

#### CSRF
CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。
你这可以这么理解CSRF攻击：攻击者盗用了你的身份，以你的名义发送恶意请求。下面是防止方法。
- 生成一个随机数
- 每次请求时要求输入验证码 

#### XSS

#### 进程，线程，协成

#### Docker entry CMD区别