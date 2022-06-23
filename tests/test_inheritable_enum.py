import unittest
from extendableenum import inheritable_enum
from enum import Enum


class TestInheritableEnum(unittest.TestCase):
    def test_decorate(self):
        """Test decoration of enums."""
        # Decorating an enum should not throw an error.
        try:
            @inheritable_enum
            class TestEnum(Enum):
                A = 1
                B = 2
        except:
            self.fail("Subclassing decorated Enum raised an exception!")

        # Decorating a non-enum member should throw an TypeError.
        def non_enum_type_error():
            @inheritable_enum
            class NonEnum:
                pass

        self.assertRaises(TypeError, non_enum_type_error)

    def test_decorated(self):
        """Test the decorated enum's properties."""

        @inheritable_enum
        class TestEnum(Enum):
            A = 1
            B = 2

        # decorated enum _member_names_ should be empty list
        self.assertListEqual(TestEnum._member_names_, [])
        # decorated enum can still access members as normal
        self.assertIs(TestEnum.A, TestEnum(1))
        self.assertIs(TestEnum['B'], TestEnum.B)
        # decorated enum has __inheritable_members__ and restore
        self.assertTrue(hasattr(TestEnum, '__inheritable_members__') and
                        hasattr(TestEnum, 'restore'))
        # all members are in __inheritable_members__
        self.assertListEqual(TestEnum.__inheritable_members__, ['A', 'B'])
        # decorated enum restore is callable
        self.assertTrue(callable(TestEnum.restore))

    def test_subclassing(self):
        """Test subclassing an inheritable enum."""

        @inheritable_enum
        class Base(Enum):
            A = 1
            B = 2

        # should be able to subclass inheritable enum
        try:
            class Derived(Base):
                C = 3
                D = 4
        except:
            self.fail('Subclassing inheritable enum raised an exception!')

        # Subclassed enum can add new members
        self.assertListEqual(Derived._member_names_, ['C', 'D'])
        # Subclassed enum can access base members as attributes
        self.assertIs(Derived.A, Base.A)

        # Subclass cannot access base members by value/name
        def access_by_name():
            return Derived['A']

        def access_by_value():
            return Derived(1)

        self.assertRaises(KeyError, access_by_name)
        self.assertRaises(ValueError, access_by_value)

    def test_restore(self):
        """Test restoring an inheritable enum."""

        @inheritable_enum
        class TestEnum(Enum):
            A = 1
            B = 2

        TestEnum.restore()
        # Enum should no longer have __inheritable_members__ and restore
        self.assertFalse(hasattr(TestEnum, '__inheritable_members__') or
                         hasattr(TestEnum, 'restore'))
        # Enum members should be in _member_names_
        self.assertListEqual(TestEnum._member_names_, ['A', 'B'])


if __name__ == '__main__':
    unittest.main()
