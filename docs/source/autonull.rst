auto_null_enum
==============

The :func:`~extendableenum.auto_null_member` class decorator is used to automatically add the null member to an ``Enum``.

The Null Member
---------------

The null member is intended to be a sentinel value for the ``Enum``. On creation, the null member is created from the module level configuration, which can be changed with calls to :func:`~extendableenum.set_auto_null`. The name and value used by the class are stored internally in the class itself, so calls to `set_auto_null` will not impact any classes already created. The default name and value are ```Null``` and ``None`` respectively:

.. code-block:: python

    from enum import Enum
    from extendableenum import set_auto_null, auto_null_member
    
    @auto_null_member
    class Defualt(Enum):
        pass
        
    set_auto_null('CUSTOM', 'Null')
    
    @auto_null_member
    class Custom(Enum):
        pass
        
    Default.__members__
    Custom.__members__

::    

    >>> {'NULL': <Defualt.NULL: None>}
    >>> {'CUSTOM: <Custom.CUSTOM: 'Null'>}

Decorating Classes with auto_null_member
----------------------------------------

The `auto_null_member` decorator can only be applied to classes with the ``EnumMeta`` metaclass. Applying the decorator to any other class will raise a ``TypeError``.

If the decorated class does not define any members, it is considered a mixin class and  the :func:`~extendableenum.inheritable_enum` decorator is automatically applied:

.. code-block:: python
    
    Default.__inheritable_members__

::    

    >>> ['NULL']
    
Otherwise, it is simply considered a normal ``Enum`` with the null member. If automatically added, the null member will always be inserted as the first member:

.. code-block:: python

    set_auto_null('NULL', None)
    
    @auto_null_member
    class Directions(Enum):
        NORTH = 0
        SOUTH = 1
        DENNIS = 2

    Directions.__members__

::    

    >>> {'NULL': <Directions.NULL: None>, 'NORTH': <Directions.NORTH: 0>, 'SOUTH': <Directions.SOUTH: 1>, 'DENNIS': <Directions.DENNIS: 2>}
    
If you want to be verbose (and possibly to silence annoying IDE warnings), you may manually define the null member as long as the value assigned matches the module configuration. This can also be used to change the ordering of the null member:

.. code-block:: python

    @auto_null_member   # Decorator has no effect in this case
    class SameDirections(Enum):
        NORTH = 0
        SOUTH = 1
        NULL = None
        DENNIS = 2
        
    SameDirections.__members__

::    

    >>> {'NORTH': <SameDirections.NORTH: 0>, 'SOUTH': <SameDirections.SOUTH: 1>, 'NULL': <SameDirections.NULL: None>, 'DENNIS': <SameDirections.DENNIS: 2>}
        
You can also create an alias for the null member using the configured value:

.. code-block:: python

    @auto_null_member
    class NullAlias(Enum):
        NULL_ALIAS = None
        
    NullAlias.NULL_ALIAS is NullAlias.NULL

::    

    >>> True
    
You cannot, however, redefine the null member with a new value, as this will raise a ValueError:

.. code-block:: python

    try:
        @auto_null_member
        class RedefineNull(Enum):
            A = 1
            NULL = 2
    except ValueError:
        print('Cannot redefine the null member')

::    

    >>> Cannot redefine the null member

OrderedEnums and the Null Member
---------------------------------

If you have an `OrderedEnum <https://docs.python.org/3/library/enum.html#orderedenum>`_:

.. code-block:: python

    @auto_null_member
    class NullGrade(OrderedEnum):
        A = 5
        B = 4
        C = 3
        D = 2
        F = 1
        
the `auto_null_member` decorator will automatically adjust any of the comparison functions (ie: ``__le__``, ``__lt__``, ``__ge__`` and ``__gt__``) defined in the class to consider the null member. In cases where neither value in the comparison are the null member, or if they are of different classes, comparison is deferred to the originally defined functions . Otherwise, the null member will always compare as less than a valid member. 

.. note::
    If the first value in the comparison is the null member, the second value is treated as a valid member, even if it is also the null member:

.. code-block:: python

    NullGrade.NULL < NullGrade.A
    NullGrade.NULL <= NullGrade.B
    NullGrade.NULL > NullGrade.C
    NullGrade.NULL >= NullGrade.C
    NullGrade.NULL < NullGrade.NULL
    NullGrade.NULL <= NullGrade.NULL
    NullGrade.NULL > NullGrade.NULL
    NullGrade.NULL >= NullGrade.NULL

::    

    >>> True
    >>> True
    >>> False
    >>> False
    >>> True
    >>> True
    >>> False
    >>> False

AutoNullEnum
------------

:class:`~extendableenum.AutoNullEnum` is a base mixin class for null member ``Enum`` s. A custom base class can easily be created, as seen in :ref:`this example<Create a Custom Base Class for Auto Null Enums>`. Since `AutoNullEnum` does not define any members other than the null member, it is inheritable:

.. code-block:: python

    class AutoNullDerived(AutoNullEnum):
        A = 1
        B = 2
        
    AutoNullDerived.auto_null_member()
    bool(AutoNullDerived.A)
    bool(AutoNullDerived.auto_null_member())

::    

    >>> AutoNullEnum.NULL
    >>> True
    >>> False


Decorated and Undecorated Subclasses
------------------------------------

When subclassing an `auto_null_member` decorated class, the subclass may or may be decorated as well. If decorated, the subclass will have access to both the base class null member as well as it's own distinct null member:

.. code-block:: python

    @auto_null_member
    class Decorated(AutoNullEnum):
        A = 1
        B = 2

    class Undecorated(AutoNullEnum):
        A = 1
        B = 2
        
    Decorated.auto_null_member()
    Undecorated.auto_null_member()
    super(Decorated, Decorated).NULL

::    

    >>> Decorated.NULL
    >>> AutoNullEnum.NULL
    >>> AutoNullEnum.NULL
