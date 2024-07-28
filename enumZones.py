from enum import Enum, auto

def returnRuName(Zones):
    if (Zones == None):
        return "None"
    if (Zones == Zones.eyebrows):
        return "Брови"
    if (Zones == Zones.eyelids):
        return "Веки"
    if (Zones == Zones.lips):
        return "Губы"

class Zones(Enum):
    eyebrows = auto()
    eyelids = auto()
    lips = auto()