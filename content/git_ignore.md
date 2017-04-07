Title: git .gitignore不起作用的原因
Date: 2014-12-25
category: git
tags: git

最近在做一个个人系统测试小项目时，先提交了几次commit，并且推到了上游。可是类似pyc这样的文件总是显示在git status中，看起来挺不爽的，所有测试用.gitignore解决。但当我写好规则时，却发现git status仍然展示pyc文件。搜索了下，原来gitignore对已经跟踪的文件是没有效果的，我们需要先清空git index。解决方法如下:
```
git rm -r --cached .
```
这样再看的时候，.gitignore就生效了，重新提交一次就可以了。
