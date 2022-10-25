from itertools import count
from multiprocessing import Event
from os import popen
from re import X
import string
from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext
import rogue.statpool
from rogue.statpool import Stat
import sdl2.ext
import sdl2.sdlttf
from rogue.tile import FloorTile, Tile, TileType, TileEntity, VoidTile
from rogue.tilemap import TileMap
from rogue.cc_scene import CCScene
from PIL import Image
from rogue.equipment import Equipment, Slot
from rogue.npc import NPC
import importlib.resources
from rogue.player import Player
import ctypes
from rogue.direction import direction_to_pos, pos_to_direction, Direction
from rogue.area import area_db
import enum
import functools
from sdl2 import SDL_bool

@enum.unique
class Menu(enum.IntEnum):
    NONE = 0
    INVENTORY = 1
    SKILLS = 2
    OPTIONS = 3
    EQUIP = 4

class equip_slot(enum.IntEnum):
    HEAD = 0
    SHOULDERS = 1
    CHEST = 2
    HANDS = 3
    LEGS = 4
    FEET = 5

def get_image_from_path(file_name: str) -> Image:
    with importlib.resources.path('rogue.resources', file_name) as path:
        return Image.open(path)
from rogue.scenery import Portal

FONTNAME = "Basic-Regular.ttf"

