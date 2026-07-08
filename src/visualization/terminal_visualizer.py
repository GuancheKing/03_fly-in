from src.core.graph import Graph
from src.core.drone import Drone


class TerminalVisualizer:
    def print_turn(
        self,
        turn: int,
        graph: Graph,
        drones: list[Drone]
    ) -> None:
        print(f"\n[Turn {turn}]")

        for zone_name, zone in graph.zones.items():
            drones_here = []

            for drone in drones:
                if drone.current_zone is zone:
                    drones_here.append(drone.id)

            drones_text = " ".join(drones_here) if drones_here else "-"
            print(f"{zone_name}: {drones_text}")
