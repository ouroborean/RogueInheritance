from shikkoku.engine import Scene
from shikkoku.app import App
from shikkoku.color import *
import sdl2.ext

from rogue.cc_scene import CCScene

FONTNAME = "Basic-Regular.ttf"

class MenuScene(Scene):
    
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
            sdl2.SDLK_DOWN: self.press_down
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.button_region = self.region.subregion(500, 600, 200, 200)
        self.title_font = self.app.init_font(40, FONTNAME)
        self.title_region = self.region.subregion(200, 200, 800, 60)


        
    def full_render(self):
        self.region.clear()
        self.render_title_region()
        self.render_button_region()
        

    def render_button_region(self):
        self.button_region.clear()
        button1_panel = self.make_panel(PURPLE, self.button_region.size())
        new_game_button = self.make_panel_button(BLUE, (190, 90))
        new_game_button = self.border_sprite(new_game_button, DARK_BLUE, 2)
        new_game_button = self.render_bordered_text(self.title_font, "New Game", BLACK, WHITE, new_game_button, 8, 13, 1)
        exit_game_button = self.make_panel_button(BLUE, (190, 90))
        exit_game_button = self.border_sprite(exit_game_button, DARK_BLUE, 2)
        exit_game_button = self.render_bordered_text(self.title_font, "Exit Game", BLACK, WHITE, exit_game_button, 8, 13, 1)
        new_game_button.click += self.new_game_click
        exit_game_button.click += self.exit_game_click
        self.button_region.add_sprite(button1_panel, 0, 0)
        self.button_region.add_sprite(new_game_button, 5, 5)
        self.button_region.add_sprite(exit_game_button, 5, 105)
        
    def render_title_region(self):
        self.title_region.clear()

        title_panel = self.make_panel(RED, self.title_region.size())
        title_panel = self.render_bordered_text(self.title_font, "Rogue Inheritance", BLACK, WHITE, title_panel, 20, 10, 1)
        self.title_region.add_sprite(title_panel, 0, 0)
        
    def new_game_click(self, button, sender):
        print("New Game Clicked")
        self.app.change_scene("cc")


    def exit_game_click(self, button, sender):
        exit()

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
            