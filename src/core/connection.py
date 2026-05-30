from src.core.zone import Zone

class Connection():
    origin: Zone
    destination: Zone
    max_capacity: int
    current_usage: int
