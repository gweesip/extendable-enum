from enum import Enum, EnumMeta
from types import MethodType

_auto_null_member_name = 'NULL'
_auto_null_member_value = None


def set_auto_null(name: str, value):
    """
    Sets the auto null member name and value.

    Configures the module level auto null member name and value. When a new enum is created and
    decorated with :func:`auto_null_member`, it will use the internally configured auto null member
    name and value.

    Args:
        name: The name of the null member. Default is `NULL`.
        value: The value of the null member. Default is ``None``.

    Raises:
        TypeError: If the name is not a 'str'.

    Note:
        The auto null member name and value are stored in the class during creation and will persist
        despite any changes to the module level name/value after creation.
    """
    global _auto_null_member_name, _auto_null_member_value
    if not isinstance(name, str):
        raise TypeError('Null member name must be a str!')
    _auto_null_member_name = name
    _auto_null_member_value = value


def _restore(the_enum):
    """
    Restores the original state of an inheritable enum.

    Undoes all modifications to the class performed by the :func:`inheritable_enum` decorator.

    Note:
        This method is automatically added as a bound class method to any class decorated by
        :func:`inheritable_enum`.
    """
    for inh_member in the_enum.__inheritable_members__:
        # noinspection PyProtectedMember
        the_enum._member_names_.append(inh_member)
    delattr(the_enum, '__inheritable_members__')
    delattr(the_enum, 'restore')


def inheritable_enum(the_enum):
    """
    Makes the specified enum members inheritable.

    This enum class decorator allows an enum class to be inheritable by removing all enum members from the
    ``_member_names_`` attribute. New enums can then subclass and inherit the members from the base class.

    Raises:
        TypeError: if the decorated class is not an ``Enum``.

    Note:
        Removing members from the ``_member_names_`` attribute impacts the normal behaviour of
        enums. The following magic functions will ignore any inheritable enum members:
        ``__dir__``, ``__iter__``, ``__len__``, and ``__reversed__``.

    Note:
        Enums that inherit from an inheritable enum can only access the inherited members as attributes
        (eg: ``MyEnum.NAME``). Name lookup (eg: ``MyEnum['NAME']``) and value lookup (eg: ``MyEnum(value)``)
        will fail.

    Note:
        After decoration, an enum class can be restored to its original state by calling the :func:`restore`
        method (eg: ``MyEnum.restore()``), which adds the member names back to the ``_member_names_`` attribute.
    """
    if type(the_enum) is not EnumMeta:
        raise TypeError(f'Cannot add inheritable enum members to a non-enum object!')
    setattr(the_enum, '__inheritable_members__', [])
    # noinspection PyProtectedMember
    for member in the_enum._member_names_:
        the_enum.__inheritable_members__.append(member)
    the_enum._member_names_ = []

    # Adds the restore method to the class. This method is bound to the decorated class as a classmethod.
    bound_restore = MethodType(_restore, the_enum)
    setattr(the_enum, 'restore', bound_restore)

    return the_enum


def _rebuild_enum(_cls, new_member_names):
    """Rebuild an enum with new member names. All other values should be preserved."""
    # get the member_type, first_enum and any extra bases/mixins.
    # noinspection PyProtectedMember
    member_type, first_enum = _cls._get_mixins_(_cls, _cls.__bases__)
    extra_bases = list(_cls.__bases__)
    extra_bases.remove(first_enum)
    _new_enum = Enum(value=_cls.__name__,
                     names=new_member_names,
                     module=_cls.__module__,
                     qualname=_cls.__qualname__,
                     # if first_enum is Enum, the type argument must be None.
                     type=first_enum if first_enum is not Enum else None)
    # add the original bases to the new class.
    if extra_bases:
        _new_enum.__bases__ = tuple(extra_bases) + (first_enum,)
    # add back any other items in the __dict__ that may not have been included in the rebuild.
    for key in _cls.__dict__:
        # Enum automatically adds a rather boring doc, so make sure that doesn't stick!
        if key not in _new_enum.__dict__ or key == '__doc__':
            setattr(_new_enum, key, _cls.__dict__[key])
    return _new_enum


