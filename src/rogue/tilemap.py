from rogue.tile import Tile, VoidTile, TileType, FloorTile
from rogue.direction import Direction, offset_direction
from rogue.scenery import Scenery
import random
from typing import Tuple

class TileMap():
    
    
    tiles: list[Tile]
    width: int
    height: int
    
    def __init__(self, dimensions: Tuple[int, int]):
        self.width, self.height = dimensions
        self.tiles = [None] * (self.width * self.height)
    
    def is_border_tile(self, i) -> bool:
        return i % self.width == 0 or i % self.width == self.width - 1 or i // self.width == 0 or i // self.width == self.height - 1
        
    def valid_coord(self, coord) -> bool:
        return (coord[0] + (coord[1] * self.width)) >= 0 and (coord[0] + (coord[1] * self.width)) < (self.width*self.height) and coord[0] < self.width and coord[1] < self.height and coord[0] >= 0 and coord[1] >= 0
    
    def add_tile(self, tile:Tile, location:Tuple):
        
        if isinstance(location, Tuple):
            true_loc = location
            num_loc = self.coord_to_num(location)
        elif isinstance(location, int):
            true_loc = self.num_to_coord(location)
            num_loc = location
        
        x = (-1, 0, 1)
        y = (-1, 0, 1)
        
        tile.set_loc(true_loc)
        
        neighbors = 0
        for offset1 in x:
            offset_x = true_loc[0] + offset1
            for offset2 in y:
                offset_y = true_loc[1] + offset2
                if not (offset1, offset2) == (0, 0) and self.get_tile((offset_x, offset_y)):
                    
                    tile.set_neighbor(offset_direction((offset1, offset2)), self.get_tile((offset_x, offset_y)))
                    neighbors += 1
                    
        self.tiles[num_loc] = tile
        
    def get_tile(self, coord: Tuple[int, int]) -> Tile:
        if self.valid_coord(coord):
            return self.tiles[coord[0] + (coord[1] * self.width)]

    def get_shortest_path(self, start, end) -> list[Tile]:
        open_nodes = list()
        closed_nodes = set()
        open_nodes.append(start)  
        ROOK_TILES = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)
        BISHOP_TILES = (Direction.NORTHEAST, Direction.NORTHWEST, Direction.SOUTHEAST, Direction.SOUTHWEST)
        while True:
            open_nodes.sort(key= lambda x: (x.f_cost, x.h_cost))
            if not open_nodes:
                return []
            current = open_nodes.pop(0)
            closed_nodes.add(current)
            if current == end:
                break
            for direction, node in current.neighbor.items():
                if node and node.walkable:
                    if node in closed_nodes:
                        continue
                    if direction in ROOK_TILES:
                        path_length = 10
                    elif direction in BISHOP_TILES:
                        path_length = 14
                    if current.g_cost + path_length < node.g_cost or not node in open_nodes:
                        node.set_g_cost(current.g_cost + path_length)
                        node.set_h_cost(end)
                        node.parent = current
                        if not node in open_nodes:
                            open_nodes.append(node)
        output = [end]
        while not start in output:
            output.append(output[-1].parent)
        output.reverse()
        return output
    
    def carpet_tile_map(self, tiles):
        for i in range(self.width * self.height):
            roll = random.randint(1, 100)
            for weight, details in tiles.items():
                if roll <= weight:
                    self.add_tile(FloorTile(*details), self.num_to_coord(i))
                    break
                else:
                    roll -= weight
        
    def border_tile_map(self, args):
        for i in range(self.width * self.height):
            if i % self.width == 0 or i % self.width == self.width - 1 or i // self.width == 0 or i // self.width == self.height - 1:
                self.get_tile(self.num_to_coord(i)).apply_scenery(Scenery(*args))
                
    def void_border(self):
        for i in range(self.width * self.height):
            if i % self.width == 0 or i % self.width == self.width - 1 or i // self.width == 0 or i // self.width == self.height - 1:
                self.add_tile(VoidTile(), self.num_to_coord(i))
    
    def add_terrain(self, scenery, clutter_seed):
        for i in range(self.width * self.height):
            if not self.is_border_tile(i):
                print("Rolling for random terrain")
                roll = random.randint(1, 100)
                if roll <= clutter_seed:
                    roll = random.randint(1, 100)
                    for weight, details in scenery.items():
                        print("Rolling for WHICH random terrain!")
                        if roll <= weight:
                            self.get_tile(self.num_to_coord(i)).apply_scenery(Scenery(*details))
                            break
                        else:
                            roll -= weight
    
    def num_to_coord(self, num: int) -> Tuple[int, int]:
        return (num % self.width, num // self.width)
    
    def coord_to_num(self, coord: Tuple[int, int]) -> int:
        return coord[0] + (coord[1] * self.width)
