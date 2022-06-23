import unittest
from extendableenum import post_mixin_enum
from enum import Enum


class TestPostMixinEnum(unittest.TestCase):
    def test_postmixin(self):
        class TheEnum(Enum):
            A = 1
            B = 2

        @post_mixin_enum(TheEnum)
        class TheMixin:
            def mixin_method(self):
                if self.value == 1:
                    return 42
                elif self.name == 'B':
                    return 43

        # Enum members should be instances of the mixin
        self.assertIsInstance(TheEnum.A, TheMixin)
        self.assertIsInstance(TheEnum.B, TheMixin)
        # The mixin_method should be callable from the enum members
        self.assertEqual(TheEnum.A.mixin_method(), 42)
        self.assertEqual(TheEnum.B.mixin_method(), 43)

    def test_cant_extend(self):
        class TheEnum(Enum):
            A = 1
            B = 2

        def add_member_mixin():
            # This should fail
            @post_mixin_enum(TheEnum)
            class TheMixin(Enum):
                C = 3

        self.assertRaises(TypeError, add_member_mixin)


if __name__ == '__main__':
    unittest.main()