from enum import Enum, auto

def returnRuName(enum_communication_method):
    if (enum_communication_method == None):
        return "None"
    if (enum_communication_method == enum_communication_method.Call):
        return "Звонок"
    if (enum_communication_method == enum_communication_method.WhatsApp):
        return "Воцап"

class EnumCommunicationMethod(Enum):
    Call = auto()
    WhatsApp = auto()