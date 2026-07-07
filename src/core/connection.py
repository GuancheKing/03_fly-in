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

    def can_accept_drone(self) -> bool:
        return not self.is_full()

    def is_full(self) -> bool:
        return self.current_usage >= self.max_capacity

    def occupy(self) -> None:
        self.current_usage += 1

    def reset_usage(self) -> None:
        self.current_usage = 0
