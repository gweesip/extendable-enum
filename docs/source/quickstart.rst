Getting Started with extendable-enum
====================================

Once you have completed :ref:`Installation`, simply import the package/components as required::

    from extendableenum import *
    
The above imports the following:

Inheritable Enums
-----------------

An enum class can be made inheritable by decorating with the ``inheritable_enum`` class decorator::

    @inheritable_enum
    class MyEnum(Enum):
    	A = 1
    	B = 2
    	
    class MySubEnum(MyEnum):
    	C = 3
    	D = 4
    	
Auto Null Enums
---------------

Enum classes can automatically contain a default null member with the ``auto_null_member`` class decorator::

    @auto_null_member
    class MyEnum(Enum)
        NULL = None    # Redundant. If missing, decorator will add this automatically.
        A = 1
        B = 2

The name and value of the auto null member can be configured with the ``set_auto_null`` function::

    set_auto_null('NULL', None)    # Default name and value if this function isn't called.
    
The ``AutoNullEnum`` class is a base class for auto null enums, containing some useful functions for dealing with the null member::

    class MyNullEnum(AutoNullEnum):
    	A = 1
    	B = 2
    	
Post Mixin Enums
----------------

Add functionality to an existing Enum class with the ``post_mixin_enum`` class decorator::

    @post_mixin_enum(MyEnum)
    class MyPostMixin:
        def some_method():
    	    ...
    	    
Copy Enum Members
-----------------

Members can be copied from an existing Enum to a new one with the ``copy_enum_members`` class decorator. The new class can optionally add new members::

    class Fruit(Enum):
        APPLE = 1
        BANANA = 2
        PEAR = 3
        
    @copy_enum_members(Fruit)
    class MoreFruit(Enum)
        MANGO = 4
        DRAGONFRUIT = 5
        
