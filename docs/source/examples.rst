Basic Examples
==============

Create an Inheritable Enum and Subclass
---------------------------------------

.. code-block:: python

    from enum import Enum
    from extendableenum import inheritable_enum

    @inheritable_enum
    class Base(Enum):
        A = 1
        B = 2

    # Subclass Base, define new members and an aliases.
    class Derived(Base):
        ALIAS_B = 2
        C = 3
        D = 4  

Create an Enum with the Null Member
-----------------------------------

.. code-block:: python

    from enum import Enum
    from extendableenum import auto_null_member, set_auto_null

    # optional: specify null member name and value
    set_auto_null('NULL', None) # this is the default name/value

    @auto_null_member
    class Fruit(Enum):
        APPLE = 1
        BANANA = 2
        PEAR = 3

    print(f'{Fruit.NULL.name}, {Fruit.NULL.value}')
    >>> NULL, None
    
Create a Custom Base Class for Auto Null Enums
----------------------------------------------

.. code-block:: python

    from enum import Enum
    from extendableenum import auto_null_member

    @auto_null_member
    class MyAutoNullEnum(Enum):
        # No enum members defined, MyAutoNullEnum is inheritable.
        def some_method(self):
            print(f'My name is {self.name} and my value is {self.value}')

    # Without the auto_null_member decorator
    class Fruit(MyAutoNullEnum):
        APPLE = 1
        BANANA = 2
        PEAR = 3

    Fruit.APPLE.some_method()
    Fruit.NULL.some_method()


>>> My name is APPLE and my value is 1
>>> My name is NULL and my value is None

Extend an Externally Defined Enum with Methods
----------------------------------------------

.. code-block:: python

    from enum import Enum
    from some_library import SomeEnum
    from extendableenum import post_mixin_enum

    @post_mixin_enum(SomeEnum)
    class MyMixin(Enum):
        def my_new_mixin(self):
            print('This is my new mixin function')

    # SomeEnum is now a subclass of MyMixin!
    SomeEnum.MEMBER.my_new_mixin()
    

>>> This is my new mixin function
    
Copy an Existing Enum with Additional Members
---------------------------------------------

.. code-block:: python

    from enum import Enum
    from extendableenum import copy_enum_members

    class AmpVolume(Enum):
        MUTE = 0
        QUIET = 1
        NORMAL = 5
        LOUD = 7
        TOOLOUD = 10
   
    @copy_enum_members(AmpVolume)
    class BetterAmpVolume(Enum):
        METAL = 10      # Alias for TOOLOUD
        SPINALTAP = 11
  
    print(repr(BetterAmpVolume.METAL))
    
    
>>> <BetterAmpVolume.TOOLOUD: 10>
