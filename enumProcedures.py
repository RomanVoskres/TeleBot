from enum import Enum, auto

def returnRuName(procedures):
    if (procedures == None):
        return None
    if (procedures == Procedures.tattoo):
        return "Таттуаж"
    if (procedures == Procedures.lightening_tatto):
        return "Освеление таттуажа"

class Procedures(Enum):
    tattoo = auto()
    lightening_tatto = auto()