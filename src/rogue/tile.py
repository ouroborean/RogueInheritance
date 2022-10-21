from rogue.direction import Direction, counter_direction
from typing import Tuple
import enum
import typing

if typing.TYPE_CHECKING:
    from rogue.actor import Actor
    from rogue.game_object import GameObject
    from rogue.scenery import Scenery



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

class Tile():
    
    loc: Tuple[int, int]
    types: set[TileType]
    neighbor: dict[Direction, "Tile"]
    entity: dict[TileEntity, function()]
    actor: "Actor"
    game_objects: list["GameObject"]
    scenery: "Scenery"
    
    def __init__(self):
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
        self.entity = {
            
        }
        self.actor = None
        self.game_objects = list()
        self.scenery = None
    
    def set_loc(self, location):
        self.loc = location
        
    def add_game_object(self, obj):
        self.game_objects.append(obj)
    
    def apply_scenery(self, scenery):
        self.scenery = scenery
        
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
        
        
class FloorTile(Tile):
    
    def __init__(self, image, tile_types):
        super().__init__()
        self.image = image
        for tile_type in tile_types:
            self.types.add(tile_type)


