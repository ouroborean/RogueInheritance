from itertools import count
from os import popen
import string
from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext
import rogue.statpool
from rogue.statpool import Stat
from rogue.tile import FloorTile, Tile, TileType, TileEntity, VoidTile
from rogue.tilemap import TileMap
from rogue.cc_scene import CCScene
from rogue.npc import NPC
from rogue.player import Player
from rogue.direction import direction_to_pos, Direction
from rogue.area import area_db

FONTNAME = "Basic-Regular.ttf"

class GameScene(Scene):
    

    def __init__(self, app, name):
        super().__init__(app, name)
        self.enemy_count = 0
        self.targets = []
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_z: self.press_z,
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
        self.game_region = self.region.subregion(5, 5, 913, 588)
        self.hovered_tile = None
        self.grid_tile = self.app.load("grid.png")
        
        self.area = area_db["test"]
        self.tile_map = self.area.gen_tilemap((14, 9))
        
        self.dest = None
        self.enemy_loc = (1, 1)
        self.path = list()        
        
    def full_render(self):
        self.region.clear()
        background = self.make_panel(BLACK, (1200, 800))
        self.region.add_sprite(background, 0, 0)
        self.render_game_region()

    def render_game_region(self):
        self.game_region.clear()
        background = self.make_panel(SILVER, self.game_region.size())
        self.game_region.add_sprite(background, 0, 0)
        WIDTH_IN_TILES = self.tile_map.width
        
        all_tiles = self.tile_map.width * self.tile_map.height
        for i in range(all_tiles):
            row = i // WIDTH_IN_TILES
            column = i % WIDTH_IN_TILES
            grid = self.make_sprite(self.grid_tile)
            self.game_region.add_sprite(grid, 1 + column * 65, 1 + row * 65)
            tile = self.tile_map.get_tile((column, row))
            tile_sprite = self.make_button(self.image_to_surf(self.app.load(tile.image, width=64, height=64)))
            tile_sprite.tile = tile
            tile_sprite.motion += self.move_over_tile
            self.game_region.add_sprite(tile_sprite, 2 + column * 65, 2 + row * 65)
            if tile.actor:
                if tile.actor.is_new == True:
                    self.targets.append(tile.actor)
                    tile.actor.is_new == False
                if tile.actor.dead:
                    print("To do: Handle Loot")
                    self.targets.remove(tile.actor)
                    tile.actor = None
                    tile.entity = TileEntity.EMPTY
                else:
                    actor_sprite = self.make_sprite(self.app.load(tile.actor.image, width = 64, height = 64))
                    self.game_region.add_sprite(actor_sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
                    tile.actor.loc = tile.loc
                    tile.entity = TileEntity.ENEMY
            
            # self.targets.clear()
            # if tile.actor:
            #     actor_sprite = self.make_sprite(self.app.load(tile.actor.image, width = 64, height = 64))
            #     self.game_region.add_sprite(actor_sprite, 2 + tile.actor.loc[0] * 65, 2 + tile.actor.loc[1] * 65)
            #     self.targets.append(tile.actor)
            #     tile.actor.loc = tile.loc
            #     tile.entity = TileEntity.ENEMY
            

        self.tile_map.get_tile(self.player.loc).entity = TileEntity.PLAYER
        self.tile_map.get_tile(self.player.loc).actor = self.player
          
        character_sprite = self.make_sprite(self.app.load(self.player.image, width=64, height=64))
        self.game_region.add_sprite(character_sprite, 2 + self.player.loc[0] * 65, 2 + self.player.loc[1] * 65)

    def get_created_character(self):
        self.player = self.app.scenes["cc"].create_player()

    def press_z(self, event):
        self.player.player_stand(self.tile_map.get_tile(self.player.loc))
        self.full_render()

    def press_right(self, event):
        twople = self.player + direction_to_pos[Direction.EAST]
        home_tile = self.tile_map.get_tile(self.player.loc)
        home_tile.entity = 3
        home_tile.actor = None
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.full_render()
        print(self.tile_map.get_tile(self.player.loc).entity)
    
    def move_over_tile(self, button, sender):
        if self.hovered_tile != button.tile:
            self.hovered_tile = button.tile
            self.path = self.tile_map.get_shortest_path(self.tile_map.get_tile((self.enemy_loc)), self.hovered_tile)[1:]
            self.full_render()
    
    def press_left(self, event):
        twople = self.player + direction_to_pos[Direction.WEST]
        home_tile = self.tile_map.get_tile(self.player.loc)
        home_tile.entity = 3
        home_tile.actor = None        
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.full_render()
        print(self.tile_map.get_tile(self.player.loc).entity)

    def press_up(self, event):
        twople = self.player + direction_to_pos[Direction.NORTH]
        home_tile = self.tile_map.get_tile(self.player.loc)
        home_tile.actor = None
        home_tile.entity = 3
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.full_render()
        print(self.tile_map.get_tile(self.player.loc).entity)        
    
    def press_down(self, event):
        twople = self.player + direction_to_pos[Direction.SOUTH]
        home_tile = self.tile_map.get_tile(self.player.loc)
        home_tile.actor = None
        home_tile.entity = 3        
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.full_render()
        print(self.tile_map.get_tile(self.player.loc).entity)        
        
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

    def send_tile(self, target):
        target_loc = self.tile_map.get_tile((target.loc))
        return target_loc

    
    def update_scene_state(self):
        for target in self.targets:
            if self.player.turn_counter >= target.speed:
                target.npc_think(self.send_tile(target))
                self.targets.remove(target)
                self.player.turn_counter -= target.speed  
                self.render_game_region()
        
            