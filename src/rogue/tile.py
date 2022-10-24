from rogue.direction import Direction, counter_direction
from rogue.scenery import Scenery, SceneryType, Portal
from typing import Tuple, Callable
import enum
import typing
from rogue.equipment import Equipment

if typing.TYPE_CHECKING:
    from rogue.actor import Actor
    from rogue.game_object import GameObject
    
    
@enum.unique
class TileType(enum.IntEnum):
    WALKABLE = 0
    OPAQUE = 1
    SOLID = 2
    INVIOLABLE = 3

@enum.unique
class TileEntity(enum.IntEnum):
    ENEMY = 0
    TERRAIN = 1
    ALLY = 2
    EMPTY = 3
    PLAYER = 4

class Tile():
    
    loc: Tuple[int, int]
    types: set[TileType]
    neighbor: dict[Direction, "Tile"]
    actor: "Actor"
    game_objects: list["GameObject"]
    scenery: "Scenery"
    g_cost: int
    h_cost: int
    path_parent: "Tile"
    
    def __init__(self):
        self.actor_added = False
        self.g_cost = 0
        self.h_cost = 0
        self.item_drop: Equipment()
        self.types = set()
        self.neighbor = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None,
            Direction.SOUTHEAST: None,
            Direction.NORTHEAST: None,
            Direction.NORTHWEST: None,
            Direction.SOUTHWEST: None
        }
        self.entity = TileEntity.EMPTY
        self.player = None
        self.actor = None
        self.game_objects = list()
        self.scenery = None
        self.path_parent = None

    def get_entity_state(self):
        return self.entity

    def set_g_cost(self, cost):
        self.g_cost = cost

    def set_h_cost(self, tile):
        self.h_cost = self.distance_to_tile(tile)
    
    def distance_to_tile(self, tile):
        x_diff = abs(self.loc[0] - tile.loc[0])
        y_diff = abs(self.loc[1] - tile.loc[1])
        return (min(x_diff, y_diff) * 14) + (abs(x_diff - y_diff) * 10)

    @property
    def walkable(self) -> bool:
        return TileType.WALKABLE in self.types and (not self.scenery or SceneryType.WALKABLE in self.scenery.types) and not self.entity == TileEntity.ENEMY
    
    @property
    def f_cost(self) -> int:
        return self.g_cost + self.h_cost
    
    def set_loc(self, location):
        self.loc = location

    def check_actor(self):
        pass
        
    def add_game_object(self, obj):
        self.game_objects.append(obj)
    
    def apply_scenery(self, scenery):
        self.scenery = scenery
        if type(scenery) == Portal:
            self.entity = TileEntity.EMPTY
        else:
            self.entity = TileEntity.TERRAIN
    
    def remove_scenery(self):
        self.scenery = None
        self.entity = TileEntity.EMPTY
    
    def add_actor(self, actor):
        self.actor = actor
    
    def set_neighbor(self, direction, tile):
        self.neighbor[direction] = tile
        tile.neighbor[counter_direction(direction)] = self
    
class VoidTile(Tile):
    
    def __init__(self):
        super().__init__()
        self.image = "voidtile.png"
        self.types.add(TileType.OPAQUE)
        self.types.add(TileType.SOLID)
        self.types.add(TileType.INVIOLABLE)
        self.entity = TileEntity.TERRAIN
        
        
class FloorTile(Tile):
    
    def __init__(self, image, tile_types = set()):
        super().__init__()
        self.image = image
        self.item_drop = None
        self.types = tile_types
        self.types.add(TileType.WALKABLE)
        for tile_type in tile_types:
            self.types.add(tile_type)


