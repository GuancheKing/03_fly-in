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
        self.previous_nodes: dict[str, str] = {}
        self.costs: dict[str, int] = {}
        self.path_priorities: dict[str, int] = {}

    def path_exists(self) -> bool:
        if self.graph.start_zone is None or self.graph.end_zone is None:
            raise PathError("Missing start or end zone", "PathFinder")

        start_name = self.graph.start_zone.name
        goal_name = self.graph.end_zone.name

        # Reset pathfinding state.
        self.costs = {
            start_name: 0
        }
        self.path_priorities = {
            start_name: 0
        }
        self.previous_nodes = {}

        # Priority queue of zones waiting to be explored.
        # Each entry stores:
        # (total_cost, -priority_score, zone_name)
        #
        # The negative priority score allows Python's default tuple sorting
        # to prefer paths that traverse more priority zones
        # when costs are same.
        pending = [
            (0, 0, start_name)
        ]
        while pending:
            # Process the best candidate first.
            # Paths are ordered by:
            #   1. Lowest total movement cost.
            #   2. Highest accumulated priority score.
            pending.sort()
            current_cost, negative_priority, current = pending.pop(0)
            # Convert the stored negative score back into
            # the accumulated priority score.
            current_priority = -negative_priority

            # Ignore outdated entries if a better path
            # to this zone has already been found.
            if (
                current_cost > self.costs[current]
                or (
                    current_cost == self.costs[current]
                    and current_priority < self.path_priorities[current]
                    )
            ):
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
                # Visiting a priority zone does not reduce the movement cost,
                # but increases the priority score used to break ties
                # between paths with the same total cost.
                priority_bonus = (
                    1 if neighbor_zone.zone_type == ZoneType.PRIORITY else 0
                )
                new_priority = current_priority + priority_bonus

                # Update the best known route if:
                # - the zone has not been visited yet,
                # - the new path has a lower total cost,
                # - or both paths have the same cost but the new one
                #   traverses more priority zones.
                if (
                    neighbor not in self.costs
                    or new_cost < self.costs[neighbor]
                    or (
                        new_cost == self.costs[neighbor]
                        and new_priority > self.path_priorities[neighbor]
                    )
                ):
                    self.costs[neighbor] = new_cost
                    self.previous_nodes[neighbor] = current
                    self.path_priorities[neighbor] = new_priority

                    # Store the updated candidate.
                    # The negative priority score ensures that paths with more
                    # priority zones are explored first when costs are equal.
                    pending.append((new_cost, -new_priority, neighbor))

        # A path exists if the goal was reached.
        return goal_name in self.costs

    def find_path(self) -> list[str]:
        if not self.previous_nodes:
            raise PathError(
                "Path has not been calculated yet",
                "PathFinder"
            )
        if self.graph.start_zone is None or self.graph.end_zone is None:
            raise PathError("Missing start or end zone", "PathFinder")

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
