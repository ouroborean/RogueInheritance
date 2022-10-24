import sdl2.ext
from shikkoku.app import App
from shikkoku.sample_scene import SampleScene
from rogue.cc_scene import CCScene

from rogue.menu_scene import MenuScene
from rogue.game_scene import GameScene

FONTNAME = "Basic-Regular.ttf"

def main():
    """Main game entry point."""

    with App("Rogue Inheritance", (1200, 800)) as app:
        app.assign_resource_path("rogue.resources")
        app.assign_font(app.init_font(16, FONTNAME))
        scene = MenuScene(app, "main")
        app.add_scene(scene)
        app.add_scene(CCScene(app, "cc"))
        app.add_scene(GameScene(app, "game"))
        print(app.window.position)
        app.start_game_loop(scene)
    
main()