import unittest
from extendableenum import copy_enum_members
from enum import Enum


class TestCopyEnumMembers(unittest.TestCase):
    def test_copy_enum_members(self):
        class Base1(Enum):
            A = 1
            B = 2

        class Base2(Enum):
            C = 3
            D = 4

        @copy_enum_members(Base1, Base2)
        class Derived(Enum):
            E = 5

        # Derived should have A, B, and C members.
        self.assertListEqual(Derived._member_names_, ['A', 'B', 'C', 'D', 'E'])

        # Derived enum members are distinct classes.
        self.assertIsNot(Derived.A, Base1.A)
        self.assertIsNot(Derived.C, Base2.C)

        self.assertTrue(hasattr(Derived, '__copied_from__'))
        self.assertTupleEqual(Derived.__copied_from__, (Base1, Base2))


if __name__ == '__main__':
    unittest.main()
