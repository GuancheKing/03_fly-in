from src.core.graph import Graph
from src.core.drone import Drone
from src.pathfinding.pathfiner import PathFinder


class Simulation:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.path = PathFinder(self.graph)
        self.turn = 0
        self.drones = []
        self._create_drones()

    def _create_drones(self):
        for drone in range(1, self.graph.nb_drones + 1):
            id = f"D{drone}"
            starting_zone = self.graph.start_zone
            self.drones.append(Drone(id, starting_zone))
            

