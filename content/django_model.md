title: Django Model源码解析（一）
date: 2018-04-08
category: Python
tags: Django, ORM

Django是Python最流行的Web框架，功能强大。虽然学习入门门槛较高，但是后期使用起来，避免了很多不必要的造轮子。
其中ORM是Django最主要的特点之一，它将数据库表定义映射为Python对象，避免了SQL语句的字符串编码，使代码变得清晰且易于维护。
Django的ORM代码，是Python元类编程的很好应用，下面一起看看。
```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=20)
    age = models.SmallIntegerField()
```
上面代码是定义表的基本例子。我们继承`models.Model`对象，`models.Model`对象部分源码如下
```python
class Model(metaclass=ModelBase):

    def __init__(self, *args, **kwargs):
        # Alias some things as locals to avoid repeat global lookups
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED

        pre_init.send(sender=cls, args=args, kwargs=kwargs)

        # Set up the storage for instance state
        self._state = ModelState()

        # There is a rather weird disparity here; if kwargs, it's set, then args
        # overrides it. It should be one or the other; don't duplicate the work
        # The reason for the kwargs check is that standard iterator passes in by
        # args, and instantiation for iteration is 33% faster.
        if len(args) > len(opts.concrete_fields):
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")

        if not kwargs:
            fields_iter = iter(opts.concrete_fields)
            # The ordering of the zip calls matter - zip throws StopIteration
            # when an iter throws it. So if the first iter throws it, the second
            # is *not* consumed. We rely on this, so don't change the order
            # without changing the logic.
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
        else:
            # Slower, kwargs-ready version.  fields_iter = iter(opts.fields)
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
                kwargs.pop(field.name, None)
```
可以看到`Model`的定义使用了元类`ModelBase`。`ModelBase`主要处理表映射的Fields字段，具体怎么处理，后面再具体分析。所谓元类，就是普通类的类，也就是普通类是元类的实例。
可以用`类名.__class__`查看普通类的元类，默认元类是`type`。《流畅的Python》第21章很透彻的分析了元类，下面这幅图是里面的一张插图，很好的表示了元类与普通类的关系。

![Python元类图]({static}/images/meta_class.jpg)

