from src.parsing.parser import MapParser


def main() -> None:
    parser = MapParser("/home/pepo/projects/repos/42/03/03_fly_in/maps/hard/01_maze_nightmare.txt")
    graph = parser.parse()


if __name__ == "__main__":
    main()