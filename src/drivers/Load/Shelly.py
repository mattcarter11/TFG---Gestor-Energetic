from .LoadBase import LoadBase
from ShellyPy import Shelly

class ShellyLoad(LoadBase):

    def __init__(self, ip:str, port:str="80", value:int=0, on_time=None):
        super().__init__(value, on_time)
        self.__load = Shelly(ip, port)

    def set_status(self, status:bool, timer:int=None):
        try:
            if timer is not None:
                self.__load.relay(0, turn=status, timer=timer)
            elif self.on_time is not None:
                self.__load.relay(0, turn=status, time=self.on_time)
            else:
                self.__load.relay(0, turn=status)
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