from src.core.zone import Zone


class Connection():
    origin: Zone
    destination: Zone
    max_capacity: int
    current_usage: int

    def __init__(
            self,
            origin: Zone,
            destination: Zone
    ):
        self.origin = origin
        self.destination = destination
        self.max_capacity = 1
        self.current_usage = 0
