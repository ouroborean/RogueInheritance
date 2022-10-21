import logging
import pytest
from shikkoku.app import App
from rogue.tilemap import TileMap
from rogue.tile import Tile, FloorTile, TileType, VoidTile
import random
logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s:%(relativeCreated)d:%(module)s:%(message)s")
logging.getLogger("PIL").setLevel(69) # turn off PIL logging

@pytest.fixture(scope="package")
def test_app():
    app = App("Test App", (50, 50))
    yield app
    
def test_shortest_path_g_cost_sort(test_app):
    
    tile_map = TileMap((10, 10))
    
    test_tiles = [tile_map.get_tile((0, i)) for i in range(10)]
    
    for i, tile in enumerate(test_tiles):
        tile.g_cost = 10 - i
    
    test_tiles.sort(key=lambda x: x.g_cost)
    
    assert test_tiles[0].g_cost == 1
    assert test_tiles[-1].g_cost == 10
    
def test_shortest_path_two_cost_sort(test_app):
    tile_map = TileMap((10, 10))
    test_tiles = [tile_map.get_tile((0, i)) for i in range(10)]
    
    for i, tile in enumerate(test_tiles):
        tile.h_cost = 10 - i
        tile.g_cost = random.randint(0, 3)
    
    test_tiles.sort(key= lambda x: (x.f_cost, x.g_cost))
    
    for i, tile in enumerate(test_tiles):
        if i < len(test_tiles) - 1:
            assert tile.f_cost <= test_tiles[i + 1].f_cost
            if tile.f_cost == test_tiles[i + 1].f_cost:
                assert tile.g_cost <= test_tiles[i + 1].g_cost

def test_shortest_path_execution(test_app):
    tile_map = TileMap((10, 10))
    
    for i in range(100):
        tile_map.add_tile(FloorTile("grasstile.png"), tile_map.num_to_coord(i))
    
    start_tile = tile_map.get_tile((0, 0))
    end_tile = tile_map.get_tile((4, 3))
    # 1, 1 - 2, 2 - 3, 2 - 4, 3
    
    
    expected_path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 3)]
    path = tile_map.get_shortest_path(start_tile, end_tile)
    
    for i, tile in enumerate(path):
        assert tile.loc == expected_path[i]
        
def test_shortest_path_execution_with_wall(test_app):
    tile_map = TileMap((10, 10))
    
    for i in range(100):
        tile_map.add_tile(FloorTile("grasstile.png"), tile_map.num_to_coord(i))
    tile_map.add_tile(VoidTile(), (2, 2))
    start_tile = tile_map.get_tile((0, 0))
    end_tile = tile_map.get_tile((4, 3))
    expected_path = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3)]
    path = tile_map.get_shortest_path(start_tile, end_tile)
    for i, tile in enumerate(path):
        assert tile.loc == expected_path[i]
    
def test_shortest_path_execution_with_annoying_wall(test_app):
    tile_map = TileMap((10, 10))
    for i in range(100):
        tile_map.add_tile(FloorTile("grasstile.png"), tile_map.num_to_coord(i))
    tile_map.add_tile(VoidTile(), (2, 0))
    tile_map.add_tile(VoidTile(), (2, 1))
    tile_map.add_tile(VoidTile(), (2, 3))
    tile_map.add_tile(VoidTile(), (2, 4))
    tile_map.add_tile(VoidTile(), (3, 1))
    tile_map.add_tile(VoidTile(), (3, 2))
    tile_map.add_tile(VoidTile(), (3, 3))
    tile_map.add_tile(VoidTile(), (3, 4))
    tile_map.add_tile(VoidTile(), (4, 4))
    tile_map.add_tile(VoidTile(), (5, 2))
    tile_map.add_tile(VoidTile(), (5, 3))
    tile_map.add_tile(VoidTile(), (5, 4))
    
    start_tile = tile_map.get_tile((0, 0))
    end_tile = tile_map.get_tile((4, 3))
    expected_path = [(0, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5), (5, 5), (6, 4), (6, 3), (6, 2), (5, 1), (4, 2), (4, 3)]
    
    path = tile_map.get_shortest_path(start_tile, end_tile)
    
    for i, tile in enumerate(path):
        assert tile.loc == expected_path[i]
        
    tile_map.add_tile(FloorTile("grasstile.png"), (3, 1))
    path = tile_map.get_shortest_path(start_tile, end_tile)
    expected_path = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 2), (4, 3)]
    for i, tile in enumerate(path):
        assert tile.loc == expected_path[i]

def test_no_path_handling(test_app):
    tile_map = TileMap((10, 10))
    for i in range(100):
        tile_map.add_tile(FloorTile("grasstile.png"), tile_map.num_to_coord(i))
    tile_map.add_tile(VoidTile(), (2, 0))
    tile_map.add_tile(VoidTile(), (2, 1))
    tile_map.add_tile(VoidTile(), (2, 2))
    tile_map.add_tile(VoidTile(), (2, 3))
    tile_map.add_tile(VoidTile(), (2, 4))
    tile_map.add_tile(VoidTile(), (2, 5))
    tile_map.add_tile(VoidTile(), (2, 6))
    tile_map.add_tile(VoidTile(), (2, 7))
    tile_map.add_tile(VoidTile(), (2, 8))
    tile_map.add_tile(VoidTile(), (2, 9))
    
    start = tile_map.get_tile((0, 0))
    end = tile_map.get_tile((4, 3))
    
    path = tile_map.get_shortest_path(start, end)
    assert not path