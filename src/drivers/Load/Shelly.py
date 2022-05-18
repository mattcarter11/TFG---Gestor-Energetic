from .Load import Load
from ShellyPy import Shelly

class ShellyLoad(Load):

    def __init__(self, ip:str, port:str="80"):
        self.__load = Shelly(ip, port)

    def set_status(self, value:bool, timer:int=None):
        try:
            if timer is not None:
                self.__load.relay(0, turn=value, timer=timer)
            else:
                self.__load.relay(0, turn=value)
        except:
            pass
        
    def get_status(self) -> dict:
        try:
            data = self.__load.status()
            return {
                "ison": data['relays'][0]["ison"],
                "power": data['meters'][0]["power"]*1.0
            }
        except:
            return { "ison": False, "power": 0 }

    def get_power(self) -> float:
        try:
            return self.__load.status()["meters"][0]["power"]*1.0
        except:
            return 0