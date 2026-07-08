from src.core.graph import Graph
from src.core.drone import Drone
from src.core.zone import Zone, ZoneType


class TerminalVisualizer:
    ZONE_SYMBOLS = {
            ZoneType.NORMAL: "⚪",
            ZoneType.BLOCKED: "⛔",
            ZoneType.RESTRICTED: "🚧",
            ZoneType.PRIORITY: "⭐",
        }

    def print_turn(
        self,
        turn: int,
        graph: Graph,
        drones: list[Drone]
    ) -> None:
        print(f"\n[Turn {turn}]")
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
                    f"({zone.current_occupancy}/{str(zone.max_drones)})"
                    )

            drones_text = " ".join(drones_here) if drones_here else "-"
            symbol = self._zone_symbol(graph, zone)

            zone_text = f"{symbol} {zone_name:<15}"
            zone_label = self._color_text(zone_text, zone.color)

            print(f"{zone_label} "
                  f"{occupancy_text:<5}"
                  f": {drones_text}")

    def _print_connections(self, graph: Graph) -> None:
        active_connections = []

        for connection in graph.connections:
            if connection.current_usage > 0:
                active_connections.append(connection)

        if not active_connections:
            return

        print(self._rainbow_text("\nActive connections:"))

        for connection in active_connections:
            name = ((connection.origin.name)
                    + " - "
                    + (connection.destination.name))
            usage = (
                f"{connection.current_usage}/"
                f"{connection.max_capacity}"
            )
            connection_text = f"🔗 {name}"
            print(f"{connection_text:<25} ({usage})")

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

    def _zone_symbol(self, graph: Graph, zone: Zone) -> str:
        if zone is graph.start_zone:
            return "🚀"
        if zone is graph.end_zone:
            return "🏁"
        return self.ZONE_SYMBOLS.get(zone.zone_type, "❓")
