
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
    portals: list
    tilemap: TileMap
    
    def __init__(self, dimensions: tuple):
        self.floor_tiles = dict()
        self.terrain_tiles = dict()
        self.flavor_tiles = dict()
        self.enemy_spawns = dict()
        self.prefabs = dict()
        self.portals = list()
        self.style = AreaStyle.SCATTER
        self.border_style = BorderStyle.VOID
        self.clutter_seed = 25
        self.tilemap = None
        self.dimensions = dimensions
        
    
    def gen_tilemap(self) -> "TileMap":
        if self.tilemap:
            print("Returning pre-genned tilemap")
            return self.tilemap
        else:
            print("Genning Tilemap")
            tilemap = TileMap(self.dimensions)
            
            tilemap.carpet_tile_map(self.floor_tiles)
            tilemap.add_terrain(self.terrain_tiles, self.clutter_seed)
            tilemap.add_portals(self.portals)
            if self.border_style == BorderStyle.TERRAIN:
                tilemap.border_tile_map(self.terrain_tiles[list(self.terrain_tiles.keys())[0]])
            elif self.border_style == BorderStyle.VOID:
                tilemap.void_border()
            self.tilemap = tilemap
            return tilemap
    
    
forest_floor_tiles = {65: ("grasstile.png",), 35: ("dirttile.png",)}
forest_terrain_tiles = {75: ("treetile.png", ("SOLID", "OPAQUE")), 15: ("bush.png", ("SOLID",)), 10: ("rock.png", ("SOLID",))}


def make_test_area():
    area = Area((14, 9))
    print("Making test area")
    area.floor_tiles = forest_floor_tiles
    area.terrain_tiles = forest_terrain_tiles
    area.border_style = BorderStyle.TERRAIN
    #protocol for adding portals:
    # List of tuples, each tuple covering a single portal
    # ( (Either Coordinates for the static location of the portal or a tuple of two coordinates for a range of random possible locations), (constructor arguments for the portal Scenery object))
    area.portals = [ ( ( (12, 7), ), ("doortile.png", list(), 0, "test2") ) ]
    return area

def make_second_test_area():
    area = Area((14, 9))
    print("Making test area 2")
    area.floor_tiles = forest_floor_tiles
    area.terrain_tiles = forest_terrain_tiles
    area.border_style = BorderStyle.TERRAIN
    #protocol for adding portals:
    # List of tuples, each tuple covering a single portal
    # ( (Either Coordinates for the static location of the portal or a tuple of two coordinates for a range of random possible locations), (constructor arguments for the portal Scenery object))
    area.portals = [ ( ( (2, 2), (3, 6) ), ("doortile.png", list(), 0, "test") ) ]
    return area

area_db = {
    "test": make_test_area(),
    "test2": make_second_test_area(),
}


