import sys
from src.parsing.parser import MapParser, MapError
from src.simulation.simulation import Simulation, SimulationError
from src.pathfinding.pathfiner import PathError


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        return

    filename = sys.argv[1]

    try:
        graph = MapParser(filename).parse()
        simulation = Simulation(graph, debug=False)
        simulation.run()
    except (MapError, PathError, SimulationError) as error:
        print(error)
        return
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return


if __name__ == "__main__":
    main()
