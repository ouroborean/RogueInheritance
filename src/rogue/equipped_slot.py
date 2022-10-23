from rogue.equipment import Equipment, Slot
import enum



class equip_slot(enum.IntEnum):
    HEAD = 0
    SHOULDERS = 1
    CHEST = 2
    HANDS = 3
    LEGS = 4
    FEET = 5

class Equip_Slot():

    def __init__(self):
        self.equip_slot_location = {
            equip_slot.HEAD : (0, 0),
            equip_slot.SHOULDERS : (74, 0),
            equip_slot.CHEST : (148, 0),
            equip_slot.HANDS : (0, 74),
            equip_slot.LEGS : (0, 148),
            equip_slot.FEET : (74, 74)
        }
        self.slot_image = self.image_to_surf(self.app.load("grid.png"))
    pass