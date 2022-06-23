copy_enum_members
=================

The :func:`~extendableenum.copy_enum_members` class decorator is used to loosely inherit from an existing ``Enum``. The defined members in the `base` class(es) will be copied to the `derived` class, creating a completely distinct ``Enum``, but allowing reuse of already defined member names/values.

Decorating a Class with copy_enum_members
-----------------------------------------

The `copy_enum_member` decorator can only be applied to classes with the ``EnumMeta`` metaclass. The decorator takes a variable number of arguments, each of which must be an ``Enum``, otherwise a ``TypeError`` will be raised. The `derived` class can also define new members:

.. code-block:: python

    from enum import Enum
    from extendableenum import copy_enum_members

    class Fruits(Enum):
    APPLE = 1
    BANANA = 2
    PEAR = 3

    class Vegetables(Enum):
        ASPARAGUS = 11
        BROCCOLI = 12
        CARROT = 13

    @copy_enum_members(Fruits, Vegetables)
    class MyFavoriteFoods(Enum):
        BEEF = 21
        CHICKEN = 22
        PORK = 23

    MyFavoriteFoods.APPLE
    MyFavoriteFoods.BROCCOLI is not Vegetables.BROCCOLI

::

    >>> MyFavoriteFoods.APPLE
    >>> True

.. note::
    It is the user's responsibility to ensure that names of the copied members do not conflict, otherwise a ``TypeError`` will be raised.

.. note::
    If a duplicated member has the same value as a previously defined member, the member will become an alias in the new ``Enum``. Priority is based on the order of the arguments supplied to the decorator function. Members defined in the new ``Enum`` have the lowest priority.

The __copied_from__ Attribute
-----------------------------

The `copy_enum_members` decorator adds the `__copied_from__` attribute to the decorated ``Enum``, which is simply the arguments that were passed to the decorator.

.. code-block:: python

    MyFavoriteFoods.__copied_from__

::

    >>> (<enum 'Fruits'>, <enum 'Vegetables'>)

