from src.core.graph import Graph
from src.core.drone import Drone, DroneStatus
from src.core.zone import Zone
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
            # print(drone.id, [zone.name for zone in drone.path])

    def _apply_move(self, drone: Drone, destination: Zone):
        # Store the current zone before moving.
        origin = drone.current_zone

        # Update the occupancy of the origin zone.
        # Start and end hubs have unlimited capacity.
        if origin is not None and not origin.is_start_or_end:
            origin.current_occupancy -= 1

        # Update the occupancy of the destination zone.
        # Start and end hubs have unlimited capacity.
        if not destination.is_start_or_end:
            destination.current_occupancy += 1

        # Update the drone position and progress.
        drone.current_zone = destination
        drone.current_step += 1

    def run_turn(self):
        for drone in self.drones:
            if drone.current_zone is self.graph.end_zone:
                drone.status = DroneStatus.DELIVERED
                continue
            next_zone = drone.path[drone.current_step + 1]

            if next_zone.can_accept_drone():
                self._apply_move(drone, next_zone)
                drone.status = DroneStatus.MOVING
            else:
                drone.status = DroneStatus.WAITING

        print(
            f"Turn {self.turn}:",
            [f"{drone.id}-{drone.current_zone.name}" for drone in self.drones]
            )
        self.turn += 1