我们回来，继续看`models.Model`源码。
我们看到`__init__`初始化方法第二行`opts=self._meta`。这个`_meta`属性，也是通过元类`ModelBase`附加给`Model`类的。它是一个`options.Options`对象，是管理ORM的核心。
`__init__`方法剩余的代码主要是处理域和值的映射关系，也是依赖`_meta`属性管理。完整的代码这里就不粘贴了。
`Model`对象除了`__init__`方法外，还有负责验证的`clean_fields`, `clean`, `validate_unique`以及负责保存对象到库的`save_base`方法，也都依赖`_meta`属性。
下面是`save_base`的代码，它通过`_meta`处理proxy，parents，auto_created，db_name然后创建或更新数据库表。
```python
    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        """
        Handle the parts of saving which should be done only once per save,
        yet need to be done in raw saves, too. This includes some sanity
        checks and signal sending.

        The 'raw' argument is telling save_base not to save any parent
        models and not to do any changes to the values before save. This
        is used by fixture loading.
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert not (force_insert and (force_update or update_fields))
        assert update_fields is None or update_fields
        cls = origin = self.__class__
        # Skip proxies, but keep the origin as the proxy model.
        if cls._meta.proxy:
            cls = cls._meta.concrete_model
        meta = cls._meta
        if not meta.auto_created:
            pre_save.send(
                sender=origin, instance=self, raw=raw, using=using,
                update_fields=update_fields,
            )
        # A transaction isn't needed if one query is issued.
        if meta.parents:
            context_manager = transaction.atomic(using=using, savepoint=False)
        else:
            context_manager = transaction.mark_for_rollback_on_error(using=using)
        with context_manager:
            parent_inserted = False
            if not raw:
                parent_inserted = self._save_parents(cls, using, update_fields)
            updated = self._save_table(
                raw, cls, force_insert or parent_inserted,
                force_update, using, update_fields,
            )
        # Store the database on which the object was saved
        self._state.db = using
        # Once saved, this is no longer a to-be-added instance.
        self._state.adding = False

        # Signal that the save is complete
        if not meta.auto_created:
            post_save.send(
                sender=origin, instance=self, created=(not updated),
                update_fields=update_fields, raw=raw, using=using,
            )
```
简单看了`model.Model`的源码后，我们接下来简单分析下`ModelBase`代码。
```python
class ModelBase(type):
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        attr_meta = attrs.pop('Meta', None)
        # Pass all attrs without a (Django-specific) contribute_to_class()
        # method to type.__new__() so that they're properly initialized
        # (i.e. __set_name__()).
        contributable_attrs = {}
        for obj_name, obj in list(attrs.items()):
            if _has_contribute_to_class(obj):
                contributable_attrs[obj_name] = obj
            else:
                new_attrs[obj_name] = obj
        new_class = super_new(cls, name, bases, new_attrs, **kwargs)

        abstract = getattr(attr_meta, 'abstract', False)
        meta = attr_meta or getattr(new_class, 'Meta', None)
        base_meta = getattr(new_class, '_meta', None)

        app_label = None

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(module)

        if getattr(meta, 'app_label', None) is None:
            if app_config is None:
                if not abstract:
                    raise RuntimeError(
                        "Model class %s.%s doesn't declare an explicit "
                        "app_label and isn't in an application in "
                        "INSTALLED_APPS." % (module, name)
                    )

            else:
                app_label = app_config.label

        new_class.add_to_class('_meta', Options(meta, app_label))
        if not abstract:
            new_class.add_to_class(
                'DoesNotExist',
                subclass_exception(
                    'DoesNotExist',
                    tuple(
                        x.DoesNotExist for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (ObjectDoesNotExist,),
                    module,
                    attached_to=new_class))
            new_class.add_to_class(
                'MultipleObjectsReturned',
                subclass_exception(
                    'MultipleObjectsReturned',
                    tuple(
                        x.MultipleObjectsReturned for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (MultipleObjectsReturned,),
                    module,
                    attached_to=new_class))
            if base_meta and not base_meta.abstract:
                # Non-abstract child classes inherit some attributes from their
                # non-abstract parent (unless an ABC comes before it in the
                # method resolution order).
                if not hasattr(meta, 'ordering'):
                    new_class._meta.ordering = base_meta.ordering
                if not hasattr(meta, 'get_latest_by'):
                    new_class._meta.get_latest_by = base_meta.get_latest_by

        is_proxy = new_class._meta.proxy
```
首先`ModelBase`继承`type`，所有的元类都继承`type`。接下来`__new__`方法，它才是Python真正的构造函数。由于普通类是元类的实例，当定义`Model`对象时，`ModelBase`的`__new__`方法将被调用。
注意是定义时，而不是调用时。就是类体本身属性和方法的初始化，都会有对应元类的`__new__`方法构建。`__new__`是一个类方法，接受的三个位置参数分别是要创建的类类名，继承的基类对象元组，以及类所属属性的映射。
下面是`__new__`部分代码注释。
```python
# Meta属性会再赋值给__meta
attr_meta = attrs.pop('Meta', None)
# 调用父类的__new__创建类对象，也就是Model对象
new_class = super_new(cls, name, bases, new_attrs, **kwargs)
# 给Model增加_meta属性, 转化成了Options对象
new_class.add_to_class('_meta', Options(meta, app_label))

# 处理抽象父Model对应的域
for base in reversed([new_class] + parents):
    # Conceptually equivalent to `if base is Model`.
    if not hasattr(base, '_meta'):
        continue
    # Skip concrete parent classes.
    if base != new_class and not base._meta.abstract:
        continue
    # Locate OneToOneField instances.
    for field in base._meta.local_fields:
        if isinstance(field, OneToOneField):
            related = resolve_relation(new_class, field.remote_field.model)
            parent_links[make_model_tuple(related)] = field

# 给Model对象追加objects作为manager
if not opts.managers:
    if any(f.name == 'objects' for f in opts.fields):
        raise ValueError(
            "Model %s must specify a custom Manager, because it has a "
            "field named 'objects'." % cls.__name__
        )
    manager = Manager()
    manager.auto_created = True
    cls.add_to_class('objects', manager)
```
可以看到`ModelBase`主要是给`Model`对象追加`_meta`属性及objects manager，并利用`Options`对象校验Model和父Model域定义。`Options`代码这里不再分析，明天写写`Model`的`Field`对象。
