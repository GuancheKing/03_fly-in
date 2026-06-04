from src.core.graph import Graph
from src.core.zone import Zone


class MapError(Exception):
    def __init__(self, msg: str, filename: str):
        super().__init__(f"Error parsing input file {filename}: {msg}")


class MapParser():
    def __init__(self, filename: str):
        self.filename = filename

    def parse(self) -> Graph:
        """
        Parse a map file and build a Graph object.

        Responsibilities:
        - Read and validate map lines.
        - Create Zone objects.
        - Create Connection objects.
        - Populate graph metadata.
        - Raise MapError when the map is invalid.

        Returns:
            Graph: Fully populated graph representation of the map.
        """
        graph = Graph()

        with open(self.filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                clean_line = line.strip()

                if not clean_line:
                    continue

                if clean_line.startswith("#"):
                    continue

                key, value = clean_line.split(":")
                key = key.strip()
                value = value.strip()

                # Parse number of drones and validate it is an integer.
                if key.lower() == "nb_drones":
                    try:
                        graph.nb_drones = int(value)
                    except ValueError:
                        raise MapError(
                            f"{key.lower()} must be an integer value",
                            f"{self.filename}:{line_number}"
                        )

                # Parse hub definitions (start_hub, hub, end_hub).
                # Expected format:
                # <name> <x> <y> [optional metadata]
                elif key.lower() in ("start_hub", "hub", "end_hub"):

                    # Remove optional metadata and keep only:
                    # <name> <x> <y>
                    basic_part = value.split("[")[0]
                    parts = basic_part.split()

                    # Validate that the hub definition contains exactly:
                    # name, x coordinate and y coordinate.
                    if len(parts) != 3:
                        raise MapError(
                            "Zone info must include name and coords (x, y)",
                            f"{self.filename}:{line_number}"
                            )
                    name, x, y = parts

                    # Convert coordinates from strings to integers.
                    # Reject invalid values such as:
                    # hub: test abc 10
                    try:
                        coords = (int(x), int(y))
                    except ValueError:
                        raise MapError(
                            "Coordinates must be integers",
                            f"{self.filename}:{line_number}"
                        )
                    if name in graph.zones:
                        raise MapError(
                            f"Duplicated hub name: {name}",
                            f"{self.filename}:{line_number}"
                        )

                    # Create the Zone object and register it in the graph.
                    zone = Zone(name, coords)
                    graph.zones[name] = zone

                    # Track special hubs used as simulation entry/exit points.
                    if key.lower() == "start_hub":
                        if graph.start_zone:
                            raise MapError(
                                f"Duplicated start zone: {name}",
                                f"{self.filename}:{line_number}"
                            )
                        graph.start_zone = zone
                    elif key.lower() == "end_hub":
                        if graph.end_zone:
                            raise MapError(
                                f"Duplicated end zone: {name}",
                                f"{self.filename}:{line_number}"
                            )
                        graph.end_zone = zone

        if graph.start_zone is None:
            raise MapError(
                "Missing start zone in map",
                f"{self.filename}:{line_number}"
                )

        if graph.end_zone is None:
            raise MapError(
                "Missing end zone in map",
                f"{self.filename}:{line_number}"
                )

        print(line_number, clean_line)
        return graph
