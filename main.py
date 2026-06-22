from src.parsing.parser import MapParser
from src.pathfinding.pathfiner import PathFinder


def main() -> None:
    parser = MapParser("/home/pepo/projects/repos/42/03/03_fly_in/maps/easy/01_linear_path.txt")
    graph = parser.parse()
    finder = PathFinder(graph)
    print(finder.path_exists())
    print(finder.find_path())


if __name__ == "__main__":
    main()
