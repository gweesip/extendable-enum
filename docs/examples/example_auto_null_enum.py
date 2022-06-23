from enum import Enum
from extendableenum import set_auto_null, auto_null_member, AutoNullEnum

if __name__ == '__main__':
    @auto_null_member
    class Default(Enum):
        pass

    set_auto_null('CUSTOM', 'Null')

    @auto_null_member
    class Custom(Enum):
        pass

    print(Default.__members__)
    print(Custom.__members__)

    print(Default.__inheritable_members__)

    set_auto_null('NULL', None)

    @auto_null_member
    class Directions(Enum):
        NORTH = 0
        SOUTH = 1
        DENNIS = 2

    print(Directions.__members__)


    @auto_null_member  # Decorator has no effect in this case
    class SameDirections(Enum):
        NORTH = 0
        SOUTH = 1
        NULL = None
        DENNIS = 2

    print(SameDirections.__members__)


    @auto_null_member
    class NullAlias(Enum):
        NULL_ALIAS = None

    print(NullAlias.NULL_ALIAS is NullAlias.NULL)

    try:
        @auto_null_member
        class RedefineNull(Enum):
            A = 1
            NULL = 2
    except ValueError:
        print('Cannot redefine the null member')


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
    class NullGrade(OrderedEnum):
        A = 5
        B = 4
        C = 3
        D = 2
        F = 1

    print(NullGrade.NULL < NullGrade.A)
    print(NullGrade.NULL <= NullGrade.B)
    print(NullGrade.NULL > NullGrade.C)
    print(NullGrade.NULL >= NullGrade.C)
    print(NullGrade.NULL < NullGrade.NULL)
    print(NullGrade.NULL <= NullGrade.NULL)
    print(NullGrade.NULL > NullGrade.NULL)
    print(NullGrade.NULL >= NullGrade.NULL)

    class AutoNullDerived(AutoNullEnum):
        A = 1
        B = 2

    print(AutoNullDerived.auto_null_member())
    print(bool(AutoNullDerived.A))
    print(bool(AutoNullDerived.auto_null_member()))

    class Undecorated(AutoNullEnum):
        A = 1
        B = 2

    @auto_null_member
    class Decorated(AutoNullEnum):
        A = 1
        B = 2

    print(Decorated.auto_null_member())
    print(Undecorated.auto_null_member())
    print(super(Decorated, Decorated).NULL)