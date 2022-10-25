from shikkoku.engine import Scene
from shikkoku.color import *
from shikkoku.text_formatter import *
import sdl2.ext
import sdl2
import importlib.resources
import typing
import rogue.player
from PIL import Image
from rogue.statpool import StatPool, Stat
from rogue.playerclass import PlayerClass, class_primary_colors, class_secondary_colors

FONTNAME = "Basic-Regular.ttf"


def get_image_from_path(file_name: str) -> Image:
    with importlib.resources.path('rogue.resources', file_name) as path:
        return Image.open(path)

class CCScene(Scene):
    
    def __init__(self, app, name):
        super().__init__(app, name)
        self.player = rogue.player.Player()
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event,
            sdl2.SDL_MOUSEBUTTONUP: self.mouse_left_up,
            sdl2.SDL_MOUSEBUTTONDOWN: self.mouse_left_down
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_RIGHT: self.press_right,
            sdl2.SDLK_LEFT: self.press_left,
            sdl2.SDLK_UP: self.press_up,
            sdl2.SDLK_DOWN: self.press_down
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.background_region = self.region.subregion(30, 30, 1140, 740)
        self.character_name_region = self.region.subregion(50, 50, 270, 80)
        self.stat_region = self.region.subregion(50, 150, 270, 540)
        self.class_region = self.region.subregion(340, 50, 270, 640)
        self.picture_region = self.region.subregion(830, 250, 100, 100)
        self.options_region = self.region.subregion(340, 700, 520, 60)
        self.title_font = self.app.init_font(24, FONTNAME)
        self.smaller_font = self.app.init_font(16, FONTNAME)
        self.char_name_font = self.app.init_font(20, FONTNAME)
        #region Class Button Regions
        
        self.class_button_regions = [self.region.subregion(350, 80 + (i * 110), 250, 80) for i in range(4)]
        
        #endregion
        #region Stat Buttons
        self.stat_up_buttons = list()
        for i in range(5):
            button = self.make_panel_button(BLACK, (20, 20))
            button = self.border_sprite(button, WHITE, 1)
            button = self.render_bordered_text(self.title_font, "+", WHITE, BLACK, button, 1, -8, 1)
            button.pressed += self.stat_up
            button.indent = 0
            button.stat = i
            self.stat_up_buttons.append(button)
            
        self.stat_down_buttons = list()
        for i in range(5):
            button = self.make_panel_button(BLACK, (20, 20))
            button = self.border_sprite(button, WHITE, 1)
            button = self.render_bordered_text(self.title_font, "-", WHITE, BLACK, button, 4, -8, 1)
            button.pressed += self.stat_down
            button.indent = 0
            button.stat = i
            self.stat_down_buttons.append(button)
        
        self.stat_button_regions = [self.stat_region.subregion(80, 100 + (i * 60), 110, 20) for i in range(5)]
        
        #endregion
        self.make_textbox(self.char_name_font, WHITE, BLACK, (260, 35), "name")

    def full_render(self):
        self.region.clear()
        background = self.make_panel(BLACK, (1200, 800))
        self.region.add_sprite(background, 0, 0)
        self.render_background_region()
        self.render_character_name_region()
        self.render_stat_region()
        self.render_class_region()
        self.render_options_region()
        self.render_picture_region()


    def render_options_region(self):
        self.options_region.clear()
        options_panel = self.make_panel(BLACK, self.options_region.size())
        options_panel = self.border_sprite(options_panel, WHITE, 1)
        start_game_button = self.make_panel_button(BLACK, (230, 40))
        start_game_button = self.border_sprite(start_game_button, WHITE, 1)
        start_game_button = self.render_bordered_text(self.title_font, "Start Game", BLACK, WHITE, start_game_button, 60, 2, 1)
        start_game_button.click += self.start_game_click
        main_menu_button = self.make_panel_button(BLACK, (230, 40))
        main_menu_button = self.border_sprite(main_menu_button, WHITE, 1)
        main_menu_button = self.render_bordered_text(self.title_font, "Main Menu", BLACK, WHITE, main_menu_button, 60, 2, 1)        
        main_menu_button.click += self.main_menu_click
        self.options_region.add_sprite(options_panel, 0, 0)
        self.options_region.add_sprite(start_game_button, 20, 10)
        self.options_region.add_sprite(main_menu_button, 270, 10)

    def main_menu_click(self, button, event):
        self.app.change_scene("main")
        
    def start_game_click(self, button, event):
        self.app.scenes["game"].get_created_character(self.create_player())
        self.app.change_scene("game")

    def create_player(self):
        self.player.image = self.player.player_class.name.lower() + "player.png"
        self.player.name = self.text_boxes["name"].text.strip()
        self.player.max_health = self.player.max_health + (3 * (self.player.statpool.stats[Stat.CONSTITUTION] - 10))
        self.player.current_health = self.player.max_health
        return self.player

    def render_background_region(self):
        self.background_region.clear()
        background = self.make_panel(BLACK, self.background_region.size())
        background = self.border_sprite(background, WHITE, 1)
        self.background_region.add_sprite(background, 0, 0)
        
    def render_character_name_region(self):
        self.character_name_region.clear()
        character_name_symbol = self.make_panel(BLACK, self.character_name_region.size())
        character_name_symbol = self.border_sprite(character_name_symbol, WHITE, 1)
        character_name_symbol = self.render_bordered_text(self.title_font, "Character Name", BLACK, WHITE, character_name_symbol, 5, 5, 1)
        self.refresh_text_box(self.text_boxes["name"])
        self.text_boxes["name"] = self.border_sprite(self.text_boxes["name"], BLACK, 2)

        self.character_name_region.add_sprite(character_name_symbol, 0, 0)
        self.character_name_region.add_sprite(self.text_boxes["name"], 5, 40)

    def render_stat_region(self):
        self.stat_region.clear()
        stat_region_panel = self.make_panel(BLACK, self.stat_region.size())
        stat_region_panel = self.border_sprite(stat_region_panel, WHITE, 1)
        stat_panel = self.draw_stat_panel()
        self.stat_region.add_sprite(stat_region_panel, 0, 0)
        self.stat_region.add_sprite(stat_panel, 60, 70)
        self.render_stat_buttons()
        
    def draw_stat_panel(self):
        PANEL_WIDTH = 150
        PANEL_HEIGHT = 400
        stat_panel = self.make_panel(BLACK, (PANEL_WIDTH, PANEL_HEIGHT))
        
        for i in range(5):
            stat_name = Stat(i).name.capitalize()
            stat = str(self.player.statpool.stats[Stat(i)])
            name_x_pos = (PANEL_WIDTH - get_string_width(self.title_font.size, stat_name)) // 2
            stat_x_pos = (PANEL_WIDTH - get_string_width(self.title_font.size, stat)) // 2
            stat_panel = self.render_bordered_text(self.title_font, stat, BLACK, WHITE, stat_panel, stat_x_pos, 30 + (i * 60), 1)
            stat_panel = self.render_bordered_text(self.title_font, stat_name, BLACK, WHITE, stat_panel, name_x_pos, i*60, 1)

        stat_panel = self.render_bordered_text(self.smaller_font, "Points Remaining", BLACK, WHITE, stat_panel, 15, 310, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.player.stat_points), BLACK, WHITE, stat_panel, 65, 340, 1)

        return stat_panel
    
    def render_stat_buttons(self):
        
        for i in range(5):
            self.stat_button_regions[i].clear()
            self.stat_button_regions[i].add_sprite(self.stat_down_buttons[i], 0 - self.stat_down_buttons[i].indent, 7 + self.stat_down_buttons[i].indent)
            self.stat_button_regions[i].add_sprite(self.stat_up_buttons[i], 90 - self.stat_up_buttons[i].indent, 7 + self.stat_up_buttons[i].indent)


    def render_class_region(self):
        self.class_region.clear()
        class_panel = self.make_panel(BLACK, self.class_region.size())
        class_panel = self.border_sprite(class_panel, WHITE, 1)
        self.class_region.add_sprite(class_panel, 0, 0)
        self.render_class_button_regions()
        

    def render_class_button_regions(self):
        for i, region in enumerate(self.class_button_regions):
            region.clear()
            pc_num = i + 1
            player_class = PlayerClass(pc_num)
            p_color = class_primary_colors[player_class]
            b_color = BLACK
            if self.player.player_class == player_class:
                b_color = class_secondary_colors[player_class]
            button = self.make_panel_button(BLACK, region.size())
            button = self.border_sprite(button, b_color, 3)
            x_offset = (region.size()[0] - get_string_width(self.title_font.size, player_class.name.capitalize())) // 2
            button = self.render_bordered_text(self.title_font, player_class.name.capitalize(), p_color, WHITE, button, x_offset, 25, 1)
            button.click += self.class_select
            button.player_class = player_class
            image = self.make_sprite(self.app.load(player_class.name.lower() + ".png"))
            region.add_sprite(button, 0, 0)
            region.add_sprite(image, 0, 13)
        
    def class_select(self, button, sender):
        self.player.player_class = button.player_class
        self.render_class_region()
        self.render_picture_region()

    def send_chosen_class(self):
        if self.w_selected == True:
            return "warrior"
        elif self.m_selected == True:
            return "wizard"
        elif self.r_selected == True:
            return "rogue"
        elif self.c_selected == True:
            return "cleric"


    def render_picture_region(self):
        self.picture_region.clear()
        if self.player.player_class:
            player_picture = self.make_sprite(self.app.load(self.player.player_class.name.lower() + "player.png"))     
            self.picture_region.add_sprite(player_picture, 0, 0)

    def mouse_left_down(self, event):
        pass

    def mouse_left_up(self, event):
        for i in range(5):
            self.stat_down_buttons[i].indent = 0
            self.stat_up_buttons[i].indent = 0
        self.render_stat_region()

    def stat_clicked(self, button, event):
        button.indent = 1
        self.render_stat_region()

    def stat_up(self, button, event):
        button.indent = 1
        if self.player.stat_points > 0:
            self.player.statpool.stats[Stat(button.stat)] += 1
            self.player.stat_points -= 1
        self.render_stat_region() 

    def stat_down(self, button, event):
        button.indent = 1
        if self.player.statpool.stats[Stat(button.stat)] > 10:
            self.player.statpool.stats[Stat(button.stat)] -= 1
            self.player.stat_points += 1
        self.render_stat_region()       

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
            