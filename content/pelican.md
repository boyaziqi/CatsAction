Title: pelican安装与部署
Date: 2015-01-02
category: python
tags: pelican, blog, git page

pelican是python编写的一个静态博客生成系统。如果有一定的python基础，部署起来很方便
#### 1：安装
```shell
virtualenv ~/virtualenvs/pelican
cd ~/virtualenvs/pelican
source bin/activate
pip install pelican
```
也可以通过源码安装：
```shell
git clone https://github.com/getpelican/pelican.git
cd pelican
python setup.py install
```

#### 2：生成博客站点
```shell
pelican-quickstart
```
回车回答相应的问题，就会为你生成一个博客目录和默认的配置文件。现在你已经可以通过reStructuredText和Markdown格式写文章了，使用的是pelican内置的主题。

#### 3：写文章
在content目录下新建文件写自己的文章。我比较喜欢Markdown，下面是一个例子
```md
Title: about me
Date: 2015-01-02
categoty: me
tags: introduction

Here is my personal introduction
```
完成之后保存为md后缀结尾的文件就行了，比如保存为About.md

#### 4：生成博客站点
```shell
cd you-blog-path
pelican content/ -s pelicanconf.py
```
content是文章所在目录，-s指定配置文件，不指定默认就为pelicanconf.py。也可以通过make生成：
```shell
make html
```
`pelican-quickstart`已经为我们生成所需的Makefile文件，可以make help查看相关命令帮助

#### 5：预览博客文章
```shell
cd output
python -m http.server
```
output是第四步生成站点的默认目录，打开浏览器输入http://localhost:8000/就可以预览了。为了方便调试，可以通过自带脚本启动服务器预览：
```shell
./develop_server.sh
```
通过这个脚本启动，当你更新文章时，它会自动重新生成站点并加载。

#### 6: 部署到github page
现在我们可以把生成的站点部署到github page或者结合Nginx部署到公有云。下面讲讲部署到github page   
> 
(1)  在github上创建自己的user page。比如我的是boyaziqi.github.io。    
(2)  `ghp-import output` 生成gh-pages分支。如果没有ghp-import命令，需要通过pip安装。  
(3)  将ph-pages分支推送到自己的user page远端源：
```shell
git remote add user-page git@github.com:elemoine/elemoine.github.io.git
git push user-page gh-pages:master
```
