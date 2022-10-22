from rogue.actor import Actor
from rogue.statpool import Stat
import rogue.statpool
import enum
from rogue.tile import Tile, TileEntity
from rogue.tilemap import TileMap
import random
from rogue.direction import Direction, pos_to_direction

class NPCDamage(enum.IntEnum):
    MAX = 0
    MIN = 1
class NPC(Actor):
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])

    def __init__(self, max_health:int = 5):
        super().__init__()
        self.statpool = rogue.statpool.StatPool()
        self.max_health = max_health
        self.current_health = 5
        self.level = 1
        self.name = "Goblin"
        self.character_class = ""
        self.image = "rogueplayer.png"
        self.can_act = True
        self.can_move = True
        self.target_tile_loc = ()
        self.speed = 1.0
        self.accuracy = 50
        self.flat_dr = 0
        self.percent_dr = 0
        self.defence = 10
        self.damage = {
            NPCDamage.MAX : 3,
            NPCDamage.MIN : 1
        }
        self.actions = {
            TileEntity.ENEMY : self.npc_swap,
            TileEntity.TERRAIN : self.npc_stand,
            TileEntity.ALLY : self.npc_attack,
            TileEntity.EMPTY : self.npc_move,
            TileEntity.PLAYER : self.npc_attack
        }

    def change_health(self, damage):
        self.current_health -= damage

    def npc_think(self, tile):
        player_adj = self.check_adjacent_tiles(tile)
        if player_adj == False:
            print("Goblin is thinking about wandering...")
            self.npc_wander(tile)

    def get_random_direction(self):
        random_dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)])
        print(random_dir)
        if not random_dir == (0,0):
            return random_dir
        else:
            self.get_random_direction()


    def npc_wander(self, tile_start):
        print("Goblin is checking a tile in the chosen direction!")
        self.check_npc_bump(tile_start.neighbor[pos_to_direction[self.get_random_direction()]], tile_start)
        

    def check_npc_bump(self, tile_target, tile_start):
        self.actions[tile_target.entity](tile_target, tile_start)
        
    def check_adjacent_tiles(self, tile):
        for adj_tile in tile.neighbor.values():
            if adj_tile.entity == TileEntity.PLAYER:
                print("True")
                self.check_npc_bump(adj_tile, tile)
                return True
        return False
                

    def npc_attack(self, target, tile):
        print(f"Goblin attacking {target.actor.name}") 
        self.do_npc_combat(target.actor)   

    def get_damage_done(self, target):
        self.damage_done = (random.randint(self.damage[NPCDamage.MIN],self.damage[NPCDamage.MAX]) - target.flat_dr) * (1 - target.percent_dr)
        return self.damage_done

    def combat_roll(self, target):
        hit = False
        attack_roll = random.randint(1, self.accuracy)
        return attack_roll >= target.defence

    def combat_miss(self):
        print(str(self.name) + " missed!")

    def do_npc_combat(self, target):
        if self.can_act:
            if self.combat_roll(target):
                print("Attack hit!")
                damage = self.get_damage_done(target)
                print(f"Did {damage} damage!")
                target.change_health(damage)
                print(f"Gorbath has {target.current_health} health left!")
            else:
                self.combat_miss()

    def npc_swap(self, tile_target, tile_start):
        pass

    def npc_stand(self, tile_target, tile_start):
        print("Goblin hits a wall and stands there!")
        pass

    def npc_move(self, tile_target, tile_start):
        tile_target.entity = TileEntity.ENEMY
        tile_target.actor = self
        tile_target.actor.is_new = True
        diff = (tile_target.loc[0] - self.loc[0], tile_target.loc[1] - self.loc[1])
        self.loc = self + diff
        tile_start.entity = TileEntity.EMPTY
        tile_start.actor = None
        

        
