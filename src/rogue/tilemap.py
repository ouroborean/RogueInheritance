from rogue.tile import Tile, VoidTile
from rogue.direction import Direction, offset_direction

from typing import Tuple

class TileMap():
    
    
    tiles: list[Tile]
    width: int
    height: int
    
    def __init__(self, dimensions: Tuple[int, int]):
        self.width, self.height = dimensions
        self.tiles = [None] * (self.width * self.height)
        
        for i, tile in enumerate(self.tiles):
            self.add_tile(VoidTile(), i)
        
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
        else:
            print(f"{coord} is not a valid tile")
            return None
        
    def num_to_coord(self, num: int) -> Tuple[int, int]:
        return (num % self.width, num // self.width)
    
    def coord_to_num(self, coord: Tuple[int, int]) -> int:
        return coord[0] + (coord[1] * self.width)
