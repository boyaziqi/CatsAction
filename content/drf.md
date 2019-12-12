title: Django REST Framework使用
date: 2017-01-08
status: hidden
category: python
tags: Django

使用DJANGO开发REST接口的时候，通常我们都会使用Django REST Framework（下面简称DRF )。

#### DRF特点
- 集成swagger，开发者通过浏览器可视化请求并验证API
- 对Django ORM序列化和反序列化支持很好
- 认证支持OAuth1和OAuth2
- view支持很强大，继承`GenericViewSet`类再搭配一些混合内，简单的逻辑几乎不需要在额外写代码
- 丰富的第三方组件和良好的社区支持

一个简单的DRF例子
```python3
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```
其实这样的写法,和Django一样的思想，对开发者都是配置大于约定。