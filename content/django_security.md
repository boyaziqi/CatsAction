title: 常见网络安全
subtitle: 之Django支持
date: 2019-03-11
category: 网络安全
tags: Django, Python, Http

#### 常见网络安全
###### 跨站脚本攻击（XSS）
Cross-Site Scripting（跨站脚本攻击）简称 XSS，是一种代码注入攻击。攻击者通过在目标网站上注入恶意脚本，使之在用户的浏览器上运行。利用这些恶意脚本，攻击者可获取用户的敏感信息如 Cookie、SessionID 等，进而危害数据安全。

```html
<input type="text" value="<%= getParameter("keyword") %>">
<button>搜索</button>
<div>
  您搜索的关键词是：<%= getParameter("keyword") %>
</div>
```
如上的代码，如果输入的url是`http://xxx/search?keyword="><script>alert('XSS');</script>
`将执行js脚本，浏览器将抛出**XSS**对话框。详细介绍和前端一些解决思路，可以查看美团技术团队的文章[前端安全系列（一）：如何防止XSS攻击？](https://www.cnblogs.com/meituantech/p/9718677.html)

###### 跨站请求伪造（CSRF）
CSRF（Cross-site request forgery）跨站请求伪造：攻击者诱导受害者进入第三方网站，在第三方网站中，向被攻击网站发送跨站请求。利用受害者在被攻击网站已经获取的注册凭证，绕过后台的用户验证，达到冒充用户对被攻击的网站执行某项操作的目的。

一个典型的CSRF攻击有着如下的流程：

- 受害者登录a.com，并保留了登录凭证（Cookie）。
- 攻击者引诱受害者访问了b.com。
- b.com 向 a.com 发送了一个请求：a.com/act=xx。浏览器会默认携带- a.com的Cookie。
- a.com接收到请求后，对请求进行验证，并确认是受害者的凭证，误以为是受害者自己发送的请求。
- a.com以受害者的名义执行了act=xx。
- 攻击完成，攻击者在受害者不知情的情况下，冒充受害者，让a.com执行了自己定义的操作

关注CSRF的详细介绍，参考美团技术团队文章[前端安全系列之二：如何防止CSRF攻击？](https://www.cnblogs.com/meituantech/p/9777222.html)

对于CSRF的预防，可以禁止跨域访问，或者追加一个Token（AES/CBC/PKCS5Padding 模式加密用户id，时间戳和一个随机字符串生成）

###### SQL注入
SQL注入是攻击者利用网站漏铜，输入特殊的SQL字符从而，从而执行数据库达到获取敏感信息或破坏数据库的目的。具体的SQL注入，可参考[SQL注入演练](https://www.oschina.net/translate/sql-injection-walkthrought)

###### 点击劫持
点击劫持是指在一个Web页面下隐藏了一个透明的iframe（opacity：0），用外层假页面诱导用户点击，实际上是在隐藏的frame上触发了点击事件进行一些用户不知情的操作。详情请看[浅析解析劫持攻击](https://www.freebuf.com/articles/web/67843.html)

#### Django解决方案
###### XSS
Django模板提供了自动对用户输入的转义。

###### XSRF
Django利用附加随机Token解决，Django模板引擎可以通过csrf_token打卡。

###### HTTPS支持
设置`SECURE_SSL_REDIRECT¶`等于`True`打卡对HTTPS的支持。。

详情查看[Django 安全](https://docs.djangoproject.com/en/3.0/topics/security/)

