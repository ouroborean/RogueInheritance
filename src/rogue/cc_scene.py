from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext
import sdl2
import importlib.resources
import typing
from PIL import Image

FONTNAME = "Basic-Regular.ttf"


def get_image_from_path(file_name: str) -> Image:
    with importlib.resources.path('rogue.resources', file_name) as path:
        return Image.open(path)

class CCScene(Scene):
    
    def __init__(self, app, name):
        super().__init__(app, name)
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
        self.cover_region = self.region.subregion(0, 0, 1200, 800)
        self.background_region = self.region.subregion(30, 30, 1140, 740)
        self.character_name_region = self.region.subregion(50, 50, 270, 80)
        self.stat_region = self.region.subregion(50, 150, 270, 540)
        self.class_region = self.region.subregion(340, 50, 270, 640)
        self.picture_region = self.region.subregion(830, 250, 100, 100)
        self.options_region = self.region.subregion(340, 700, 520, 60)
        self.warrior_button_region = self.region.subregion(350, 80, 250, 80)
        self.wizard_button_region = self.region.subregion(350, 190, 250, 80)
        self.rogue_button_region = self.region.subregion(350, 300, 250, 80)
        self.cleric_button_region = self.region.subregion(350, 410, 250, 80)
        self.title_font = self.app.init_font(24, FONTNAME)
        self.smaller_font = self.app.init_font(16, FONTNAME)
        self.str_up_region = self.region.subregion(208, 257, 20, 22)
        #region Stat Buttons
        self.strength_up = self.make_panel_button(BLACK, (20, 20))
        self.strength_up = self.border_sprite(self.strength_up, WHITE, 1)
        self.strength_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.strength_up, 1, -8, 1)
        self.strength_up.pressed += self.str_up
        self.strength_up.indent = 0
        self.strength_down = self.make_panel_button(BLACK, (20, 20))
        self.strength_down = self.border_sprite(self.strength_down, WHITE, 1)
        self.strength_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.strength_down, 4, -8, 1)
        self.strength_down.pressed += self.str_down
        self.strength_down.indent = 0
        self.dexterity_up = self.make_panel_button(BLACK, (20, 20))
        self.dexterity_up = self.border_sprite(self.dexterity_up, WHITE, 1)
        self.dexterity_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.dexterity_up, 1, -8, 1)
        self.dexterity_up.pressed += self.dex_up
        self.dexterity_up.indent = 0
        self.dexterity_down = self.make_panel_button(BLACK, (20, 20))
        self.dexterity_down = self.border_sprite(self.dexterity_down, WHITE, 1)
        self.dexterity_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.dexterity_down, 4, -8, 1)
        self.dexterity_down.pressed += self.dex_down
        self.dexterity_down.indent = 0
        self.constitution_up = self.make_panel_button(BLACK, (20, 20))
        self.constitution_up = self.border_sprite(self.constitution_up, WHITE, 1)
        self.constitution_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.constitution_up, 1, -8, 1)
        self.constitution_up.pressed += self.con_up
        self.constitution_up.indent = 0
        self.constitution_down = self.make_panel_button(BLACK, (20, 20))
        self.constitution_down = self.border_sprite(self.constitution_down, WHITE, 1)
        self.constitution_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.constitution_down, 4, -8, 1)
        self.constitution_down.pressed += self.con_down
        self.constitution_down.indent = 0
        #endregion
        #region Stat Button Regions
        self.dex_up_region = self.region.subregion(208, 317, 20, 22)
        self.con_up_region = self.region.subregion(208, 377, 20, 22)
        self.str_down_region = self.region.subregion(133, 257, 20, 22)
        self.dex_down_region = self.region.subregion(133, 317, 20, 22)
        self.con_down_region = self.region.subregion(133, 377, 20, 22)
        #endregion
        self.w_selected = False
        self.m_selected = False
        self.r_selected = False
        self.c_selected = False
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.stat_points = 5
        dexterity = 10
        



        
    def full_render(self):
        self.region.clear()
        self.render_clear_render()
        self.render_background_region()
        self.render_character_name_region()
        self.render_stat_region()
        self.render_class_region()
        self.render_options_region()
        self.render_picture_region()

    def render_clear_render(self):
        self.cover_region.clear()

        cover = self.make_panel(BLACK, self.cover_region.size())

        self.cover_region.add_sprite(cover, 0, 0)

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
        self.app.change_scene("game")

    def render_background_region(self):
        self.background_region.clear()

        background = self.make_panel(BLACK, self.background_region.size())

        background = self.border_sprite(background, WHITE, 1)

        self.background_region.add_sprite(background, 0, 0)
        
    def render_character_name_region(self):
        self.character_name_region.clear()
        character_name = self.make_panel(BLACK, self.character_name_region.size())
        character_name = self.border_sprite(character_name, WHITE, 1)
        character_name = self.render_bordered_text(self.title_font, "Character Name", BLACK, WHITE, character_name, 5, 5, 1)
        text_box = self.make_panel(WHITE, (260, 35))

        self.character_name_region.add_sprite(character_name, 0, 0)
        self.character_name_region.add_sprite(text_box, 5, 40)

    def render_stat_region(self):
        self.stat_region.clear()
        stat_region_panel = self.make_panel(BLACK, self.stat_region.size())
        stat_region_panel = self.border_sprite(stat_region_panel, WHITE, 1)
        stat_panel = self.render_stat_panel()
        self.stat_region.add_sprite(stat_region_panel, 0, 0)
        self.stat_region.add_sprite(stat_panel, 60, 70)
        self.render_stat_buttons()

    def render_class_region(self):
        self.class_region.clear()
        class_panel = self.make_panel(BLACK, self.class_region.size())
        class_panel = self.border_sprite(class_panel, WHITE, 1)
        self.class_region.add_sprite(class_panel, 0, 0)
        self.render_warrior_button_region()
        self.render_wizard_button_region()
        self.render_cleric_button_region()
        self.render_rogue_button_region()

    def render_warrior_button_region(self):
        self.warrior_button_region.clear()
        if self.w_selected == True:
            warrior_panel_border = self.make_panel_button(BLACK, self.warrior_button_region.size())
            warrior_panel_border = self.border_sprite(warrior_panel_border, DARK_RED, 3)
            warrior_panel_border = self.render_bordered_text(self.title_font, "Warrior", RED, WHITE, warrior_panel_border, 85, 25, 1)
            warrior_panel_border.click += self.warrior_select
            warrior_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("warrior.png")))
            self.warrior_button_region.add_sprite(warrior_panel_border, 0, 0)
            self.warrior_button_region.add_sprite(warrior_image, 0, 13)
            print("Warrior was selected!")
        else:

            warrior_panel = self.make_panel_button(BLACK, self.warrior_button_region.size())
            warrior_panel = self.render_bordered_text(self.title_font, "Warrior", RED, WHITE, warrior_panel, 85, 25, 1)
            warrior_panel.click += self.warrior_select
            warrior_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("warrior.png")))
            self.warrior_button_region.add_sprite(warrior_panel, 0, 0)
            self.warrior_button_region.add_sprite(warrior_image, 0, 13)

    def send_chosen_class(self):
        if self.w_selected == True:
            return "Warrior"
        elif self.m_selected == True:
            return "Wizard"
        elif self.r_selected == True:
            return "Rogue"
        elif self.c_selected == True:
            return "Cleric"



    def render_wizard_button_region(self):
        self.wizard_button_region.clear()
        if self.m_selected == True:
            wizard_panel_border = self.make_panel_button(BLACK, self.wizard_button_region.size())
            wizard_panel_border = self.border_sprite(wizard_panel_border, DARK_BLUE, 3)
            wizard_panel_border = self.render_bordered_text(self.title_font, "Wizard", BLUE, WHITE, wizard_panel_border, 85, 25, 1)
            wizard_panel_border.click += self.wizard_select
            wizard_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("wizard.png")))
            self.wizard_button_region.add_sprite(wizard_panel_border, 0, 0)
            self.wizard_button_region.add_sprite(wizard_image, 0, 10)
            print("Mage was selected!")
        else:

            wizard_panel = self.make_panel_button(BLACK, self.wizard_button_region.size())
            wizard_panel = self.render_bordered_text(self.title_font, "Wizard", BLUE, WHITE, wizard_panel, 85, 25, 1)
            wizard_panel.click += self.wizard_select
            wizard_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("wizard.png")))

            self.wizard_button_region.add_sprite(wizard_panel, 0, 0)
            self.wizard_button_region.add_sprite(wizard_image, 0, 10)

    def render_rogue_button_region(self):
        self.rogue_button_region.clear()
        if self.r_selected == True:
            rogue_panel_border = self.make_panel_button(BLACK, self.rogue_button_region.size())
            rogue_panel_border = self.border_sprite(rogue_panel_border, DARK_GREEN, 3)
            rogue_panel_border = self.render_bordered_text(self.title_font, "Rogue", GREEN, WHITE, rogue_panel_border, 85, 25, 1)
            rogue_panel_border.click += self.rogue_select
            rogue_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("rogue.png")))
            self.rogue_button_region.add_sprite(rogue_panel_border, 0, 0)
            self.rogue_button_region.add_sprite(rogue_image, 0, 10)
            print("Rogue was selected!")
        else:
            rogue_panel = self.make_panel_button(BLACK, self.rogue_button_region.size())
            rogue_panel = self.render_bordered_text(self.title_font, "Rogue", GREEN, WHITE, rogue_panel, 85, 25, 1)
            rogue_panel.click += self.rogue_select
            rogue_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("rogue.png")))
            self.rogue_button_region.add_sprite(rogue_panel, 0, 0)
            self.rogue_button_region.add_sprite(rogue_image, 0, 10)

    def render_cleric_button_region(self):
        self.cleric_button_region.clear()
        if self.c_selected == True:
            cleric_panel_border = self.make_panel_button(BLACK, self.cleric_button_region.size())
            cleric_panel_border = self.border_sprite(cleric_panel_border, YELLOW, 3)
            cleric_panel_border = self.render_bordered_text(self.title_font, "Cleric", YELLOW, WHITE, cleric_panel_border, 85, 25, 1)
            cleric_panel_border.click += self.cleric_select
            cleric_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("cleric.png")))
            self.cleric_button_region.add_sprite(cleric_panel_border, 0, 0)
            self.cleric_button_region.add_sprite(cleric_image, 0, 10)
            print("Cleric was selected!")
        else:
            cleric_panel = self.make_panel_button(BLACK, self.cleric_button_region.size())
            cleric_panel = self.render_bordered_text(self.title_font, "Cleric", YELLOW, WHITE, cleric_panel, 85, 25, 1)
            cleric_panel.click += self.cleric_select
            cleric_image = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("cleric.png")))
            self.cleric_button_region.add_sprite(cleric_panel, 0, 0)
            self.cleric_button_region.add_sprite(cleric_image, 0, 10)

    def render_stat_panel(self):
        stat_panel = self.make_panel(BLACK, (150, 400))
        stat_panel = self.render_bordered_text(self.title_font, str(self.strength), BLACK, WHITE, stat_panel, 60, 30, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Strength", BLACK, WHITE, stat_panel, 28, 0, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.dexterity), BLACK, WHITE, stat_panel, 60, 90, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Dexterity", BLACK, WHITE, stat_panel, 25, 60, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.constitution), BLACK, WHITE, stat_panel, 60, 150, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Constitution", BLACK, WHITE, stat_panel, 10, 120, 1)
        stat_panel = self.render_bordered_text(self.smaller_font, "Points Remaining", BLACK, WHITE, stat_panel, 15, 240, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.stat_points), BLACK, WHITE, stat_panel, 65, 270, 1)

        return stat_panel

    def render_stat_buttons(self):
        self.str_up_region.clear()
        self.str_down_region.clear()
        self.dex_up_region.clear()
        self.dex_down_region.clear()
        self.con_up_region.clear()
        self.con_down_region.clear()
        self.str_up_region.add_sprite(self.strength_up, 2 - self.strength_up.indent, 0 + self.strength_up.indent)
        self.dex_up_region.add_sprite(self.dexterity_up, 2 - self.dexterity_up.indent, 0 + self.dexterity_up.indent)
        self.con_up_region.add_sprite(self.constitution_up, 2 - self.constitution_up.indent, 0 + self.constitution_up.indent)
        self.str_down_region.add_sprite(self.strength_down, 2 - self.strength_down.indent, 0 + self.strength_down.indent)
        self.dex_down_region.add_sprite(self.dexterity_down, 2 - self.dexterity_down.indent, 0 + self.dexterity_down.indent)
        self.con_down_region.add_sprite(self.constitution_down, 2 - self.constitution_down.indent, 0 + self.constitution_down.indent)
       
    def render_picture_region(self):
        self.picture_region.clear()
        player_picture = self.make_panel(BLACK, self.picture_region.size())
        if self.w_selected:
            player_picture = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("warriorplayer.png")))
        elif self.m_selected:
            player_picture = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("wizardplayer.png")))
        elif self.r_selected:
            player_picture = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("rogueplayer.png")))
        elif self.c_selected:
            player_picture = self.sprite_factory.from_surface(self.image_to_surf(get_image_from_path("clericplayer.png")))        
        self.picture_region.add_sprite(player_picture, 0, 0)

    def warrior_select(self, button, sender):
        print("Warrior Selected")
        self.w_selected = True
        self.m_selected = False
        self.r_selected = False
        self.c_selected = False
        self.render_class_region()
        self.render_picture_region()

    def wizard_select(self, button, sender):
        print("Wizard Selected")
        self.w_selected = False
        self.m_selected = True
        self.r_selected = False
        self.c_selected = False
        self.render_class_region()
        self.render_picture_region()

    def rogue_select(self, button, sender):
        print("Rogue Selected")
        self.w_selected = False
        self.m_selected = False
        self.r_selected = True
        self.c_selected = False
        self.render_class_region()
        self.render_picture_region()

    def cleric_select(self, button, sender):
        print("Cleric Selected")
        self.w_selected = False
        self.m_selected = False
        self.r_selected = False
        self.c_selected = True
        self.render_class_region()
        self.render_picture_region()

    def mouse_left_down(self, event):
        pass

    def mouse_left_up(self, event):
        self.strength_up.indent = 0
        self.strength_down.indent = 0
        self.dexterity_up.indent = 0
        self.dexterity_down.indent = 0
        self.constitution_up.indent = 0
        self.constitution_down.indent = 0
        self.render_stat_region()


    def stat_clicked(self, button, event):
        button.indent = 1
        self.render_stat_region()

    def str_up(self, button, event):
        button.indent = 1
        if self.stat_points > 0:
            self.strength += 1
            self.stat_points -= 1
        self.render_stat_region()

    def dex_up(self, button, event):
        button.indent = 1
        if self.stat_points > 0:
            self.dexterity += 1
            self.stat_points -= 1
        self.render_stat_region()

    def con_up(self, button, event):
        button.indent = 1
        if self.stat_points > 0:
            self.constitution += 1
            self.stat_points -= 1
        self.render_stat_region()    

    def str_down(self, button, event):
        button.indent = 1
        if self.strength > 10:
            self.strength -= 1
            self.stat_points += 1
        self.render_stat_region()       

    def dex_down(self, button, event):
        button.indent = 1
        if self.dexterity > 10:
            self.dexterity -= 1
            self.stat_points += 1
        self.render_stat_region()  

    def con_down(self, button, event):
        button.indent = 1
        if self.constitution > 10:
            self.constitution -= 1
            self.stat_points += 1
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
            