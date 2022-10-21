from random import random
from rogue.actor import Actor
from rogue.statpool import Stat
import rogue.statpool
import enum
import rogue.tile

class PlayerDamage(enum.IntEnum):
    MAX = 0
    MIN = 1



class Player(Actor):
    
    def __init__(self):
        self.statpool = rogue.statpool.StatPool()
        self.max_health = 10
        self.current_health = 10
        self.level = 1
        self.name = "Gorbath the Simple"
        self.character_class = ""
        self.can_act = True
        self.can_move = True
        self.accuracy = 100
        self.flat_dr = 0
        self.percent_dr = 0
        self.defence = 15
        self.damage = {
            PlayerDamage.MAX : 5,
            PlayerDamage.MIN : 3
        }
        self.entity = {
            0 : self.player_attack,
            1 : self.player_stand,
            2 : self.player_swap,
            3 : self.player_move
        }

    def player_attack(self, target):
        pass

    def player_stand(self):
        pass

    def player_swap():
        pass

    def player_move():
        pass

    def get_damage_done(self, target):
        self.damage_done = (target.flat_dr - random(3,5)) / target.percent_dr
        return self.damage_done

    

    def combat_roll(self, target):
        hit = False
        attack_roll = random(1, self.accuracy)
        if attack_roll >= target.defence:
            hit = True
        return hit

    def combat_miss(self):
        print(str(self.name) + " missed!")

    def do_player_combat(self, target):
        if self.can_act:
            if self.combat_roll(target):
                damage = self.get_damage_done(target)
                target.change_health(damage)
            else:
                self.combat_miss()


            


    