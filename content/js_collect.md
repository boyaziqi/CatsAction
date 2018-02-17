Title:  js问题汇总
Date: 2018-01-13
Modified: 2018-01-13
category: js
tags: 前端, 事件, 历史记录

#### 问题-：浏览器回退到上一个页面，表单里输入的内容无法记录。
> 描述：最近在使用bootstrap的过程中，发现某个页面浏览器历史记录返回，无法记录表单里的输入内容，选中的复选框又恢复到初始状态。
>
> 解决：在某次偶然的机会，看到该页面禁用了表单autocomplete功能(大部分浏览器都是打开的)。去掉就好了。

<br/>
#### 问题二：bootstrap模态框确认按钮向后端发送多次请求。
> 描述：当同一个模态框有多个触发源，弹出多次时，最后点击确认按钮，对应的事件处理函数会被调用多次。
> 
> 解决: 绑定事件处理函数之前，先调用jquery off方法解绑先前绑定的事件处理函数。我先前用unbind方法效果不明显。

<br/>
#### 问题三：