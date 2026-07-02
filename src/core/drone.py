from enum import Enum
from src.core.zone import Zone
from src.core.connection import Connection


class DroneStatus(str, Enum):
    WAITING = "waiting"
    MOVING = "moving"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Drone():
    id: str
    current_zone: Zone | None
    current_connection: Connection | None
    status: DroneStatus
    path: list[Zone]
    current_step: int
    remaining_turns: int
    destination_zone: Zone | None

    def __init__(
            self,
            id: str,
            starting_zone: Zone
    ):
        self.id = id
        self.current_zone = starting_zone
        self.current_connection = None
        self.status = DroneStatus.WAITING
        self.path = []
        self.current_step = 0
        self.remaining_turns = 0
        self.destination_zone = None
