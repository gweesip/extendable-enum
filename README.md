# Extendable Enum

`extendableenum` is a simple package for extending, subclassing and reusing python `Enum` classes.
It contains four class decorators and a single class:
1. `inheritable_enum` - Enum class decorator. Makes the class and all its members inheritable. 
Subclassing enums can define new members while still having access to the base class members. 
2. `auto_null_member` - Enum class decorator. Automatically adds the null member to an enum class.
If the class doesn't define any other enum members, also becomes an inheritable enum. The auto null 
member name and value can be set with the `set_auto_null` function. Default name/value is
`NULL/None`.
3. `post_mixin_enum` - Enum class decorator. Adds the decorated class as a base class to an existing
enum. Allows extending an enum class with methods after creation.
4. `copy_enum_members` - Enum class decorator. Creates a new and distinct enum class with the same
members as an existing enum. New enum can optionally define additional members.
5. `AutoNullEnum` - A base class for enum classes using the auto null feature. Contains convenience
functions for dealing with the auto null member.

# Documentation

Full documentation for the package can be found on [read the docs](https://extendable-enum.readthedocs.io/en/latest/)

# Installation

Install with pip:

```
pip install extendable-enum
```

# Requirements

- Python 3.6+
  - This version was auto-detected by the [vermin](https://github.com/netromdk/vermin) package.
  This is yet to be verified.

# Examples
Basic usage and examples can be found here. For in depth behaviour and advanced
usage, see the [docs](link.com).
## Inheritable Enums
```
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

Base.restore() # Base now behaves as if it were never decorated.
```

## Auto Null Member
### Create An Enum with the Null Member
```
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
```
### Create a Custom Base Class for Auto Null Enums
```
from enum import Enum
from extendableenum import auto_null_member

@auto_null_member
class MyAutoNullEnum(Enum):
  # No enum members defined, MyAutoNullEnum is inheritable.
  def some_method(self):
    print(f'My name is {self.name} and my value is {self.value}')

class Fruit(MyAutoNullEnum):
  APPLE = 1
  BANANA = 2
  PEAR = 3

Fruit.APPLE.some_method()
>>> My name is APPLE and my value is 1
Fruit.NULL.some_method()
>>> My name is NULL and my value is None

*** move the below to the docs. ***
# With decorator
@auto_null_enum
class Decorated(MyAutoNullEnum):
  A = 1
  B = 2
  
  # override some_method
  def some_method(self):
    print(f'{self.name}:{self.value}')

assert(Decorated.NULL is not MyAutoNullEnum.NULL)
Decorated.A.some_method()
>>> A:1
Decorated.NULL.some_method()
>>> NULL:None
# access MyAutoNULLEnum.NULL using super()
super(Decorated, Decorated).NULL.some_method()
>>> My name is NULL and my value is None
```

## Post Mixin Enum
### Extending an Externally Defined Enum
```
from enum import Enum
from some_library import SomeEnum
from extendableenum import post_mixin_enum

@post_mixin_enum(SomeEnum)
class MyMixin(Enum):
  def my_new_mixin(self):
    print('This is my new mixin function!')

# SomeEnum is now a subclass of MyMixin!
assert(isinstance(SomeEnum.MEMBER, MyMixin))
SomeEnum.MEMBER.my_new_mixin()
>>> This is my new mixin function!
```

## Copy Enum Members
### Extend an Existing Enum with Additional Name/Values
```
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

```

# Contributing
Pull requests are always welcome! For any additional features or major changes,
please open an issue for discussion.

This is my first public project, so any comments, suggestions, and feedback are also welcome!

# Acknowledgements
Thanks to StackOverflow users `Ethan Furman`, `jsbueno` and `l4mpi` for
inspiration, help and some code examples (see 
[this question](https://stackoverflow.com/questions/72100527/add-a-mixin-to-python-enum-after-its-created)
if you are curious).
# License
[GNU GPL v 3](https://www.gnu.org/licenses/gpl-3.0.en.html)
