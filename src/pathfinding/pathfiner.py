from src.core.graph import Graph


class PathError(Exception):
    def __init__(self, msg: str, filename: str):
        super().__init__(f"Error finding a path {filename}: {msg}")


class PathFinder:
    def __init__(self, graph: Graph):
        self.graph = graph
        # Stores the previous node used to reach each visited node.
        # This is later used to rebuild the final path.
        self.previous_nodes = {}

    def path_exists(self) -> bool:
        start_name = self.graph.start_zone.name
        goal_name = self.graph.end_zone.name

        # Track already visited nodes to avoid infinite loops.
        visited = {start_name}

        # Queue of nodes waiting to be explored.
        # BFS uses FIFO order.
        queue = [start_name]

        while queue:
            current = queue.pop(0)

            # Stop as soon as the destination is found.
            if current == goal_name:
                return True

            # Explore all unvisited neighbors of the current node.
            for neighbor in self.graph.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)

                    # Remember where this neighbor was reached from.
                    self.previous_nodes[neighbor] = current
                    queue.append(neighbor)
        return False

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
