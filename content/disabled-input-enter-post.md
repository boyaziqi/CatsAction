Title: 禁止input输入框回车自动提交表单
Date: 2015-05-01
Modified: 2017-04-10 11:17
category: js
tags: form, js, HTML5

最近在做项目的时候，发现一个小bug。input输入框回车直接提交表单，导致页面直接展示后端返回的json数据，而未执行相应的js跳转页面。
```json
{"code": 200, "data": {"xxxxx": "xxxxxxx", "yyyyyyy": "yyyyyyyy"}, "success": "true"}
```
解决方法是为keydown事件指定返回值。如下：
```html
<form name="vehicle-selection" action="/selection" method="POST" onkeydown="if(event.keyCode==13){return false}">
    <input type="text" name="nature" value="211">
......
</form>
```
通过keyCode==13判断是否回车键
