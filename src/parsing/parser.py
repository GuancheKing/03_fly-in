from src.core.graph import Graph


class MapError(Exception):
    def __init__(self, msg: str, filename: str):
        super().__init__(f"Error parsing input file {filename}: {msg}")


class MapParser():
    def __init__(self, filename: str):
        self.filename = filename

    def parse(self) -> Graph:
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

                print(line_number, clean_line)

        return graph
