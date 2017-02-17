"""
Descriptors allow you to define an object that can behave in the same
way as a property on any class to which it's assigned.

Properties are implemented as descriptors behind the scenes. So are methods.
They work by implementing any of the three possible methods, getting, setting
and deleting.

`__get__()` manages retrieval of attribute values, but unlike a property,
a descriptor can manage attribute access on both the class and its instances.
`__get__()` receives both the object instance and its owner class as arguments.
If the descriptor is accessed directly on a class instead of an instance,
the instance argument will be None.

`__set__()` manages setting a value on the attribute managed by the descriptor.
Unlike __get__, __set__ only works on instance objects.
"""

import datetime


class CurrentTime:
    """
    Simple descriptor using only the __get__ method to  always provide
    an up to date value when requested.

    >>> Example.time
    datetime.datetime(2017, 2, 14, 23, 33, 26, 876065)
    >>> Example().time
    datetime.datetime(2017, 2, 14, 23, 33, 32, 955559)
    >>>
    """
    def __get__(self, instance, owner):
        return datetime.datetime.now()


class ExampleCurrentTime:
    time = CurrentTime()


class LoggedAttribute:
    """
    Simple descriptor that behaves like an attribute but logs
    every time its value is changed.
    """
    def __init__(self):
        self.log = []
        self.value_map = {}

    def __set__(self, instance, value):
        self.value_map[instance] = value
        log_value = (datetime.datetime.now(), instance, value)
        self.log.append(log_value)

    def __get__(self, instance, owner):
        if not instance:
            return self  # This way, the log is accessible
        return self.value_map[instance]


class ExampleLoggedAttribute:
    """
    >>> e = ExampleLoggedAttribute()
    >>> e.value = 'testing'
    >>> e.value
    'testing'
    >>> ExampleLoggedAttribute.value.log
    [(datetime.datetime(2017, 2, 14, 23, 44, 8, 451457), <descriptors.ExampleLoggedAttribute object at 0
    x...>, 'testing')]
    >>>
    """
    value = LoggedAttribute()
