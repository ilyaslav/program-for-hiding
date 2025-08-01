class PingRpi:
    def __init__(self, rpi_name: str):
        self.rpi_status = False
        self.ping_number = 0
        self.ping_status = False
        self.name = rpi_name
