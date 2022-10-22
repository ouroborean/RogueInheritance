from rogue.prefab import Prefab
import random
import enum
import typing
from rogue.scenery import SceneryType, Scenery
from rogue.tilemap import TileMap

@enum.unique
class AreaStyle(enum.IntEnum):
    SCATTER = 0
    LINK = 1

class BorderStyle(enum.IntEnum):
    VOID = 0
    TERRAIN = 1
    WATER = 2


class Area():
    
    floor_tiles: dict[int, tuple]
    terrain_tiles: dict[int, tuple]
    flavor_tiles: dict[int, tuple]
    enemy_spawns: dict[int, tuple]
    prefabs: dict[int, Prefab]
    style: AreaStyle
    border_style: BorderStyle
    clutter_seed: int
    
    def __init__(self):
        self.floor_tiles = dict()
        self.terrain_tiles = dict()
        self.flavor_tiles = dict()
        self.enemy_spawns = dict()
        self.prefabs = dict()
        self.style = AreaStyle.SCATTER
        self.border_style = BorderStyle.VOID
        self.clutter_seed = 25
        
    
    
    def gen_tilemap(self, dimensions: tuple) -> "TileMap":
        tilemap = TileMap(dimensions)
        
        tilemap.carpet_tile_map(self.floor_tiles)
        tilemap.add_terrain(self.terrain_tiles, self.clutter_seed)
            
        if self.border_style == BorderStyle.TERRAIN:
            tilemap.border_tile_map(self.terrain_tiles[list(self.terrain_tiles.keys())[0]])
        elif self.border_style == BorderStyle.VOID:
            tilemap.void_border()
        
        
        
        return tilemap
    
forest_floor_tiles = {65: ("grasstile.png",), 35: ("dirttile.png",)}
forest_terrain_tiles = {75: ("treetile.png", (SceneryType.SOLID, SceneryType.OPAQUE)), 15: ("bush.png", (SceneryType.SOLID,)), 10: ("rock.png", (SceneryType.SOLID,))}

area_db = {
    "test": Area()
}
area_db["test"].floor_tiles = forest_floor_tiles
area_db["test"].terrain_tiles = forest_terrain_tiles
area_db["test"].border_style = BorderStyle.TERRAIN

