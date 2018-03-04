Title: pycurl安装的问题
Date: 2017-12-24 17:02
category: python
tags: pycurl, macos


最近在安装pycurl的时候, `pip install pycurl`显示已经成功安装，不过在导入的时候去出现如下错误
```python
In [1]: import pycurl
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-1-141165d68a5f> in <module>()
----> 1 import pycurl

ImportError: pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (none/other)

In [2]:
```

这个原因是pycurl需要知道ssl是哪一个具体的库， [stackoverflow](https://stackoverflow.com/questions/21096436/ssl-backend-error-when-using-openssl)上有很详细的讨论，我试了其中很多人的回答，只有下面这种方式对我的环境有效

```shell
pip uninstall pycurl
export PYCURL_SSL_LIBRARY=openssl

# --no-cache-dir --compile 不能省
pip install pycurl --compile pycurl --no-cache-dir
```

不过这样只是解决了全局环境下，对虚拟环境还是不行。暂时我没找到根本的解决方法，只能采取下面比较暴力的方式

```shell
cp /usr/local/Cellar/python3/3.6.4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pycurl.cpython-36m-darwin.so .tox/py36/lib/site-packages
```
如果大家有更好的解决方式，欢迎在https://github.com/boyaziqi/CatsAction/issues 给我提issue
