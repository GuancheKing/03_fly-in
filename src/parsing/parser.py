from src.core.graph import Graph
from src.core.zone import Zone, ZoneType
from src.core.connection import Connection


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

                    # Create the Zone object from the parsed hub definition.
                    zone = Zone(name, coords)

                    # Extract optional metadata declared inside brackets.
                    # Example:
                    # [color=yellow max_drones=2 zone=restricted]
                    metadata = self._parse_metadata(value)

                    # Apply optional display attributes.
                    if "color" in metadata:
                        zone.color = metadata["color"]

                    # Parse and validate zone capacity settings.
                    # Metadata values are extracted as strings and
                    # must be converted to their expected types.
                    if "max_drones" in metadata:
                        try:
                            zone.max_drones = int(metadata["max_drones"])
                            if zone.max_drones < 1:
                                raise MapError(
                                    "Max_drones in zone must be > 1",
                                    f"{self.filename}:{line_number}"
                                )
                        except ValueError:
                            raise MapError(
                                "Invalid type for max_drones: "
                                f"{metadata['max_drones']}",
                                f"{self.filename}:{line_number}"
                            )

                    # Parse and validate the zone type.
                    # Only values defined in ZoneType are accepted.
                    if "zone" in metadata:
                        try:
                            zone.zone_type = ZoneType(metadata["zone"])
                        except ValueError:
                            raise MapError(
                                f"Invalid zone type: {metadata['zone']}",
                                f"{self.filename}:{line_number}"
                            )

                    # Register the zone in the graph
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

                # Parse connection definitions.
                # Expected format:
                # zone1-zone2 [optional metadata]
                elif key.lower() == "connection":
                    # Remove optional metadata and keep only:
                    # zone1-zone2
                    basic_part = value.split("[")[0].strip()

                    # Validate connection format.
                    # A connection must link exactly two zones.
                    parts = basic_part.split("-")
                    if len(parts) != 2:
                        raise MapError(
                            "Field Connection must be formatted as 'connection:"
                            " zone1-zone2'",
                            f"{self.filename} : {line_number}"
                        )

                    # Extract origin and destination zone names.
                    origin_name, destination_name = parts

                    # Resolve zone names into actual Zone objects.
                    origin = graph.zones.get(origin_name)
                    destination = graph.zones.get(destination_name)

                    # Connections reference existing zones.
                    # Reject connections pointing to unknown zones.
                    if origin is None:
                        raise MapError(
                            "Unknown zone referenced in connection:"
                            f" {origin_name}",
                            f"{self.filename}:{line_number}"
                            )
                    if destination is None:
                        raise MapError(
                            "Unknown zone referenced in connection:"
                            f" {destination_name}",
                            f"{self.filename}:{line_number}"
                            )

                    # Create the Connection object.
                    connection = Connection(
                        origin,
                        destination
                    )

                    metadata = self._parse_metadata(value)

                    if "max_link_capacity" in metadata:
                        try:
                            connection.max_capacity = int(
                                metadata["max_link_capacity"]
                                )
                            if connection.max_capacity < 1:
                                raise MapError(
                                    "Max_capacity in connection must be > 1",
                                    f"{self.filename}:{line_number}"
                                )

                        except ValueError:
                            raise MapError(
                                "Invalid type for max_link_capacity: "
                                f"{metadata['max_link_capacity']}",
                                f"{self.filename}:{line_number}"
                            )

                    # Register the connection in the graph.
                    graph.connections.append(connection)

                    # Update graph adjacency information.
                    # Connections are considered bidirectional.
                    if origin_name not in graph.adjacency:
                        graph.adjacency[origin_name] = []
                    graph.adjacency[origin_name].append(destination_name)

                    if destination_name not in graph.adjacency:
                        graph.adjacency[destination_name] = []
                    graph.adjacency[destination_name].append(origin_name)

        # Validate graph-wide requirements.
        # A valid map must contain exactly one start hub
        # and exactly one end hub.
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

        if graph.nb_drones is None:
            raise MapError(
                "Map must define nb_drones",
                f"{self.filename}:{line_number}"
                )

        if graph.nb_drones < 1:
            raise MapError(
                "Invalid value for nb_drones",
                f"{self.filename}:{line_number}"
                )
        
        # DEBUGGING printeos
        # print(graph.nb_drones)
        # print(graph.start_zone.name)
        # print(graph.end_zone.name)
        # print(len(graph.zones))
        # print(len(graph.connections))
        # debug adjacency - print(graph.adjacency)
        # debug - print(line_number, clean_line)
        return graph

    def _parse_metadata(self, value: str) -> dict[str, str]:
        if "[" not in value:
            return {}
        raw_data = value.split("[")[1].split("]")[0]
        data_list = raw_data.split(" ")
        metadata = {}
        for item in data_list:
            key, value = item.split("=")
            metadata[key] = value
        return metadata

