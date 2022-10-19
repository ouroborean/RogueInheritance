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
        self.warrior_button_region = self.region.subregion(350, 80, 250, 80)
        self.wizard_button_region = self.region.subregion(350, 190, 250, 80)
        self.rogue_button_region = self.region.subregion(350, 300, 250, 80)
        self.cleric_button_region = self.region.subregion(350, 410, 250, 80)
        self.title_font = self.app.init_font(24, FONTNAME)
        self.str_up_region = self.region.subregion(208, 257, 20, 22)
        self.strength_up = self.make_panel_button(BLACK, (20, 20))
        self.strength_up = self.border_sprite(self.strength_up, WHITE, 1)
        self.strength_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.strength_up, 1, -8, 1)
        self.strength_up.pressed += self.stat_clicked
        self.strength_up.indent = 0
        self.strength_down = self.make_panel_button(BLACK, (20, 20))
        self.strength_down = self.border_sprite(self.strength_down, WHITE, 1)
        self.strength_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.strength_down, 4, -8, 1)
        self.strength_down.pressed += self.stat_clicked
        self.strength_down.indent = 0
        self.dexterity_up = self.make_panel_button(BLACK, (20, 20))
        self.dexterity_up = self.border_sprite(self.dexterity_up, WHITE, 1)
        self.dexterity_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.dexterity_up, 1, -8, 1)
        self.dexterity_up.pressed += self.stat_clicked
        self.dexterity_up.indent = 0
        self.dexterity_down = self.make_panel_button(BLACK, (20, 20))
        self.dexterity_down = self.border_sprite(self.dexterity_down, WHITE, 1)
        self.dexterity_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.dexterity_down, 4, -8, 1)
        self.dexterity_down.pressed += self.stat_clicked
        self.dexterity_down.indent = 0
        self.constitution_up = self.make_panel_button(BLACK, (20, 20))
        self.constitution_up = self.border_sprite(self.constitution_up, WHITE, 1)
        self.constitution_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, self.constitution_up, 1, -8, 1)
        self.constitution_up.pressed += self.stat_clicked
        self.constitution_up.indent = 0
        self.constitution_down = self.make_panel_button(BLACK, (20, 20))
        self.constitution_down = self.border_sprite(self.constitution_down, WHITE, 1)
        self.constitution_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, self.constitution_down, 4, -8, 1)
        self.constitution_down.pressed += self.stat_clicked
        self.constitution_down.indent = 0
        self.dex_up_region = self.region.subregion(208, 317, 20, 22)
        self.con_up_region = self.region.subregion(208, 377, 20, 22)
        self.str_down_region = self.region.subregion(133, 257, 20, 22)
        self.dex_down_region = self.region.subregion(133, 317, 20, 22)
        self.con_down_region = self.region.subregion(133, 377, 20, 22)
        self.w_selected = False
        self.m_selected = False
        self.r_selected = False
        self.c_selected = False
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        



        
    def full_render(self):
        self.region.clear()
        self.render_clear_render()
        self.render_background_region()
        self.render_character_name_region()
        self.render_stat_region()
        self.render_class_region()

    def render_clear_render(self):
        self.cover_region.clear()

        cover = self.make_panel(BLACK, self.cover_region.size())

        self.cover_region.add_sprite(cover, 0, 0)

    def render_background_region(self):
        self.background_region.clear()

        background = self.make_panel(BLACK, self.background_region.size())

        background = self.border_sprite(background, WHITE, 1)

        self.background_region.add_sprite(background, 0, 0)

        # button1_panel = self.make_panel(PURPLE, self.button_region.size())
        # new_game_button = self.make_panel_button(BLUE, (190, 90))
        # new_game_button = self.border_sprite(new_game_button, DARK_BLUE, 2)
        # new_game_button = self.render_bordered_text(self.title_font, "New Game", BLACK, WHITE, new_game_button, 8, 13, 1)
        # exit_game_button = self.make_panel_button(BLUE, (190, 90))
        # exit_game_button = self.border_sprite(exit_game_button, DARK_BLUE, 2)
        # exit_game_button = self.render_bordered_text(self.title_font, "Exit Game", BLACK, WHITE, exit_game_button, 8, 13, 1)
        # new_game_button.click += self.new_game_click
        # exit_game_button.click += self.exit_game_click
        # self.button_region.add_sprite(button1_panel, 0, 0)
        # self.button_region.add_sprite(new_game_button, 5, 5)
        # self.button_region.add_sprite(exit_game_button, 5, 105)
        # image10 = self.sprite_factory.from_surface(self.get_scaled_surface(get_image_from_path("unholy.png")))
        # self.region_baubles.add_sprite(image1, -10, -10)
        
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
            print("What am I even doing")

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
            print("What am I even doing")

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
            print("What am I even doing")

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
            print("What am I even doing")

    def render_stat_panel(self):
        stat_panel = self.make_panel(BLACK, (150, 400))
        stat_panel = self.render_bordered_text(self.title_font, str(self.strength), BLACK, WHITE, stat_panel, 60, 30, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Strength", BLACK, WHITE, stat_panel, 28, 0, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.dexterity), BLACK, WHITE, stat_panel, 60, 90, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Dexterity", BLACK, WHITE, stat_panel, 25, 60, 1)
        stat_panel = self.render_bordered_text(self.title_font, str(self.constitution), BLACK, WHITE, stat_panel, 60, 150, 1)
        stat_panel = self.render_bordered_text(self.title_font, "Constitution", BLACK, WHITE, stat_panel, 10, 120, 1)
        return stat_panel

    def render_stat_buttons(self):
        self.str_up_region.clear()
        self.str_down_region.clear()
        self.dex_up_region.clear()
        self.dex_down_region.clear()
        self.con_up_region.clear()
        self.con_down_region.clear()
        # strength_up = self.make_panel_button(BLACK, (20, 20))
        # strength_up = self.border_sprite(strength_up, WHITE, 1)
        # strength_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, strength_up, 1, -8, 1)
        # strength_up.pressed += self.strength_up
        # strength_down = self.make_panel_button(BLACK, (20, 20))
        # strength_down = self.border_sprite(strength_down, WHITE, 1)
        # strength_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, strength_down, 4, -8, 1)
        # strength_down.click += self.strength_down
        # dexterity_up = self.make_panel_button(BLACK, (20, 20))
        # dexterity_up = self.border_sprite(dexterity_up, WHITE, 1)
        # dexterity_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, dexterity_up, 1, -8, 1)
        # dexterity_up.click += self.dexterity_up
        # dexterity_down = self.make_panel_button(BLACK, (20, 20))
        # dexterity_down = self.border_sprite(dexterity_down, WHITE, 1)
        # dexterity_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, dexterity_down, 4, -8, 1)
        # dexterity_down.click += self.dexterity_down
        # constitution_up = self.make_panel_button(BLACK, (20, 20))
        # constitution_up = self.border_sprite(constitution_up, WHITE, 1)
        # constitution_up = self.render_bordered_text(self.title_font, "+", WHITE, WHITE, constitution_up, 1, -8, 1)
        # constitution_up.click += self.constitution_up
        # constitution_down = self.make_panel_button(BLACK, (20, 20))
        # constitution_down = self.border_sprite(constitution_down, WHITE, 1)
        # constitution_down = self.render_bordered_text(self.title_font, "-", WHITE, WHITE, constitution_down, 4, -8, 1)
        # constitution_down.click += self.constitution_down
        self.str_up_region.add_sprite(self.strength_up, 2 - self.strength_up.indent, 0 + self.strength_up.indent)
        self.dex_up_region.add_sprite(self.dexterity_up, 2 - self.dexterity_up.indent, 0 + self.dexterity_up.indent)
        self.con_up_region.add_sprite(self.constitution_up, 2 - self.constitution_up.indent, 0 + self.constitution_up.indent)
        self.str_down_region.add_sprite(self.strength_down, 2 - self.strength_down.indent, 0 + self.strength_down.indent)
        self.dex_down_region.add_sprite(self.dexterity_down, 2 - self.dexterity_down.indent, 0 + self.dexterity_down.indent)
        self.con_down_region.add_sprite(self.constitution_down, 2 - self.constitution_down.indent, 0 + self.constitution_down.indent)


    def warrior_select(self, button, sender):
        print("Warrior Selected")
        self.w_selected = True
        self.m_selected = False
        self.r_selected = False
        self.c_selected = False
        self.render_class_region()
        
    def wizard_select(self, button, sender):
        print("Wizard Selected")
        self.w_selected = False
        self.m_selected = True
        self.r_selected = False
        self.c_selected = False
        self.render_class_region()

    def rogue_select(self, button, sender):
        print("Rogue Selected")
        self.w_selected = False
        self.m_selected = False
        self.r_selected = True
        self.c_selected = False
        self.render_class_region()

    def cleric_select(self, button, sender):
        print("Cleric Selected")
        self.w_selected = False
        self.m_selected = False
        self.r_selected = False
        self.c_selected = True
        self.render_class_region()

    def mouse_left_down(self, event):
        #just set it to do a bool "clicked" or "not clicked" state to render a button a few things down and re-render the stat panel
        #probably make a def stat_button_clicked and a def stat_button_unclicked for toggling the boolean and re-rendering the scene
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
            