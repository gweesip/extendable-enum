# Example code showing the inheritable_enum decorator and its behaviour.
# This code is used in the docs as well.

from enum import Enum
from extendableenum import inheritable_enum

if __name__ == '__main__':
    # Only Enum classes can be decorated. Others raise a TypeError
    try:
        @inheritable_enum
        class MyClass:
            pass
    except TypeError:
        print("Can't decorate a non-enum class with inheritable_enum")

    # Make an inheritable enum.
    @inheritable_enum
    class Fruit(Enum):
        APPLE = 1
        BANANA = 2
        PEAR = 3

    # The decorator adds the member names to a new attribute, __inheritable_members__,
    print(Fruit.__inheritable_members__)
    # clears the _member_names_ attribute, and
    print(Fruit._member_names_)
    # adds the restore function
    print(Fruit.restore)
    # The members still exist and can be accessed through the __members__ attribute
    print(Fruit.__members__)

    # They can also be accessed by name, value and attribute.
    print(Fruit['APPLE'])
    print(Fruit(2))
    print(Fruit.PEAR)

    # Since the members are no longer in _member_names_, they are not included in dir,
    print(dir(Fruit))
    # they are not counted by len,
    print(len(Fruit))
    # they are not included in reversed, and
    print([member for member in reversed(Fruit)])
    # they are not included in iteration.
    print([member for member in Fruit])
    # They can still be iterated using the __members__ attribute
    print([member for member in Fruit.__members__])

    # The decorated class can be restored,
    Fruit.restore()
    # which deletes the __inheritable_members__ attribute,
    print(hasattr(Fruit, '__inheritable_members__'))
    # removes the restore function, and
    print(hasattr(Fruit, 'restore'))
    # restores all names in _member_names_ in the definition order.
    print([member for member in Fruit])

    # Once restored, the class cannot be inherited.
    try:
        class BadFruit(Fruit):
            MANGO = 4
            DRAGONFRUIT = 5
    except TypeError:
        print("This fails because Fruit was restored previously, and normal enums can't be extended")

    # But we can easily make it inheritable again
    inheritable_enum(Fruit)

    # And create a subclass with new members
    class MoreFruit(Fruit):
        MANGO = 4
        DRAGONFRUIT = 5

    # Only the non-inherited members will be in _member_names_
    print(MoreFruit._member_names_)

    # Inherited members are not included in dir, len, reversed or iteration
    print(dir(MoreFruit))
    print(len(MoreFruit))
    print([member for member in reversed(MoreFruit)])
    print([member for member in MoreFruit])

    # Inherited members can not be accessed by name
    try:
        MoreFruit['APPLE']
    except KeyError:
        print('Access to super members by name not supported')

    # or by value
    try:
        MoreFruit(1)
    except ValueError:
        print('Access by value not allowed')

    # but can still be accessed as attributes.
    print(MoreFruit.APPLE)
    # The returned members are the superclass members.
    print(MoreFruit.APPLE is Fruit.APPLE)