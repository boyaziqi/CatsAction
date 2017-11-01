Title: zsh打开vi模式up向上箭头不能按子模式搜索解决方法
Date: 2017-10-29 00:15:15
category: :Linux
tags: zsh, oh-my-zsh, history-substring-search

由于我习惯在终端下用vim下写代码，因此最近把zsh的模式也改成了vi模式，这样就可以在终端
里使用很多vi快捷键。但是却发现一个问题：<br>

 *按方向键的上下键，zsh不能根据输入的字符匹配最近输入的历史命令*

 在网上搜索了下，记录如下
 ```bash
 plugins=(... vi-mode history-substring-search ...)
# not with
plugins=(... history-substring-search vi-mode ...)
```
具体就是history-substring-search插件需要放在vi-mode插件前面，请参考[here](https://github.com/robbyrussell/oh-my-zsh/issues/2735)
