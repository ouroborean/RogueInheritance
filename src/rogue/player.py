from random import random
from rogue.actor import Actor
from rogue.statpool import Stat
import rogue.statpool
import enum
from rogue.tile import Tile, TileEntity
from rogue.tilemap import TileMap
import random
from rogue.direction import direction_to_pos
from rogue.equipment import Equipment, Slot
from rogue.scenery import Portal
import typing

if typing.TYPE_CHECKING:
    from rogue.game_scene import GameScene


class PlayerDamage(enum.IntEnum):
    MAX = 0
    MIN = 1



class Player(Actor):
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])

    def __init__(self):
        self.statpool = rogue.statpool.StatPool()
        # self.item_gain = Equipment()
        self.inventory = []
        self.max_health = 200
        self.loc = (3, 2)
        self.current_health = 200
        self.level = 1
        self.name = "Gorbath the Simple"
        self.character_class = ""
        self.can_act = True
        self.tile = ()
        self.can_move = True
        self.is_new = False
        self.accuracy = 100
        self.flat_dr = 0
        self.percent_dr = 0
        self.turn_counter = 0.0
        self.speed = 1.0
        self.image = ""
        self.defence = 15
        self.game_scene = None
        self.to_inventory = None
        self.to_equip = None
        self.damage = {
            PlayerDamage.MAX : 5,
            PlayerDamage.MIN : 3
        }
        self.actions = {
            0 : self.player_attack,
            1 : self.player_stand,
            2 : self.player_swap,
            3 : self.player_move,
            4 : self.player_stand
        }
        self.equipped = {
            Slot.HEAD : None,
            Slot.SHOULDERS : None,
            Slot.CHEST : None,
            Slot.HANDS : None,
            Slot.LEGS : None,
            Slot.FEET : None
        }

    def check_player_bump(self, target):
        self.actions[target.entity](target)

    def player_attack(self, target):
        print(f"Player attacking {target.actor.name}")
        self.do_player_combat(target.actor)

    def player_stand(self, tile):
        print("Player wastes a turn doing nothing!")    
        
    def set_game_scene(self, scene: "GameScene"):
        self.game_scene = scene
    
    def player_swap(self):
        pass

    def player_move(self, tile):
        diff = (tile.loc[0] - self.loc[0], tile.loc[1] - self.loc[1])
        self.game_scene.tile_map.get_tile(self.loc).entity = TileEntity.EMPTY
        self.game_scene.tile_map.get_tile(self.loc).actor = None
        self.loc = self + diff
        tile.entity = TileEntity.PLAYER
        tile.actor = self
        if tile.item_drop:
            self.inventory.append(tile.item_drop)
        tile.item_drop = None
        if self.game_scene.p_pressed:
            self.game_scene.get_path_to_mouse()
        if self.check_for_portals(tile):
            self.game_scene.change_area(tile.scenery)


    def get_damage_done(self, target):
        self.damage_done = (random.randint(self.damage[PlayerDamage.MIN],self.damage[PlayerDamage.MAX]) - target.flat_dr) * (1 - target.percent_dr)
        return self.damage_done
        

    def check_for_portals(self, tile):
        return tile.scenery and type(tile.scenery) == Portal and not tile.scenery.locked

    def combat_roll(self, target):
        hit = False
        attack_roll = random.randint(1, self.accuracy)
        return attack_roll >= target.defence

    def combat_miss(self):
        print(str(self.name) + " missed!")

    def do_player_combat(self, target):
        if self.can_act:
            if self.combat_roll(target):
                print("Gorbath's attack hit!")
                damage = self.get_damage_done(target)
                print(f"Gorbath did {damage} damage!")
                print(f"Goblin has {target.current_health} health left!")
                target.change_health(damage)
            else:
                self.combat_miss()

    def change_health(self, damage):
        self.current_health -= damage

            


    