class GameScene(Scene):
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])


    def __init__(self, app, name):
        super().__init__(app, name)
        self.enemy_count = 0
        self.to_equip = None
        self.old_tile = (0, 0) 
        self.previous_x = 38
        self.cursor_x = 38
        self.cursor_y = 38
        self.direction_x = 0
        self.x_distance = 0
        self.y_distance = 0
        self.loc = (0, 0)
        self.previous_xy = (0, 0)
        self.direction_xy = (0, 0)
        self.previous_y = 38
        self.direction_y = 0
        self.target_radius = 1
        self.b_pressed = False
        self.to_inventory = None
        self.enemy_spawn_clicked = False
        self.p_pressed = False
        self.item_count = 0
        self.seen_tiles = { Tile }
        self.the_wheel = {
            0 : (0, -1),
            1 : (-1, 0),
            2 : (0, 1),
            3 : (1, 0),
            4 : (0, -1)
        }
        self.targets = []
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event
            # sdl2.SDL_MOUSEMOTION: self.handle_mouse_movement
            
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_z: self.press_z,
            sdl2.SDLK_p: self.press_p,
            sdl2.SDLK_b: self.press_b,
            sdl2.SDLK_w: self.press_up,
            sdl2.SDLK_KP_PLUS: self.press_plus,
            sdl2.SDLK_KP_MINUS: self.press_minus,
            sdl2.SDLK_a: self.press_left,
            sdl2.SDLK_s: self.press_down,            
            sdl2.SDLK_d: self.press_right,                        
            sdl2.SDLK_RIGHT: self.press_right,
            sdl2.SDLK_LEFT: self.press_left,
            sdl2.SDLK_UP: self.press_up,
            sdl2.SDLK_DOWN: self.press_down,
            sdl2.SDLK_SPACE: self.press_space
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.menu_state = {
            Menu.INVENTORY : False,
            Menu.SKILLS : False,
            Menu.OPTIONS : False,
            Menu.EQUIP : False
        }

        self.render_open_menu = {
            Menu.NONE : self.do_nothing,
            Menu.INVENTORY : self.render_inventory_menu,
            Menu.SKILLS : self.render_skill_menu,
            Menu.OPTIONS : self.render_options_menu,
            Menu.EQUIP : self.render_equip_menu
        }
        self.equip_slot_location = {
            Slot.HEAD : (0, 0),
            Slot.SHOULDERS : (74, 0),
            Slot.CHEST : (148, 0),
            Slot.HANDS : (0, 74),
            Slot.LEGS : (0, 148),
            Slot.FEET : (74, 74)
        }
        self.menu_toggle_switch = {
            Menu.INVENTORY : self.toggle_inventory_menu,
            Menu.SKILLS : self.do_nothing,
            Menu.OPTIONS : self.do_nothing,
            Menu.EQUIP : self.toggle_equip_menu
        }
        self.slot_image = self.image_to_surf(self.app.load("grid.png"))
        self.title_font = self.app.init_font(24, FONTNAME)
        self.button_font = self.app.init_font(10, FONTNAME)
        self.game_region = self.region.subregion(5, 5, 913, 588)
        self.button_region = self.region.subregion(1000, 500, 150, 150)
        self.mouse_cursor = self.make_button(self.image_to_surf(self.app.load("rogueplayer.png", width=50, height=50)))
        self.inventory_region = self.region.subregion(200, 200, 600, 300)
        self.hovered_tile = None
        self.tile_select = None
        self.grid_tile = self.app.load("grid.png")
        self.area = area_db["test"]
        self.tile_map = self.area.gen_tilemap()
        self.dest = None
        self.path = list()     

    def render_equip_menu(self):
        self.inventory_region.clear()
        background = self.make_panel(WHITE, self.inventory_region.size())
        self.inventory_region.add_sprite(background, 0, 0)
        for i in self.equip_slot_location.values():
            slot = self.make_button(self.image_to_surf(self.app.load("grid.png")))
            self.inventory_region.add_sprite(slot, i[0], i[1])
        for slot, gear in self.player.equipped.items():
            if gear:
                equip_sprite = self.make_sprite(self.app.load(gear.image, width=64, height=64))
                self.inventory_region.add_sprite(equip_sprite, self.equip_slot_location[slot][0], self.equip_slot_location[slot][1])

    def render_inventory_menu(self):
        self.inventory_region.clear()
        background = self.make_panel(WHITE, self.inventory_region.size())
        self.inventory_region.add_sprite(background, 0, 0)
        for i in range(16):
            row = i // 4
            column = i % 4
            inventory_slot = self.make_button(self.image_to_surf(self.app.load("grid.png")))
        #    inventory_slot.click += self.inventory_item
            inventory_slot.click += self.equip_item
            inventory_slot.item = None
            self.inventory_region.add_sprite(inventory_slot, 5 + column * 65 + (9*column), 5 + row * 65 + (9*row))
            if i + 1 <= len(self.player.inventory):
                if self.player.inventory[i] != None:
                    item_sprite = self.make_sprite(self.app.load(self.player.inventory[i].image, width=64, height=64))
                    self.inventory_region.add_sprite(item_sprite, 5 + column * 65 + (9*column), 5 + row * 65 + (9*row))
                    inventory_slot.item = self.player.inventory[i]

    def equip_item(self, button, event):
        if button.item:    
            print(f"Player currently equipped with {self.player.equipped[button.item.equip_slot]}")
            self.to_equip = button.item
            print(f"Transferring {button.item} to equipment!")
            self.to_inventory = self.player.equipped[button.item.equip_slot]
            self.player.equipped[self.to_equip.equip_slot] = self.to_equip
            print(f"Player equipped {self.player.equipped[self.to_equip.equip_slot].name}")
            print(f"Inventory: {self.player.inventory}")
            placeholder = self.player.inventory.index(self.to_equip)
            print(placeholder)
            self.player.inventory.insert(placeholder, self.to_inventory)
            print(f"Inventory: {self.player.inventory}")
            self.player.inventory.remove(self.player.inventory[placeholder + 1])
            print(self.player.inventory)
        # self.player.inventory.insert(placeholder, self.to_inventory)
        # self.player.inventory.remove(self.player.inventory[placeholder + 1])
        # self.render_game_region()
        
        # print(self.to_equip)
            
        # self.player.inventory.remove(self.player.inventory.index(self.to_equip))
            self.render_game_region()

    def inventory_item(self, button, event):
        print(button.item.name)
        print(button.item.stat_changes)
        # if self.player.inventory: 
        #     self.item_count = 0
        #     for i in self.player.inventory:
        #         row = self.item_count // 4
        #         column = self.item_count % 4
        #         item_sprite = self.make_sprite(self.app.load(i.image, width=64, height=64))
        #         self.inventory_region.add_sprite(item_sprite, 5 + column * 65 + (9*column), 5 + row * 65 + (9*row))
        #         self.item_count += 1

    def full_render(self):
        self.region.clear()
        background = self.make_panel(BLACK, (1200, 800))
        self.region.add_sprite(background, 0, 0)
        self.render_game_region()
        self.render_button_region()

        

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
            if self.enemy_spawn_clicked == True:
                tile_sprite.click += self.enemy_spawn
            else:
                tile_sprite.click += functools.partial(self.player.check_player_bump, self.tile_select)
            self.game_region.add_sprite(tile_sprite, 2 + column * 65, 2 + row * 65)
            if tile.scenery and tile.entity != TileEntity.PLAYER and tile.entity != TileEntity.ENEMY:
                scenery_sprite = self.make_sprite(self.app.load(tile.scenery.image, width=64, height=64))
                self.game_region.add_sprite(scenery_sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
            if tile.actor:
                if tile.actor.dead:
                    print(tile.actor.name + " died on " + str(tile.actor.loc))
                    tile.actor.item_drop.form_new_equipment()
                    tile.item_drop = tile.actor.item_drop
                    print(tile.item_drop.name)
                    print(tile.item_drop.stat_changes)
                    print(tile.item_drop.image)
                    item_sprite = self.make_sprite(self.app.load(tile.item_drop.image, width=64, height=64))
                    self.game_region.add_sprite(item_sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1]* 65)
                    if tile.actor in self.targets:
                        self.targets.remove(tile.actor)
                    tile.actor = None
                    tile.entity = TileEntity.EMPTY
                else:
                    actor_sprite = self.make_sprite(self.app.load(tile.actor.image, width = 64, height = 64))
                    self.game_region.add_sprite(actor_sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
                    tile.actor.loc = tile.loc
                    tile.entity = TileEntity.ENEMY
            if tile in self.path:
                path_panel = self.make_panel(PURPLE, (64, 64))
                self.game_region.add_sprite(path_panel, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
            elif tile in self.seen_tiles:
                path_panel = self.make_panel(RED, (64, 64))
                self.game_region.add_sprite(path_panel, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
            if tile.item_drop:
                item_sprite = self.make_sprite(self.app.load(tile.item_drop.image, width=64, height=64))
                self.game_region.add_sprite(item_sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1]* 65)
        
        self.tile_map.get_tile(self.player.loc).entity = TileEntity.PLAYER
        self.tile_map.get_tile(self.player.loc).actor = self.player
          
        character_sprite = self.make_sprite(self.app.load(self.player.image, width=64, height=64))
        self.game_region.add_sprite(character_sprite, 2 + self.player.loc[0] * 65, 2 + self.player.loc[1] * 65)

        if self.tile_map.get_tile(self.player.loc).scenery:
            self.tile_map.get_tile(self.player.loc).scenery = None
        self.render_open_menu[self.check_open_menu()]()

    def render_button_region(self):
        self.button_region.clear()
        background = self.make_panel(SILVER, self.button_region.size())
        bag_button = self.make_panel_button(BLACK, (60, 30))
        bag_button = self.render_bordered_text(self.button_font, "INVENTORY", BLACK, WHITE, bag_button, 4, 6, 1)
        bag_button.menu = Menu.INVENTORY
        bag_button.click += functools.partial(self.check_for_menus, Menu.INVENTORY)
        enemy_spawn_button = self.make_panel_button(BLACK, (60, 30))
        enemy_button_sprite = self.make_sprite(self.app.load("rogueplayer.png", width=20, height=30))
        enemy_spawn_button.click += self.enemy_spawn_button_click
        item_drop_button = self.make_panel_button(BLACK, (60, 30))
        equipment_button = self.make_panel_button(BLACK, (60, 30))
        equipment_button = self.render_bordered_text(self.button_font, "EQUIPMENT", BLACK, WHITE, equipment_button, 4, 6, 1)
        equipment_button.menu = Menu.EQUIP
        equipment_button.click += functools.partial(self.check_for_menus, Menu.EQUIP)
        options_button = self.make_panel_button(BLACK, (60, 30))
        options_button = self.render_bordered_text(self.button_font, "OPTIONS", BLACK, WHITE, options_button, 12, 6, 1)
        skills_button = self.make_panel_button(BLACK, (60, 30))
        skills_button = self.render_bordered_text(self.button_font, "SKILLS", BLACK, WHITE, skills_button, 16, 6, 1)
        self.button_region.add_sprite(background, 0, 0)
        self.button_region.add_sprite(bag_button, 10, 10)
        self.button_region.add_sprite(enemy_spawn_button, 80, 10)
        self.button_region.add_sprite(item_drop_button, 10, 50)
        self.button_region.add_sprite(equipment_button, 80, 50)
        self.button_region.add_sprite(options_button, 10, 90)
        self.button_region.add_sprite(skills_button, 80, 90) 
        self.button_region.add_sprite(enemy_button_sprite, 100, 10)       

    def do_nothing(self):
        pass

    def toggle_equip_menu(self):
        if self.menu_state[Menu.EQUIP] == True:
            self.menu_state[Menu.EQUIP] = False
        else:
            self.menu_state[Menu.EQUIP] = True
        self.inventory_region.clear()
        self.render_game_region()

    def check_for_menus(self, opening_menu : Menu, button, event):
        if self.menu_state[button.menu] == True:
            self.menu_toggle_switch[opening_menu]()
        else:
            for menu, state in self.menu_state.items():
                self.menu_state[menu] = False
                
            self.menu_toggle_switch[opening_menu]()

    def toggle_inventory_menu(self):
        if self.menu_state[Menu.INVENTORY] == True:
            self.menu_state[Menu.INVENTORY] = False
        else:
            self.menu_state[Menu.INVENTORY] = True
        self.inventory_region.clear()            
        self.render_game_region()

    def render_skill_menu(self):
        print("Skill Menu Opened!")
        pass

    def render_options_menu(self):
        print("Options Menu Opened!")
        pass

    def check_open_menu(self):
        for menu, state in self.menu_state.items():
            if state:
                return menu         
        return Menu.NONE

    def get_created_character(self):
        self.player = self.app.scenes["cc"].create_player()
        self.player.set_game_scene(self)

    def enemy_spawn_button_click(self, button, event):
        self.enemy_spawn_clicked = True

    def check_actors(self):
        for target in self.targets:
            target.turn_counter += self.player.speed
            while target.turn_counter >= target.speed:
                target.npc_think(self.send_tile(target))
                target.turn_counter -= target.speed  

    def send_tile(self, target):
        target_loc = self.tile_map.get_tile((target.loc))
        return target_loc
           
    def change_area(self, portal):
        self.path.clear()
        self.area = area_db[portal.area_dest]
        self.tile_map = self.area.gen_tilemap()
        for exit_portal in self.tile_map.portals:
            if exit_portal.id == portal.id:
                self.player.loc = exit_portal.loc
        self.full_render()

    def enemy_spawn(self, button, sender):
        self.tile_map.get_tile(button.tile.loc).entity = TileEntity.ENEMY
        self.tile_map.get_tile(button.tile.loc).actor = NPC()
        self.targets.append(self.tile_map.get_tile(button.tile.loc).actor)
        self.enemy_spawn_clicked = False

    def is_tile_seen(self, tile):
        for tile in self.seen_tiles:
            if self.tile_map.get_tile(self.loc) == tile:
                return True
        return False

    def move(self, direction):
        self.loc = self + direction
        self.seen_tiles.add(self.tile_map.get_tile(self.loc))        


    def spin_the_wheel(self, tile, radius):
        if tile:
            self.loc = (tile.loc)
            for spin in range(len(self.the_wheel)-1):
                for y in range(radius):
                    self.loc = tile.loc
                    for z in range(radius - y):
                        self.move(self.the_wheel[spin]) 
                    for a in range(y):
                        self.move(self.the_wheel[spin + 1])

    def press_minus(self, event):
        if self.b_pressed:
            if self.target_radius > 1:
                self.target_radius -= 1

    def press_plus(self, event):
        if self.b_pressed:
            self.target_radius += 1
        
    def press_b(self, event):
        self.b_pressed = not self.b_pressed
        # if self.b_pressed:
        #     self.spin_the_wheel(self.tile_map.get_tile(self.player.loc), 4)
        # else:
        #     self.seen_tiles.clear()
        self.render_game_region()
                
        

#region Tile Selection Functions
    def select_tile(self, button):
        if self.hovered_tile != button:
            self.hovered_tile = button
            self.path.clear()
            self.path.append(button)
            self.full_render()

    def move_over_tile(self, button):
        if self.hovered_tile != button:
            self.hovered_tile = button
            self.get_path_to_mouse()
            self.full_render()

    def get_path_to_mouse(self):
        if self.hovered_tile:
            self.path = self.tile_map.get_shortest_path(self.tile_map.get_tile(self.player.loc), self.hovered_tile)[1:]
#endregion
    
#region Keypress Functions





    def press_right(self, event):
        twople = self.player + direction_to_pos[Direction.EAST]
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.tile_map.get_tile(self.player.loc).entity = TileEntity.PLAYER        
        self.check_actors()
        self.render_game_region()
    
    def press_left(self, event):
        twople = self.player + direction_to_pos[Direction.WEST]      
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors() 
        self.render_game_region()        
        self.full_render()

    def press_up(self, event):
        twople = self.player + direction_to_pos[Direction.NORTH]
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors()
        self.render_game_region()
        self.full_render()       
    
    def press_down(self, event):
        twople = self.player + direction_to_pos[Direction.SOUTH]       
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors()  
        self.render_game_region()           
        self.full_render()   

    def press_p(self, event):
        print("P pressed!")
        self.p_pressed = not self.p_pressed
        if self.p_pressed:
            print("Path Mode turned ON, so now showing path to mouse!")
            self.get_path_to_mouse()
        else:
            if self.hovered_tile:
                print("Path Mode turned OFF, so now showing selected tile")
                self.path.clear()
                self.path.append(self.hovered_tile)
        self.render_game_region()

    def press_z(self, event):
        self.player.player_stand(self.tile_map.get_tile(self.player.loc))
        self.check_actors()  
        self.render_game_region()

#endregion
    
    def press_space(self, event):
        if self.path:
            direction_tuple = (0, 0)
            for direction, tile in self.tile_map.get_tile(self.player.loc).neighbor.items():
                if self.path[0] == tile:
                    direction_tuple = direction_to_pos[direction]
            twople = self.player + direction_tuple
            self.player.check_player_bump(self.tile_map.get_tile(twople))
            self.check_actors()            
            self.full_render()

 #region Arrow Keys Release Functions  
    def release_right(self, event):
        pass
    
    def release_left(self, event):
        pass
    
    def release_up(self, event):
        pass
    
    def release_down(self, event):
        pass
#endregion    
    
    def handle_mouse_movement(self, button, event):
        # self.cover_region.clear()
        # self.cover_region.add_sprite(self.mouse_cursor, event.motion.x - 25, event.motion.y - 25)        
        # self.previous_x = self.cursor_x
        # self.previous_y = self.cursor_y
        # self.x_distance = abs(self.previous_x - event.motion.x)
        # self.y_distance = abs(self.previous_y - event.motion.y)  
        # self.previous_x = event.motion.x
        # self.previous_y = event.motion.y
        # self.cursor_x += (event.motion.xrel * self.x_distance)
        # self.cursor_y += (event.motion.yrel * self.y_distance)
        # self.cover_region.add_sprite(mouse_cursor, self.app.mouse_x - 25, self.app.mouse_y - 25)
        # if self.previous_x == event.motion.x:
        #     self.direction_x = 0
        # elif self.previous_x < event.motion.x:
        #     self.direction_x = 1
        # elif self.previous_x > event.motion.x:
        #     self.direction_x = -1
        # if self.previous_y == event.motion.y:
        #     self.direction_y = 0
        # elif self.previous_y < event.motion.y:
        #     self.direction_y = 1
        # elif self.previous_y > event.motion.y:
        #     self.direction_y = -1
        # self.previous_xy = (self.previous_x, self.previous_y)
        # self.direction_xy = (self.direction_x, self.direction_y)
        # self.x_distance = abs(self.previous_x - event.motion.x)
        # self.y_distance = abs(self.previous_y - event.motion.y)
        # self.previous_x = event.motion.x
        # self.previous_y = event.motion.y
        # self.cursor_x += self.direction_x  + (self.direction_x * self.x_distance) - self.direction_x
        # self.cursor_y += self.direction_y + (self.direction_y * self.y_distance) - self.direction_y

        # self.render_cover_region()
        # print(self.direction_xy)
        # print(f"x = {event.motion.x} | y = {event.motion.y} | xrel = {event.motion.xrel} | yrel = {event.motion.yrel}")
        pass

#region Event Handlers    
    def handle_event(self, event):
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)
    
    def handle_key_down_event(self, event):
        if event.key.keysym.sym in self.key_down_event_handlers:
            self.key_down_event_handlers[event.key.keysym.sym](event)
    
    def handle_key_up_event(self, event):
        if event.key.keysym.sym in self.key_up_event_handlers:
            self.key_up_event_handlers[event.key.keysym.sym](event)
#endregion
    
    def update_scene_state(self):
        # self.cover_region.clear()
        # self.cover_region.add_sprite(self.mouse_cursor, self.app.mouse_x - 25, self.app.mouse_y - 25)  
        tile_x = (self.app.mouse_x - 7) // 65
        tile_y = (self.app.mouse_y - 7) // 65
        self.seen_tiles.clear()
        if self.p_pressed:
            self.tile_select = (self.tile_map.get_tile((tile_x, tile_y)))
            self.move_over_tile(self.tile_map.get_tile((tile_x, tile_y)))
        else:
            self.tile_select = (self.tile_map.get_tile((tile_x, tile_y))) 
            self.select_tile(self.tile_select) 

        if self.b_pressed:
            self.spin_the_wheel(self.hovered_tile, self.target_radius)
        else:
            self.seen_tiles.clear()
        self.render_game_region() 
        # self.previous_x = self.cursor_x
        # self.previous_y = self.cursor_y
        # self.x_distance = abs(self.previous_x - self.app.mouse_x)
        # self.y_distance = abs(self.previous_y - self.app.mouse_y)  
        # self.previous_x = self.app.mouse_x
        # self.previous_y = self.app.mouse_y
        # self.cursor_x += (self.app.mouse_xrel * self.x_distance)
        # self.cursor_y += (self.app.mouse_yrel * self.y_distance)
        # self.render_cover_region()


        
            