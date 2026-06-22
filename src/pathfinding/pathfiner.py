from src.core.graph import Graph


class PathFinder:
    def __init__(self, graph: Graph):
        self.graph = graph

    def path_exists(self) -> bool:
        start_name = self.graph.start_zone.name
        goal_name = self.graph.end_zone.name

        visited = {start_name}
        queue = [start_name]

        while queue:
            current = queue.pop(0)

            if current == goal_name:
                return True

            for neighbor in self.graph.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
