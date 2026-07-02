import sys
from src.parsing.parser import MapParser
from src.simulation.simulation import Simulation


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        return

    filename = sys.argv[1]

    graph = MapParser(filename).parse()

    simulation = Simulation(graph, debug=True)
    simulation.run()


if __name__ == "__main__":
    main()
