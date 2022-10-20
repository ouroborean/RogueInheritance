import string
from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext

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
        self.background_region = self.region.subregion(0, 0, 1200, 800)



        
        
    def full_render(self):
        self.get_created_character()
        self.render_background_region()

    def render_background_region(self):

        background_panel = self.make_panel(BLACK, self.background_region.size())
        background_panel = self.render_bordered_text(self.title_font, str(self.character_class), BLACK, WHITE, background_panel, 0, 0, 1)
        self.background_region.add_sprite(background_panel, 0, 0)
        
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
            