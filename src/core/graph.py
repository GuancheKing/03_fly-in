from src.core.zone import Zone
from src.core.connection import Connection


class Graph():
    zones: dict[str, Zone]
    connections: list[Connection]
    adjacency: dict[str, list[str]]
    start_zone: Zone | None
    end_zone: Zone | None

    def __init__(self):
        self.zones = {}
        self.connections = []
        self.adjacency = {}
        self.start_zone = None
        self.end_zone = None
