import enum
import typing



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
        self.types = set()
        for scenerytype in types:
            self.types.add(SceneryType[scenerytype])
        
        
class Portal(Scenery):
    
    
    
    def __init__(self, image, types=set(), id: int=0, area_dest: str=""):
        super().__init__(image, types)
        self.id = id
        self.area_dest = area_dest
        self.types.add(SceneryType.WALKABLE)
        self.locked = False
        self.loc = (0, 0)
        
    def lock_location(self, loc):
        self.loc = loc
        
    
        