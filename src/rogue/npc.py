from rogue.actor import Actor
from rogue.statpool import Stat
import rogue.statpool
import enum

class NPCDamage(enum.IntEnum):
    MAX = 0
    MIN = 1
class NPC(Actor):
    
    def __init__(self):
        self.statpool = rogue.statpool.StatPool()
        self.max_health = 5
        self.current_health = 5
        self.level = 1
        self.name = "Goblin"
        self.character_class = ""
        self.can_act = True
        self.can_move = True
        self.accuracy = 50
        self.flat_dr = 0
        self.percent_dr = 0
        self.defence = 10
        self.damage = {
            NPCDamage.MAX : 3,
            NPCDamage.MIN : 1
        }
        
