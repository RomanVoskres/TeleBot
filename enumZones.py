from enum import Enum, auto

def returnRuName(zones):
    if (zones == None):
        return "None"
    if (zones == Zones.eyebrows):
        return "Брови"
    if (zones == Zones.eyelids):
        return "Веки"
    if (zones == Zones.lips):
        return "Губы"

class Zones(Enum):
    eyebrows = auto()
    eyelids = auto()
    lips = auto()