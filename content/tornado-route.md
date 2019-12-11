Title: tornado路由装饰器
Date: 2016-08-17
Modified: 2017-04-17 14:11
category: python
tags: tornado, url路由

我们知道，tornado启动时通过Application类加载handler，并实现handler的对应关系，即所谓URL路由。
下面是[tornado入门里的一个简单示例](http://demo.pythoner.com/itt2zh/ch1.html#ch1-1-1)
```python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
```
这样写的缺点是：每次增加handler，都得在Application里增加hanlder和url的映射关系，如果项目很大，管理起来十分不便。
而且不符合软件工程高内聚低耦合的要求。下面装饰器将handler对应的url封装到handler类属性里，那么在主函数就可以写相应的代码自动加载路由了。
```python
import inspect

def route(pattern, priority=0, override=False):
    """ 装饰 Handler 用于 URL 路由，被装饰的 Handler 将在启动时装载

    可以用 priority 指定优先级

    override 用于覆盖掉之前的 route (用于继承复用某个 handler)
    """
    def wrapper(handler):
        if not inspect.isclass(handler) or\
                not issubclass(handler, RequestHandler):
            raise ValueError("Handler must be a subclass of"
                             " tornado.web.RequestHandler")
        if hasattr(handler, "__routes__") and not override:
            handler.__routes__.append((pattern, priority))
        else:
            handler.__routes__ = [(pattern, priority)]
        return handler
    return wrapper
```
