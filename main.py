from src.parsing.parser import MapParser
from src.simulation.simulation import Simulation


def main() -> None:
    parser = MapParser("/home/pepo/projects/repos/42/03/03_fly_in/maps/easy/01_linear_path.txt")

    graph = parser.parse()

    simulation = Simulation(graph, debug=True)
    simulation.run()


if __name__ == "__main__":
    main()
