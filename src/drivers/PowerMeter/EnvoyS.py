from .PowerMeterBase import PowerMeterBase
import json, requests

class EnvoyS(PowerMeterBase):

    def __init__(self, url:str, user:str, pswd:str, timeout:int=5, zero_ref:int=20):
        super().__init__(timeout, zero_ref)
        self.url        = url
        self.auth       = requests.auth.HTTPDigestAuth(user, pswd)

    def power_consumed(self) -> float:
        data = self.__get_data()
        if data:
            return self.__exract_consumed(data)
        return 0.0

    def power_produced(self) -> float:
        data = self.__get_data()
        if data:
            prod = self.__exract_produced(data)
            if prod > self.zero_ref:
                return prod
        return 0.0

    def power_pc(self) -> tuple:
        data = self.__get_data()
        if data:
            prod = self.__exract_produced(data)
            cons = self.__exract_consumed(data)
            if prod > self.zero_ref:
                return (prod, cons)
            else:
                return (0.0, cons)
        return (0.0, 0.0)

    def power_available(self) -> float:
        data = self.__get_data()
        if data:
            prod = self.__exract_produced(data)
            cons = self.__exract_consumed(data)
            if prod > self.zero_ref:
                prod = 0
            return prod-cons
        return 0

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
        return data['total-consumption']['ph-a']['p']+data['total-consumption']['ph-b']['p']+data['total-consumption']['ph-c']['p']

    def __exract_produced(self, data:dict) -> float:
        return data['production']['ph-a']['p']+data['production']['ph-b']['p']+data['production']['ph-c']['p']