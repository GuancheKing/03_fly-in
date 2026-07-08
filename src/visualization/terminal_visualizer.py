from src.core.graph import Graph
from src.core.drone import Drone


class TerminalVisualizer:
    def print_turn(
        self,
        turn: int,
        graph: Graph,
        drones: list[Drone]
    ) -> None:
        print(self._rainbow_text(f"\n[Turn {turn}]"))
        self._print_zones(graph, drones)
        self._print_connections(graph)

    def _print_zones(
            self,
            graph: Graph,
            drones: list[Drone]
            ) -> None:
        for zone_name, zone in graph.zones.items():
            drones_here = []

            for drone in drones:
                if drone.current_zone is zone:
                    drones_here.append(drone.id)

            if zone.is_start_or_end:
                occupancy_text = "∞"
            else:
                occupancy_text = (
                    f"{zone.current_occupancy}/{str(zone.max_drones)}"
                    )

            drones_text = " ".join(drones_here) if drones_here else "-"
            zone_label = self._color_text(zone_name, zone.color)

            print(f"{zone_label} "
                  f"({occupancy_text})"
                  f": {drones_text}")

    def _print_connections(self, graph: Graph) -> None:
        print(self._rainbow_text("\nConnections:"))

        for connection in graph.connections:
            name = (
                self._color_text(
                    connection.origin.name,
                    connection.origin.color
                    )
                + "-"
                + self._color_text(
                    connection.destination.name,
                    connection.destination.color
                    ))
            usage = (
                f"{connection.current_usage}/"
                f"{connection.max_capacity}"
            )
            print(f"{name} ({usage})")

    def _color_text(self, text: str, color: str | None) -> str:
        colors = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
        }

        reset = "\033[0m"

        if color not in colors:
            return text

        return f"{colors[color]}{text}{reset}"

    def _rainbow_text(self, text: str) -> str:
        new_text = []
        colors_list = [
            "red", "green",
            "yellow", "blue", "magenta",
            "cyan"
            ]
        for index, letter in enumerate(text):
            color = index % len(colors_list)
            new_text.append(self._color_text(letter, colors_list[color]))
        return "".join(new_text)
