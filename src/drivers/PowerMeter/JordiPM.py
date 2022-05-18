import json, requests
from PowerMeter import PowerMeter

class JordiPM(PowerMeter):

    def __init__(self, url:str, user:str, pswd:str, timeout:int=5, zero_ref:int=20):
        self.url        = url
        self.auth       = requests.auth.HTTPDigestAuth(user, pswd)
        self.timeout    = timeout
        self.zero_ref   = zero_ref

    def power_consumed(self) -> float:
        if (data := self.__get_data()):
            return self.__exract_consumed(data)
        return 0.0

    def power_generated(self) -> float:
        if (data := self.__get_data()):
            prod = self.__exract_generated(data)
            if prod > self.zero_ref:
                return prod
        return 0.0

    def power_gc(self) -> float:
        if (data := self.__get_data()):
            prod = self.__exract_generated(data)
            cons = self.__exract_consumed(data)
            if prod > self.zero_ref:
                return (prod, cons)
            else:
                return (0.0, cons)
        return (0.0, 0.0)

    def __get_data(self) -> dict:
        try:
            marker = b'data: '
            stream = requests.get(self.url, auth=self.auth, stream=True, timeout=self.timeout)
            for line in stream.iter_lines():
                if line.startswith(marker):
                    line = line.replace(marker, b'')
                    return json.loads(line.decode())
        except Exception:
            return None

    def __exract_consumed(self, data:dict) -> float:
        return data['total-consumption']['ph-a']['p']+data['total-consumption']['ph-b']['p']+data['total-consumption']['ph-c']

    def __exract_generated(self, data:dict) -> float:
        return data['production']['ph-a']['p']+data['production']['ph-b']['p']+data['production']['ph-c']['p']