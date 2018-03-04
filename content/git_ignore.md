Title: git .gitignore不起作用的原因
Date: 2016-12-20
category: git
tags: .gitignore

最近自己在折腾一个小项目时，先提交了几次commit，并且推到了上游。可是类似 pyc 这样的文件总是显示在 git status 中，看起来挺不爽的，所以添加了一个 .gitignore 过滤掉 pyc 文件。
但当我写好规则时，却发现 git status 仍然展示 pyc 文件。搜索了下，原来 gitignore 对已经跟踪的文件是没有效果的，我们需要先清空 git index。解决方法如下:
```
git rm -r --cached .
```
这样再看的时候，.gitignore 就生效了，重新提交一次就可以了。
