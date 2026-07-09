from src.core.zone import Zone
from src.core.connection import Connection


class Graph():
    nb_drones: int | None
    zones: dict[str, Zone]
    connections: list[Connection]
    adjacency: dict[str, list[str]]
    start_zone: Zone | None
    end_zone: Zone | None

    def __init__(self) -> None:
        self.nb_drones = None
        self.zones = {}
        self.connections = []
        self.adjacency = {}
        self.start_zone = None
        self.end_zone = None