def auto_null_member(the_enum):
    """
    Adds the null member to an enum if required.

    Enum class decorator which will add the auto null member to the class if missing. The auto null
    member will have the name and value as configured at the module level which can be set
    using :func:`set_auto_null`.

    If the decorated class doesn't define any members, the class is
    considered a mixin and becomes inheritable (see :func:`inheritable_enum`), otherwise, the null
    member is prepended to the defined members.

    Args:
        the_enum: the decorated class.

    Raises:
        TypeError: if the decorated class is not an ``Enum``.
    """

    if type(the_enum) is not EnumMeta:
        raise TypeError(f'Non-enum classes cannot be decorated with auto_null_member!')

    # function binder for comparison methods. This interjects a check for the null member before
    # deferring comparison to the originally defined function.
    def _compare_function_binder(func):
        """
        Function Binder - Binds previously defined comparison methods to a new comparison
        method that accommodates the auto-null member.

        This method is used to augment the normal comparison methods that may be present in
        an enum. If an enum class has ```__lt__```, ```__gt__```, ```__le__```, or ```__ge__```
        methods (either defined or inherited), these methods will be redefined to accommodate
        auto-null member comparisons. The originally defined comparison function will be bound
        as a fall-through case.

        If neither object being compared is the auto-null member (or the objects are of different
        classes), the originally defined comparison method will be called, otherwise, a boolean
        value is returned. The auto-null member always evaluates to 'less than' a valid enum member.

        In cases where the auto-null is compared to itself, 'less than' comparisons return
        ```True``` and 'greater than` comparisons return ```False```.
        """

        # The following is temporarily removed for the quick and easy fix of moving the conditionals inside
        # new_compare_fn. Will investigate the use of partials or other method to handle this to make the code
        # a little easier to read and follow. The intent of this was to have the values for self and other null
        # cases separate from the main logic to make it obvious and easier to configure.
        # if func.__name__ in ('__lt__', '__le__'):
        #     null_self_return = True
        #     null_other_return = False
        # if func.__name__ in ('__gt__', '__ge__'):
        #     null_self_return = False
        #     null_other_return = True

        def new_compare_fn(self, other):
            if self.__class__ is other.__class__:
                if self is self.__class__(_auto_null_member_value):
                    # self_null_return
                    if func.__name__ in ('__lt__', '__le__'):
                        return True
                    # __gt__ or __ge__, self_null_return
                    else:
                        return False
                elif other is other.__class__(_auto_null_member_value):
                    # null_other_return
                    if func.__name__ in ('__lt__', '__le__'):
                        return False
                    # __gt__ or __ge__, null_other_return
                    else:
                        return True
            # fall through case defers to originally defined function
            return func(self, other)

        return new_compare_fn

    # if no members are defined, or the only member defined is the null member (ie a mixin).
    is_mixin = len(the_enum) == 0 or (len(the_enum) == 1 and _auto_null_member_name in the_enum.__members__)
    # if the null member was defined explicitly in the class definition.
    if len(the_enum) and _auto_null_member_name in the_enum.__members__:
        # and it is the correct value
        if the_enum.__members__[_auto_null_member_name].value == _auto_null_member_value:
            # no need to rebuild the class, so we can return the original class.
            new_enum = the_enum
        # cls defined a null member with the incorrect value (overwrite attempt). Throw TypeError.
        else:
            raise ValueError(f"{the_enum} decorated with auto_null_member:\n"
                             f"\tAttempted to redefine '{_auto_null_member_name}' member with incorrect value"
                             f" {the_enum.__members__[_auto_null_member_name].value}.\n"
                             f"\t'{_auto_null_member_name}' member must have value {_auto_null_member_value}.")
    else:
        # Enum will be rebuilt with the auto-null member inserted as the first element
        new_member_names = [(_auto_null_member_name, _auto_null_member_value)]
        new_member_names += [(name, val.value) for name, val in the_enum.__members__.items()]
        new_enum = _rebuild_enum(the_enum, new_member_names)

    if is_mixin:
        # make the null member inheritable.
        # noinspection PyTypeChecker
        new_enum = inheritable_enum(new_enum)

    # Add the auto_null_member_name and auto_null_member_value as a class attribute.
    # This is to allow modifying the module level name and value while retaining a record of what name/value
    # was used when creating the individual classes.
    setattr(new_enum, 'auto_null_name', _auto_null_member_name)
    setattr(new_enum, 'auto_null_value', _auto_null_member_value)

    # If the decorated enum had comparison methods, they need to be redefined to accommodate the null member
    # redefine the comparison functions if they exist in the original class to allow for comparisons between
    # valid enum members and the null member.
    for compare_function in ('__gt__', '__lt__', '__ge__', '__le__'):
        old_function = getattr(new_enum, compare_function, None)
        # only modify comparison functions if they exist and are not wrapper descriptors.
        if old_function is not None and type(old_function).__name__ != 'wrapper_descriptor':
            setattr(new_enum, compare_function, _compare_function_binder(old_function))

    return new_enum


@auto_null_member
class AutoNullEnum(Enum):
    """A Base class for auto null Enums."""

    @classmethod
    def auto_null_member(cls):
        """Returns the null member."""
        return getattr(cls, cls.auto_null_name)

    def __bool__(self):
        """Valid members return ``True``, null member returns ``False``."""
        return self is not self.__class__.auto_null_member()


def post_mixin_enum(the_enum):
    """
    Adds a new base class to an existing enum class.

    Class decorator which prepends the decorated class to the enum class' bases. This allows an
    existing enum class to be extended with methods after creation.

    Args:
         the_enum: the ``Enum`` class which is to be modified.

    Raises:
        TypeError: if the mixin class is an ``Enum`` and it defines any members.
    """
    def insert_class(new_mixin):
        if isinstance(new_mixin, EnumMeta) and len(new_mixin):
            raise TypeError(f'{new_mixin}: cannot extend enumeration {the_enum}')
        # Note that the new mixin cannot be appended to the bases, as this breaks enum functionality.
        the_enum.__bases__ = (new_mixin,) + the_enum.__bases__
        return new_mixin

    return insert_class


def copy_enum_members(*args):
    """
    Copies enum member name/values from existing enum classes.

    Enum class decorator which allows the decorated class to 'inherit' the members from other
    enum classes.

    Args:
        args: the ``Enum`` class(es) to copy members from.

    Raises:
        TypeError: if any of the classes are not ``Enum`` s.
    """
    def add_members(derived_enum):
        if not isinstance(derived_enum, EnumMeta):
            raise TypeError(f'Cannot add enum members to non Enum class {derived_enum}')
        new_member_names = []
        for base_enum in args:
            if not isinstance(base_enum, EnumMeta):
                raise TypeError(f'Cannot copy enum members from non enum class {base_enum}')
            new_member_names += [(name, val.value) for name, val in base_enum.__members__.items()]
        new_member_names += [(name, val.value) for name, val in derived_enum.__members__.items()]
        setattr(derived_enum, '__copied_from__', args)
        return _rebuild_enum(derived_enum, new_member_names)

    return add_members


if __name__ == '__main__':
    pass
