from src.core.graph import Graph
from src.core.zone import ZoneType


class PathError(Exception):
    def __init__(self, msg: str, filename: str):
        super().__init__(f"Error finding a path {filename}: {msg}")


class PathFinder:
    def __init__(self, graph: Graph):
        self.graph = graph
        # Stores the previous node used to reach each visited node.
        # This is later used to rebuild the final path.
        self.previous_nodes = {}
        self.costs = {}

    def path_exists(self) -> bool:
        start_name = self.graph.start_zone.name
        goal_name = self.graph.end_zone.name

        # Stores the minimum known cost to reach each zone.
        self.costs = {
            start_name: 0
        }
        # Stores the previous zone used to reach each zone.
        # This is later used to rebuild the final path.
        self.previous_nodes = {}

        # Zones waiting to be explored.
        # Each entry stores (current_cost, zone_name).
        pending = [
            (0, start_name)
        ]
        while pending:
            # Always process the zone with the lowest known cost.
            pending.sort()
            current_cost, current = pending.pop(0)

            # Ignore outdated entries if a better path
            # to this zone has already been found.
            if current_cost > self.costs[current]:
                continue

            # Explore every reachable neighbor.
            for neighbor in self.graph.adjacency[current]:
                neighbor_zone = self.graph.zones[neighbor]
                # Blocked zones cannot be traversed.
                if neighbor_zone.zone_type == ZoneType.BLOCKED:
                    continue
                # Calculate the total cost to reach the neighbor.
                neighbor_cost = neighbor_zone.movement_cost()
                new_cost = current_cost + neighbor_cost

                # Update the path if this route is cheaper
                # than any previously known route.
                if (
                    neighbor not in self.costs
                    or new_cost < self.costs[neighbor]
                ):
                    self.costs[neighbor] = new_cost
                    self.previous_nodes[neighbor] = current
                    pending.append((new_cost, neighbor))

        # A path exists if the goal was reached.
        return goal_name in self.costs

    # def path_exists_BFS(self) -> bool:
    #     start_name = self.graph.start_zone.name
    #     goal_name = self.graph.end_zone.name

    #     # Track already visited nodes to avoid infinite loops.
    #     visited = {start_name}

    #     # Queue of nodes waiting to be explored.
    #     # BFS uses FIFO order.
    #     queue = [start_name]

    #     while queue:
    #         current = queue.pop(0)

    #         # Stop as soon as the destination is found.
    #         if current == goal_name:
    #             return True

    #         # Explore all unvisited neighbors of the current node.
    #         for neighbor in self.graph.adjacency.get(current, []):
    #             if neighbor not in visited:
    #                 visited.add(neighbor)

    #                 # Remember where this neighbor was reached from.
    #                 self.previous_nodes[neighbor] = current
    #                 queue.append(neighbor)
    #         return False

    def find_path(self) -> list[str]:
        if not self.previous_nodes:
            raise PathError(
                "Path has not been calculated yet",
                "PathFinder"
            )
        start_name = self.graph.start_zone.name
        goal_name = self.graph.end_zone.name

        # Rebuild the path backwards, starting from the goal.
        current = goal_name
        path = [goal_name]

        while current != start_name:
            current = self.previous_nodes[current]
            path.append(current)

        # Reverse the path so it goes from start to goal.
        return path[::-1]
