Title: vim 选项iskeyword
Date: 2017-06-23
category: vim
tags: vim选项

之前在用ctags来辅助跳转到 python 定义处时，我已经生成相应的tags文件，可是在类似self.method_name的语句按`<C-T>`时却不能正常跳转。查看
tags文件里也有对应的tag，网上搜索了好久也未找寻到解决方法。一个偶然的机会，发现iskeyword选项，它很好的解决了我的烦恼。

iskeyword 设置作为单词整体的字符，可能是升级到vim8.0的原因，"."字符被当做单词的一部分，所以`viw`等操作时都会选中点，`<C-T>`也不能正常识别，所以我做了如下修改

```shell
set iskeyword -= .
```
这样就好了，可以使用
```
set iskeyword?
```
查看当前值
