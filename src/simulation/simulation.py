from src.core.graph import Graph
from src.core.drone import Drone, DroneStatus
from src.core.zone import Zone
from src.pathfinding.pathfiner import PathFinder


class Simulation:

    def __init__(self, graph: Graph, debug: bool = False):
        self.graph = graph
        self.pathfinder = PathFinder(self.graph)
        self.turn = 0
        self.debug = debug
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
        # Process one simulation turn.
        for drone in self.drones:
            # Skip drones that have already been delivered.
            if drone.current_zone is self.graph.end_zone:
                drone.status = DroneStatus.DELIVERED
                continue
            # Get the next zone in the planned path.
            next_zone = drone.path[drone.current_step + 1]

            if next_zone.can_accept_drone():
                self._apply_move(drone, next_zone)
                drone.status = DroneStatus.MOVING
            # Wait until the destination becomes available.
            else:
                drone.status = DroneStatus.WAITING

        self.turn += 1

    def _all_drones_at_goal(self):
        # Check whether all drones have reached the destination.
        for drone in self.drones:
            if drone.current_zone is not self.graph.end_zone:
                return False
        return True

    def _print_turn(self):
        # Collect all drone movements for the current turn.
        turn_output = []

        for drone in self.drones:
            if drone.status == DroneStatus.MOVING:
                drone_output = f"{drone.id}-{drone.current_zone.name}"
                turn_output.append(drone_output)
        if turn_output:
            # Print the turn only if at least one drone moved.
            print(" ".join(turn_output))

    def _print_statistics(self):
        print("\n====================")
        print("Simulation finished")
        print("====================")
        print(f"Total turns : {self.turn}")
        print(f"Drones      : {len(self.drones)}")

    def run(self):
        # Run the simulation until all drones are delivered.
        while not self._all_drones_at_goal():
            self.run_turn()
            self._print_turn()

        # Show additional statistics in debug mode.
        if self.debug:
            self._print_statistics()
