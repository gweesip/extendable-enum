from enum import Enum
from extendableenum import post_mixin_enum

if __name__ == '__main__':
    class Animal(Enum):
        ANT = 1
        BEE = 2
        CAT = 3
        DOG = 4


    @post_mixin_enum(Animal)
    class SpeakMixin:
        def speak(self):
            if self is Animal.ANT:
                return '...'
            elif self is Animal.BEE:
                return 'buzz buzz'
            elif self is Animal.CAT:
                return 'Meow'
            elif self is Animal.DOG:
                return 'Woof'
            else:
                return '???'

    print(Animal.__bases__)
    print(isinstance(Animal.ANT, SpeakMixin))
    print(Animal.BEE.speak())
