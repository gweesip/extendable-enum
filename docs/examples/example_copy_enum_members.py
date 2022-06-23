from enum import Enum
from extendableenum import copy_enum_members

if __name__ == '__main__':
    class Fruits(Enum):
        APPLE = 1
        BANANA = 2
        PEAR = 3

    class Vegetables(Enum):
        ASPARAGUS = 1
        BROCCOLI = 12
        CARROT = 13

    @copy_enum_members(Fruits, Vegetables)
    class MyFavoriteFoods(Enum):
        BEEF = 21
        CHICKEN = 22
        PORK = 23

    print(MyFavoriteFoods.APPLE)
    print(MyFavoriteFoods.BROCCOLI is not Vegetables.BROCCOLI)

    print(MyFavoriteFoods.__copied_from__)