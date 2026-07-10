*This project has been created as part of the 42 curriculum by @josjimen.*

# Fly-in
An object-oriented drone routing and traffic simulation written in Python.

## Description
Fly-in is a drone routing simulator that computes efficient paths through a graph of connected zones while respecting movement costs, zone occupancy and connection capacities.

The simulation aims to transport every drone from the start hub to the destination hub using the minimum possible number of turns.

The project was developed following an object-oriented design and implements a custom graph representation without using external graph libraries.

## Features
- Custom graph implementation
- Object-oriented architecture
- Capacity-aware simulation
- Restricted zones (2-turn movement)
- Priority and blocked zones
- Colored terminal visualization

## Project Structure
.
├── Makefile
├── README.md
├── main.py
├── requirements.txt
├── maps
│   ├── challenger
│   ├── easy
│   ├── hard
│   ├── medium
│   └── tests
└── src
    ├── core
    │   ├── connection.py
    │   ├── drone.py
    │   ├── graph.py
    │   └── zone.py
    ├── parsing
    │   └── parser.py
    ├── pathfinding
    │   └── pathfiner.py
    ├── simulation
    │   └── simulation.py
    └── visualization
        └── terminal_visualizer.py

Main responsibilities:

- main.py: parses command-line arguments and starts the simulation.
- core/: contains the main domain objects: graph, zones, connections and drones.
- parsing/: reads and validates map files.
- pathfinding/: calculates the weighted shortest path.
- simulation/: manages drone movement turn by turn.
- visualization/: displays the visual state of the simulation in the terminal.
- maps/: contains official maps and additional parser test cases.

## Input File Format
The program reads map files written in a custom text format.

A valid map must define:

- The number of drones.
- One start hub.
- One end hub.
- Zero or more intermediate hubs.
- Connections between previously defined zones.

Example: "this_is_a_map.txt"

nb_drones: 5

start_hub: start 0 0 [color=green]
hub: corridor_a 1 0 [zone=normal max_drones=2]
hub: tunnel 2 0 [zone=restricted color=red]
end_hub: goal 3 0 [color=yellow]

connection: start-corridor_a [max_link_capacity=2]
connection: corridor_a-tunnel
connection: tunnel-goal

Note: a map folder is provided with examples and tests for parsing/validation

## Instructions

### Requirements
The project requires:

Python 3.10 or later
make
pip

No external graph libraries are used.

### Installation
Install the project dependencies with:

make install

This command:

Creates a virtual environment in .venv.
Upgrades pip.
Installs the packages listed in requirements.txt.

### Running the Simulation
Run the program with:

make run MAP=path/to/map.txt

Example:

make run MAP=maps/easy/01_linear_path.txt

The MAP variable is mandatory and must contain the path to an existing map file.

If no map is provided, the Makefile displays an error message.

### Visual Mode
ath/to/map.txt

Example:

make visual MAP=maps/easy/02_simple_fork.txt

The visual mode displays:

- The current turn.
- Every zone in the graph.
- Zone type symbols.
- Current zone occupancy.
- Drone positions.
- Active connections.
- Current connection usage.

The mandatory movement output is still printed.

### Debugging
Run the program using Python's built-in debugger:

make debug MAP=path/to/map.txt

Example:

make debug MAP=maps/easy/01_linear_path.txt

This command starts the simulation through pdb.

Useful pdb commands include:

n: execute the next line.
s: enter a function.
c: continue execution.
p variable: print the value of a variable.
q: exit the debugger.

The program also provides a separate --debug option that prints simulation statistics after execution:
.venv/bin/python main.py maps/easy/01_linear_path.txt --debug

This mode displays:

- Total simulation turns.
- Total number of drones.

### Code Quality
Run Flake8 and Mypy with the mandatory project flags:

make lint

Run stricter Mypy checks with:

make lint-strict

The project dependencies used for code validation are:

- flake8
- mypy

### Cleaning the Project
Remove the virtual environment and cache files with:

make clean

This removes:

.venv
.mypy_cache
.pytest_cache
__pycache__ directories
.pyc files

Recreate the environment from scratch with:

make re

### Help
Display the available Makefile commands with:

make help

## Algorithm Explanation

### 1. Graph Representation
The map is represented as a custom undirected graph.

The Graph class stores:

- The total number of drones.
- A dictionary of zones indexed by name.
- A list of connections.
- An adjacency dictionary.
- References to the start and end zones.

Each zone is represented by a Zone object containing:

- Its name.
- Its coordinates.
- Its zone type.
- Its maximum capacity.
- Its current occupancy.
- Its optional display colour.
- Whether it is the start or end hub.

Each connection is represented by a Connection object containing:

- Its origin zone.
- Its destination zone.
- Its maximum capacity.
- Its current usage during the active turn.

Connections are bidirectional. When the parser reads a connection, it adds both directions to the adjacency dictionary.

Example:

connection: start-middle

Produces adjacency information equivalent to:

start -> middle
middle -> start
### 2. Pathfinding Strategy
The pathfinding algorithm searches for the lowest-cost route from the start hub to the end hub.

It follows a Dijkstra-style approach.

The algorithm maintains three main structures:

costs: stores the lowest known cost to reach each zone.
previous_nodes: stores the previous zone used to reach each zone.
pending: stores zones that still need to be explored.

The start hub begins with a cost of zero.

cost(start) = 0

During each iteration:

1. The pending zones are sorted by accumulated cost.
2. The zone with the lowest cost is selected.
3. Every adjacent zone is examined.
4. Blocked zones are ignored.
5. The movement cost of the neighbouring zone is added.
6. The neighbour is updated if the new path is cheaper.
7. The current zone is stored as its predecessor.

When the search finishes, a valid path exists if the end hub appears in the cost dictionary.

The final path is reconstructed backwards from the end hub using previous_nodes.

Example:

goal <- zone_b <- zone_a <- start

After reversing:

start -> zone_a -> zone_b -> goal
### 3. Path Cost Calculation
The cost of a path depends on the type of each destination zone.

Zone type	    Movement cost
normal	        1
priority	    1
restricted	    2
blocked	        Not traversable

For example:

start -> normal -> restricted -> goal

Has a total cost of:

1 + 2 + 1 = 4

Blocked zones are never added to a valid path.

In the current implementation, priority zones have the same numerical cost as normal zones. Therefore, a priority zone is not given an additional preference when two possible paths have the same total cost.
### 4. Drone Distribution

### 5. Turn Scheduling

### 6. Zone Capacity Management

### 7. Connection Capacity Management

### 8. Restricted Zones

### 9. Conflict and Deadlock Prevention

### 10. Performance Optimizations

### 11. Complexity

## Simulation Rules

### Zone Types

### Zone Occupancy

### Connection Capacity

### Movement Costs

## Visual Representation

## Error Handling

## Performance

## Testing

## Design Decisions and Trade-offs

## Resources

### Technical References

### Use of AI