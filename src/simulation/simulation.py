from src.core.graph import Graph
from src.core.drone import Drone
from src.pathfinding.pathfiner import PathFinder


class Simulation:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.pathfinder = PathFinder(self.graph)
        self.turn = 0
        self.drones = []
        self._create_drones()
        self._prepare_paths()

    def _create_drones(self):
        # Create all drones at the start zone.
        for drone in range(1, self.graph.nb_drones + 1):
            id = f"D{drone}"
            starting_zone = self.graph.start_zone
            self.drones.append(Drone(id, starting_zone))

    def _prepare_paths(self):
        if not self.pathfinder.path_exists():
            raise RuntimeError("No path found")

        for drone in self.drones:
            # Assign an initial path to every drone.
            drone_path_names = self.pathfinder.find_path()

            # Convert zone names into Zone objects.
            for zone in drone_path_names:
                drone.path.append(self.graph.zones[zone])
            print(drone.id, [zone.name for zone in drone.path])
