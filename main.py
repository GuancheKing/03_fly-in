import argparse
from src.parsing.parser import MapParser, MapError
from src.simulation.simulation import Simulation, SimulationError
from src.pathfinding.pathfiner import PathError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the fly-in drone simulation."
    )

    parser.add_argument(
        "map_file",
        help="Path to the map file to simulate."
    )

    parser.add_argument(
        "--visual",
        action="store_true",
        help="Display a visual terminal representation each turn."
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Display simulation statistics after execution"
    )

    return parser.parse_args()


def main() -> None:

    args = parse_args()
    try:
        graph = MapParser(args.map_file).parse()
        simulation = Simulation(
            graph,
            debug=args.debug,
            visual=args.visual
            )
        simulation.run()

    except (MapError, PathError, SimulationError) as error:
        print(error)
        return

    except FileNotFoundError:
        print(f"File not found: {args.map_file}")
        return


if __name__ == "__main__":
    main()
