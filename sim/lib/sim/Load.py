class Load():
    def __init__(self, value:float):
        self.value = value
        self.on = False

    def set_status(self, status:bool):
        if status and not self.on:
            self.on = True
            return 1
        if not status and self.on:
            self.on = False
            return -1
        return 0

    def get_power(self) -> float:
        return self.on*self.value*1.0