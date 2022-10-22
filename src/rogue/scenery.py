import enum

@enum.unique
class SceneryType(enum.IntEnum):
    WALKABLE = 0
    OPAQUE = 1
    SOLID = 2
    INVIOLABLE = 3

class Scenery():
    
    types: set
    
    def __init__(self, image, types=set()):
        self.image = image
        self.types = types