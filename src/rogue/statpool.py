import enum

@enum.unique
class Stat(enum.IntEnum):
    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2

class StatPool():

    def __init__(self):
        self.stats = {
            Stat.STRENGTH : 10,
            Stat.DEXTERITY : 10,
            Stat.CONSTITUTION : 10
        }