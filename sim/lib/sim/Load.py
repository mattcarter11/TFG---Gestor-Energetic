class Load():
    def __init__(self, value:float):
        self.value = value
        self.on = False

    def turn_on(self):
        if not self.on:
            self.on = True
            return 1
        return 0

    def turn_off(self):
        if self.on:
            self.on = False
            return -1
        return 0

    def get_power(self) -> float:
        return self.on*self.value*1.0