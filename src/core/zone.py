from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone():
    name: str
    coords: tuple[int, int]
    zone_type: ZoneType
    max_drones: int
    color: str | None
    current_occupancy: int
    is_start_or_end: bool

    def __init__(self, name: str, coords: tuple[int, int]):
        self.name = name
        self.coords = coords
        self.zone_type = ZoneType.NORMAL
        self.max_drones = 1
        self.color = None
        self.current_occupancy = 0
        self.is_start_or_end = False

    def is_full(self) -> bool:
        if self.is_start_or_end:
            return False
        return self.max_drones <= self.current_occupancy

    def can_accept_drone(self) -> bool:
        if self.zone_type == ZoneType.BLOCKED or self.is_full():
            return False
        return True
