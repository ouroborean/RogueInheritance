from rogue.direction import Direction, counter_direction
from typing import Tuple
import enum

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


    def set_loc(self, location):
        self.loc = location
    
    def set_neighbor(self, direction, tile):
        self.neighbor[direction] = tile
        tile.neighbor[counter_direction(direction)] = self
    
class VoidTile(Tile):
    
    def __init__(self):
        super().__init__()
        self.types.add(TileType.OPAQUE)
        self.types.add(TileType.SOLID)
        self.types.add(TileType.INVIOLABLE)
        
        