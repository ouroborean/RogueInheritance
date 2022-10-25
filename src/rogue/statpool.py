import enum

@enum.unique
class Stat(enum.IntEnum):
    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2
    INTELLIGENCE = 3
    WISDOM = 4
    FLAT_DR = 5
    PERCENT_DR = 6
    DEFENCE = 7

class StatPool():

    def __init__(self):
        self.stats = {
            Stat.STRENGTH : 10,
            Stat.DEXTERITY : 10,
            Stat.CONSTITUTION : 10,
            Stat.INTELLIGENCE: 10,
            Stat.WISDOM: 10,
            Stat.FLAT_DR: 0,
            Stat.PERCENT_DR: 0,
            Stat.DEFENCE: 0
        }