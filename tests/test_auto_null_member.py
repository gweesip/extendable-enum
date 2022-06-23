import unittest
import extendableenum
from extendableenum import auto_null_member, _auto_null_member_value, _auto_null_member_name, AutoNullEnum, \
    set_auto_null
from enum import Enum


class TestAutoNullMember(unittest.TestCase):
    def test_autonull_mixin(self):
        @auto_null_member
        class AutoNullMixin(Enum):
            pass

        # AutoNullMixin is an inheritable enum
        self.assertTrue(hasattr(AutoNullMixin, '__inheritable_members__') and
                        hasattr(AutoNullMixin, 'restore'))
        # AutoNullMixin has the null member
        self.assertIn(_auto_null_member_name, AutoNullMixin.__inheritable_members__)
        # AutoNull member has the correct value
        self.assertEqual(AutoNullMixin[_auto_null_member_name].value, _auto_null_member_value)

    def test_autonull_enum(self):
        # auto_null_member decorated enum should automatically include the NULL member.
        @auto_null_member
        class AutoNull(Enum):
            A = 1
            B = 2

        # null member name should appear in _member_names_ along with members defined explicitly
        self.assertListEqual(AutoNull._member_names_, [_auto_null_member_name, 'A', 'B'])
        # AutoNull should have an auto_null_name property that returns the auto null member name used in creation
        # as well as an auto_null_value property that returns the value.
        self.assertTrue(hasattr(AutoNull, 'auto_null_name') and
                        AutoNull.auto_null_name == _auto_null_member_name and
                        hasattr(AutoNull, 'auto_null_value') and
                        AutoNull.auto_null_value == _auto_null_member_value)

        # Should get the same behaviour if the NULL member is explicitly defined in the Enum with the correct value.
        @auto_null_member
        class AutoNull(Enum):
            NULL = None
            A = 1
            B = 2

        self.assertListEqual(AutoNull._member_names_, [_auto_null_member_name, 'A', 'B'])
        self.assertTrue(hasattr(AutoNull, 'auto_null_name') and
                        AutoNull.auto_null_name == _auto_null_member_name and
                        hasattr(AutoNull, 'auto_null_value') and
                        AutoNull.auto_null_value == _auto_null_member_value)

        # Trying to redefine the null member raises a ValueError.
        def redefine_null():
            @auto_null_member
            class AutoNullFailure(Enum):
                A = 1
                NULL = 2

        self.assertRaises(ValueError, redefine_null)

    def test_autonull_ordering(self):
        class OrderedEnum(Enum):
            def __ge__(self, other):
                if self.__class__ is other.__class__:
                    return self.value >= other.value
                return NotImplemented

            def __gt__(self, other):
                if self.__class__ is other.__class__:
                    return self.value > other.value
                return NotImplemented

            def __le__(self, other):
                if self.__class__ is other.__class__:
                    return self.value <= other.value
                return NotImplemented

            def __lt__(self, other):
                if self.__class__ is other.__class__:
                    return self.value < other.value
                return NotImplemented

        @auto_null_member
        class OrderedNullEnum(OrderedEnum):
            A = 1
            B = 2

        # Test ordering of enum members
        self.assertTrue(OrderedNullEnum.B > OrderedNullEnum.A > OrderedNullEnum.NULL and
                        OrderedNullEnum.B >= OrderedNullEnum.A >= OrderedNullEnum.NULL and
                        OrderedNullEnum.NULL < OrderedNullEnum.A < OrderedNullEnum.B and
                        OrderedNullEnum.NULL <= OrderedNullEnum.A <= OrderedNullEnum.B)

        # Test comparisons between nulls
        self.assertTrue(OrderedNullEnum.NULL < OrderedNullEnum.NULL <= OrderedNullEnum.NULL)
        self.assertFalse(OrderedNullEnum.NULL > OrderedNullEnum.NULL or
                         OrderedNullEnum.NULL >= OrderedNullEnum.NULL)

    def test_autonull_module_variables(self):
        @auto_null_member
        class Enum1(Enum):
            A = 1

        extendableenum.set_auto_null('IAMNULL', 0)
        extendableenum._auto_null_member_name = 'IAMNULL'
        extendableenum._auto_null_member_value = 0

        @auto_null_member
        class Enum2(Enum):
            A = 1

        self.assertFalse(Enum1.auto_null_value == extendableenum._auto_null_member_value)
        self.assertNotIn(extendableenum._auto_null_member_name, Enum1._member_names_)
        self.assertTrue(Enum2.auto_null_value == extendableenum._auto_null_member_value)
        self.assertIn(extendableenum._auto_null_member_name, Enum2._member_names_)

        def invalid_name():
            set_auto_null(1, 'Bad!')

        self.assertRaises(TypeError, invalid_name)

        # restore module level variables for other tests...
        extendableenum._auto_null_member_name = 'NULL'
        extendableenum._auto_null_member_value = None

    def test_autonull_base(self):
        # Deriving without decoration inherits the base class null member
        class Undecorated(AutoNullEnum):
            A = 1
            B = 2

        # Deriving with decoration should have its own null member
        @auto_null_member
        class Decorated(AutoNullEnum):
            A = 1
            B = 2

        # Undecorated NULL is the inherited null member
        self.assertIs(Undecorated.NULL, AutoNullEnum.NULL)
        # Decorated NULL is a distinct null member
        self.assertIsNot(Decorated.NULL, AutoNullEnum.NULL)
        # Subclasses can access the base class NULL member through super
        self.assertIs(super(Undecorated, Undecorated).NULL, AutoNullEnum.NULL)
        self.assertIs(super(Decorated, Decorated).NULL, AutoNullEnum.NULL)

        self.assertIs(Undecorated.auto_null_member(), Undecorated.NULL)
        self.assertIs(Decorated.auto_null_member(), Decorated(None))

        # test __bool__ function inherited from AutoNullEnum
        self.assertFalse(Undecorated.NULL)
        self.assertFalse(Decorated.NULL)
        self.assertTrue(Undecorated.A)
        self.assertTrue(Decorated.A)


if __name__ == '__main__':
    unittest.main()
