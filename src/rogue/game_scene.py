import string
from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext

from rogue.tile import FloorTile, TileType
from rogue.tilemap import TileMap
from rogue.cc_scene import CCScene

FONTNAME = "Basic-Regular.ttf"

class GameScene(Scene):
    
    def __init__(self, app, name):
        super().__init__(app, name)
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_RIGHT: self.press_right,
            sdl2.SDLK_LEFT: self.press_left,
            sdl2.SDLK_UP: self.press_up,
            sdl2.SDLK_DOWN: self.press_down,
            
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.title_font = self.app.init_font(24, FONTNAME)
        self.game_region = self.region.subregion(5, 5, 912, 609)
        
        self.grid_tile = self.app.load("grid.png")
        self.tile_map = TileMap((9, 6))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (1, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (2, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (3, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (4, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (5, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (6, 1))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (7, 1))
        
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (1, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (2, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (3, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (4, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (5, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (6, 2))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (7, 2))
        
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (1, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (2, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (3, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (4, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (5, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (6, 3))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (7, 3))
        
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (1, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (2, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (3, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (4, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (5, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (6, 4))
        self.tile_map.add_tile(FloorTile("grasstile.png", [TileType.WALKABLE,]), (7, 4))
        
        
        
    def full_render(self):
        background = self.make_panel(BLACK, (1200, 800))
        self.region.add_sprite(background, 0, 0)
        
        self.render_game_region()
        self.get_created_character()
    
    def render_game_region(self):
        self.game_region.clear()
        background = self.make_panel(SILVER, self.game_region.size())
        self.game_region.add_sprite(background, 0, 0)
        
        WIDTH_IN_TILES = 9
        
        for i in range(54):
            row = i // WIDTH_IN_TILES
            column = i % WIDTH_IN_TILES
            grid = self.make_sprite(self.grid_tile)
            self.game_region.add_sprite(grid, 1 + column * 101, 1 + row * 101)
            tile = self.tile_map.get_tile((column, row))
            tile_sprite = self.make_sprite(self.app.load(tile.image))
            self.game_region.add_sprite(tile_sprite, 2 + column * 101, 2 + row * 101)
    
    def get_created_character(self):
        self.character_class = self.app.scenes["cc"].send_chosen_class()

    def press_right(self, event):
        pass
    
    def press_left(self, event):
        pass

    def press_up(self, event):
        pass
    
    def press_down(self, event):
        pass
        
    def release_right(self, event):
        pass
    
    def release_left(self, event):
        pass
    
    def release_up(self, event):
        pass
    
    def release_down(self, event):
        pass
    
    def handle_event(self, event):
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)
    
    def handle_key_down_event(self, event):
        if event.key.keysym.sym in self.key_down_event_handlers:
            self.key_down_event_handlers[event.key.keysym.sym](event)
    
    def handle_key_up_event(self, event):
        if event.key.keysym.sym in self.key_up_event_handlers:
            self.key_up_event_handlers[event.key.keysym.sym](event)
    
    def update_scene_state(self):
        pass
            