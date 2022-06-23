inheritable_enum
================

The :func:`~extendableenum.inheritable_enum` class decorator is used to make an ``Enum`` and all its members inheritable.

Decorating a Class with inheritable_enum
----------------------------------------
The `inheritable_enum` class decorator can only be applied to classes with the ``EnumMeta`` metaclass. Any other class will raise a ``TypeError``. 

.. code-block:: python
    
    try:
        @inheritable_enum
        class MyClass:
            pass
    except TypeError:
        print("Can't decorate a non-enum class with inheritable_enum")

::    
    
    >>> Can't decorate a non-enum class with inheritable_enum


The decorator applies the following modifications to the class before returning it:

#.	A new list attribute, ``__inheritable_members__``, is added to the class, and all defined members are appended to it in the order they are defined.

#.	The ``_member_names_`` list attribute is cleared, removing all member names from the list. This is required to bypass the checks within ``EnumMeta`` for existing members, which raises ``TypeError`` when attempting to subclass an ``Enum``.

#.	The :func:`~extendableenum.restore` is added to the class as a bound classmethod.

.. code-block:: python

    from enum import Enum
    from extendableenum import inheritable_enum
    
    @inheritable_enum
    class Fruit(Enum):
    	APPLE = 1
    	BANANA = 2
    	PEAR = 3
    	
    Fruit.__inheritable__members__
    Fruit._mebers_names_
    Fruit.restore
    Fruit.__members__
    
::    

    >>> ['APPLE', 'BANANA', 'PEAR']
    >>> []
    >>> <bound method _restore of <enum 'Fruit'>>
    >>> {'APPLE': <Fruit.APPLE: 1>, 'BANANA': <Fruit.BANANA: 2>, 'PEAR': <Fruits.Pear: 3>}
    

The Decorated Class
-------------------

Member Access
.............
Once decorated, the ``Enum`` members can still be accessed as normal:

.. code-block:: python

    Fruit['APPLE']	# Access by name
    Fruit(2)		# Access by value
    Fruit.PEAR		# Attribute access

::

    >>> Fruit.APPLE
    >>> Fruit.BANANA
    >>> Fruit.PEAR

Modified Enum Behaviour
.......................
Removing the member from `_member_names_` attribute impacts the following normal behaviour of the ``Enum``:

``__dir__``
^^^^^^^^^^^
The ``__dir__`` function appends the `_member_names_` to the returned list, so the actual members will be excluded:

.. code-block:: python

    dir(Fruit)

::

    >>> ['__class__', '__doc__', '__members__', '__module__']

``__len__``
^^^^^^^^^^^
The ``__len__`` function returns the number of members in `_member_names_`, thus the decorated class will always return 0:

.. code-block:: python

    len(Fruit)

::

    >>> 0
    
``__reversed__``
^^^^^^^^^^^^^^^^
The ``__reversed__`` function returns the `_member_names_` in reversed order, thus the decorated class will not return any of the members:

.. code-block:: python
    
    [member for member in reversed(Fruit)]

::

    >>> []

``__iter__``
^^^^^^^^^^^^
Iteration of ``Enum`` s relies on the `_member_names_`, thus direct iteration of the ``Enum`` is not possible. Iteration is still possible through the ``__members__`` attribute:

.. code-block:: python

    [member for member in Fruit]
    [member for member in Fruit.__members__]
    
::

    >>> []
    >>> ['APPLE', 'BANANA', 'PEAR']
    
Restoring the Enum
------------------
At any time, simply call the `restore` classmethod of the decorated ``Enum``, which will undo all changes to it:

#.	``__inheritable_members__`` are added back to `_member_names_` in definition order.
#.	``__inheritable_members__`` attribute is deleted from the class.
#.	`restore` function is removed from the class.

.. code-block:: python

    Fruit.restore()
    hasattr(Fruit, '__inheritable_members__')
    hasattr(Fruit, 'restore')
    [member for member in Fruit]

::

    >>> False
    >>> False
    >>> [<Fruit.APPLE: 1>, <Fruit.BANANA: 2>, <Fruit.PEAR: 3>]
    
Subclasses of the Decorated Class
---------------------------------
An inheritable ``Enum``, unlike a normal ``Enum``, can be subclassed:

.. code-block:: python

    try:
        class BadFruit(Fruit):
            MANGO = 4
            DRAGONFRUIT = 5
    except TypeError:
        print("This fails because Fruit was restored previously, and normal enums can't be extended")
    
    inheritable_enum(Fruit)    # Make Fruit inheritable again.
    
    class MoreFruit(Fruit):
        MANGO = 4
        DRAGONFRUIT = 5



    >>> This fails because Fruit was restored previously, and normal enums can't be extended

As shown above, the subclass can add additional members. Only these new members will appear in the `_member_names_` attribute of the new class.

.. code-block:: python

    MoreFruit._member_names_

::
    
    >>> ['MANGO', 'DRAGONFRUIT']
    
Side Effects
............
The super class members being excluded from the subclass `_member_names_` attribute has the same side effects as for the :ref:`decorated class <Modified Enum Behaviour>`:

.. code-block:: python

    dir(MoreFruit)
    len(MoreFruit)
    [member for member in reversed(MoreFruit)]
    [member for member in MoreFruit]

::
   
    >>> ['MANGO', 'DRAGONFRUIT', '__class__', '__doc__', '__members__', '__module__']
    >>> 2
    >>> [<MoreFruit.DRAGONFRUIT: 5> , <MoreFruit.MANGO: 4>]
    >>> [<MoreFruit.MANGO: 4>, <MoreFruit.DRAGONFRUIT: 5>]
    
Attribute Access
................
The members defined in the subclass be accessed as usual for an ``Enum``. The super class members may not be accessed by either name or value:

.. code-block:: python

    try:
        MoreFruit['APPLE']
    except KeyError:
        print('Access to super members by name not supported')
        
    try:
        MoreFruit(1)
    except ValueError:
        print('Access to super members by value not supported')

::
    
    >>> Access to super members by name not supported
    >>> Access to super members by value not supported
    
However, super members can be accessed directly as attributes from the subclass. 

.. note::
    The members returned by the subclass **are** the super class ``Enum`` members:

.. code-block:: python

    MoreFruit.APPLE
    MoreFruit.APPLE is Fruit.APPLE

::

    >>> Fruit.APPLE
    >>> True

