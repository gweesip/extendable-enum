post_mixin_enum
===============

The :func:`~extendableenum.post_mixin_enum` class decorator is used to add a new base class to an existing ``Enum``:

.. code-block:: python

    from enum import Enum
    from extendableenum import post_mixin_enum
    
    class Animal(Enum):
        ANT = 1
        BEE = 2
        CAT = 3
        DOG = 4
        
    @post_mixin_enum(Animal)
    class SpeakMixin:
        def speak(self):
            if self is Animal.ANT:
                return ''
            elif self is Animal.BEE:
                return 'buzz buzz'
            elif self is Animal.CAT:
                return 'Meow'
            elif self is Animal.DOG:
                return 'Woof'
            else:
                return '???'
                
    Animal.__bases__
    isinstance(Animal.ANT, SpeakMixin)
    Animal.BEE.speak()

::

    >>> (<class '__main__.SpeakMixin'>, <enum 'Enum'>)
    >>> True
    >>> buzz buzz

.. note::
    The mixin class can subclass ``Enum``, however, it cannot not define any members, as extending an enum with the `post_mixin_enum` is not supported. Doing so will raise a ``TypeError``. This can be bypassed if the mixin ``Enum`` is :ref:`inheritable <inheritable_enum>`.
