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
- Weighted Dijkstra-based pathfinding
- Restricted zones (2-turn movement)
- Priority and blocked zones
- Colored terminal visualization

## Project Structure
```text
.
├── Makefile
├── README.md
├── main.py
├── requirements.txt
├── maps/
│   ├── challenger/
│   ├── easy/
│   ├── hard/
│   ├── medium/
│   └── tests/
└── src/
    ├── core/
    │   ├── connection.py
    │   ├── drone.py
    │   ├── graph.py
    │   └── zone.py
    ├── parsing/
    │   └── parser.py
    ├── pathfinding/
    │   └── pathfinder.py
    ├── simulation/
    │   └── simulation.py
    └── visualization/
        └── terminal_visualizer.py
```

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

Example:

```text
nb_drones: 5

start_hub: start 0 0 [color=green]
hub: corridor_a 1 0 [zone=normal max_drones=2]
hub: tunnel 2 0 [zone=restricted color=red]
end_hub: goal 3 0 [color=yellow]

connection: start-corridor_a [max_link_capacity=2]
connection: corridor_a-tunnel
connection: tunnel-goal
...
```

The parser ignores blank lines and comments beginning with '#'.

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
make visual MAP=path/to/map.txt

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

## Usage Examples
### Example Input
The following example defines two drones travelling through a single intermediate zone:

nb_drones: 2

start_hub: start 0 0 [color=green]
hub: middle 1 0 [zone=normal color=blue]
end_hub: goal 2 0 [color=yellow]

connection: start-middle
connection: middle-goal

The map can be executed with:
make run MAP=maps/example.txt

### Example Output
D1-middle
D1-goal D2-middle
D2-goal

Each line represents one simulation turn:

Turn 1: D1 moves from start to middle.
Turn 2: D1 reaches goal while D2 moves to middle.
Turn 3: D2 reaches goal.

Drones that cannot move during a turn are omitted from the output.

Once a drone reaches the end hub, it is considered delivered and is no longer displayed in later turns.
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

Although each connection is stored as a single Connection object, the graph treats every connection as bidirectional by inserting both directions into the adjacency list.

Example:

connection: start-middle

Produces adjacency information equivalent to:

start -> middle
middle -> start

### 2. Pathfinding Strategy
The pathfinding algorithm searches for the lowest-cost route from the start hub to the end hub.
Routes are primarily optimized by total movement cost. When two routes have the same total cost, the algorithm prefers the one that traverses the largest number of priority zones.

It is based on Dijkstra's shortest-path algorithm.

The algorithm maintains four main structures:

- costs: stores the lowest known cost to reach each zone.
- previous_nodes: stores the previous zone used to reach each zone.
- path_priorities: stores the number of priority zones in the best known path to each visited zone
- pending: stores zones that still need to be explored.

The start hub begins with a cost of zero.

cost(start) = 0

During each iteration:

1. The pending zones are sorted by accumulated cost.
2. The zone with the lowest cost is selected.
3. Every adjacent zone is examined.
4. Blocked zones are ignored.
5. The movement cost of the neighbouring zone is added.
6. The neighbour is updated if the new path has a lower total cost, or if both paths have the same cost but the new one traverses more priority zones.
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

Priority zones have the same movement cost as normal zones.

However, when two candidate paths have the same total movement cost, the algorithm prefers the path that traverses the highest number of priority zones.

This tie-breaking strategy preserves the optimal path cost while respecting the semantics of priority zones defined in the project specification.

### 4. Drone Distribution
Once the optimal path has been computed, every drone is assigned the same route from the start hub to the destination hub.

The pathfinding algorithm is executed only once. Each drone stores its own copy of the resulting path together with its current position along that route.

No attempt is made to distribute drones across multiple alternative paths. Instead, traffic naturally emerges from the simulation rules, where zone occupancy, connection capacity and movement costs determine when each drone is allowed to advance.

This separation keeps the routing algorithm independent from the movement scheduler and simplifies the overall design.

### 5. Turn Scheduling
The simulation advances one turn at a time until every drone reaches the destination hub.

During each turn, drones are processed sequentially in the order they were created.

For every drone, the scheduler performs the following steps:

1. Skip drones that have already reached the destination.
2. Complete the movement of drones currently crossing restricted zones.
3. Determine the next zone in the assigned path.
4. Verify that the destination zone has available capacity.
5. Verify that the connecting edge has available capacity.
6. Reserve the connection for the current turn.
7. Move the drone immediately or start a restricted-zone transit.

After every drone has been processed, the turn counter is incremented and the connection usage is reset for the next turn.

Because every drone is evaluated once per turn, no drone can perform more than one movement during the same simulation step.

### 6. Zone Capacity Management
Each zone maintains its current occupancy throughout the simulation.

Before a drone moves, the destination zone is checked to determine whether it can accept another drone. A movement is only allowed if the occupancy remains within the configured capacity.

The start and end hubs are treated as special cases and have unlimited capacity.

When a drone leaves a regular zone, its occupancy is decreased immediately. Likewise, when a drone enters a regular zone, its occupancy is increased immediately.

This guarantees that no two drones can simultaneously occupy a zone beyond its maximum capacity.

### 7. Connection Capacity Management
Each connection has a maximum number of drones that may use it during a single turn.

Before a drone moves, the simulation checks whether the selected connection has available capacity. If the limit has already been reached during the current turn, the drone must wait until the next one.

Unlike zones, connections do not remain occupied after a drone has crossed them. Instead, they only record how many drones have used them during the current turn.

At the end of every turn, the usage counter of every connection is reset, allowing them to be used again in the next simulation step.

This models throughput rather than permanent occupancy and prevents an excessive number of drones from crossing the same connection simultaneously.

### 8. Restricted Zones

Restricted zones require two turns to traverse instead of one.

When a drone starts moving towards a restricted zone:

- it immediately leaves its current zone;
- the destination zone reserves one occupancy slot;
- the drone enters an `IN_TRANSIT` state;
- the movement is completed during the following turn.

While a drone is in transit, it cannot begin another movement or occupy any intermediate zone.

Reserving the destination occupancy before arrival guarantees that no other drone can enter the same restricted zone while it is already being approached.

### 9. Conflict and Deadlock Prevention
The simulation prevents movement conflicts by enforcing all capacity constraints before a drone is allowed to move.

A movement is only performed when:

- the destination zone has available capacity;
- the selected connection has available capacity;
- the drone is not currently traversing a restricted zone.

If any of these conditions is not satisfied, the drone remains in the `WAITING` state and is evaluated again during the next turn.

Because every drone is processed once per turn and all occupancy values are updated immediately after each movement, later drones always observe the updated state of the simulation.

This deterministic scheduling avoids collisions and ensures that the simulation always respects the configured constraints.

### 10. Performance Optimizations
Although the project focuses on clarity rather than maximum performance, several implementation decisions reduce unnecessary work during the simulation.

The shortest path is computed only once before the simulation starts and is then reused by every drone.

Zone occupancy and connection usage are updated incrementally as drones move, avoiding repeated scans of the graph.

Dictionary lookups are used throughout the project to provide constant-time access to zones, costs and adjacency information.

The visualizer is completely independent from the simulation logic and is only executed when visual mode is enabled, preventing additional overhead during normal execution.

### 11. Complexity

The pathfinding implementation uses a sorted list of pending nodes instead of a priority queue. This simplifies the implementation while remaining efficient for the expected map sizes of the project.

## Simulation Rules
### Zone Types
Four zone types are supported:

| Zone type     | Description |
|-----------    |-------------|
| Normal        | Standard zone with a movement cost of 1 turn. |
| Priority      | Preferred zone. Movement also costs 1 turn, but routes traversing more        priority zones are preferred when multiple paths have the same total cost. |
| Restricted    | Crossing requires 2 turns. |
| Blocked       | Cannot be traversed and is ignored during pathfinding. |

### Zone Occupancy
Each regular zone has a configurable maximum occupancy.

A drone may only enter a zone if its current occupancy is below the configured limit.

The start and end hubs have unlimited capacity.

### Connection Capacity
Each connection defines the maximum number of drones that may use it during a single turn.

Connection usage is reset after every simulation turn.

### Movement Costs
Movement cost depends exclusively on the destination zone.

| Destination zone  | Cost |
|------------------ |------|
| Normal            | 1 |
| Priority          | 1 |
| Restricted        | 2 |
| Blocked           | Not traversable |

## Visual Representation
When visual mode is enabled (`make visual`), the simulator displays the complete state of the graph after every turn.

Each zone is represented by an icon indicating its type:

| Symbol    | Meaning |
|--------   |---------|
| 🚀        | Start hub |
| 🏁        | End hub |
| ⚪        | Normal zone |
| ⭐        | Priority zone |
| 🚧        | Restricted zone |
| ⛔        | Blocked zone |

For every zone, the visualizer displays:

- zone name;
- current occupancy;
- drones currently inside the zone.

Active connections used during the current turn are also displayed together with their current usage.

ANSI escape sequences are used to optionally display coloured zone names when supported by the terminal.

## Error Handling
The parser validates the input map before the simulation begins.

Examples of detected errors include:

- missing start or end hub;
- duplicated zones;
- duplicated start or end hubs;
- invalid coordinates;
- invalid capacities;
- unknown zone references;
- duplicated connections;
- disconnected graphs;
- invalid number of drones.

Errors are reported through dedicated exception classes with descriptive messages to simplify debugging.

## Performance
The simulator prioritises readability and correctness over aggressive optimisation.

Several implementation choices help keep execution efficient:

- constant-time dictionary lookups;
- a single pathfinding pass before the simulation starts;
- incremental occupancy updates;
- optional visualisation executed only when requested.

These choices provide good performance while keeping the code easy to understand and maintain.

## Testing
The repository includes several categories of maps:

- **easy/** — basic functionality.
- **medium/** — more complex routing scenarios.
- **hard/** — congestion and capacity stress tests.
- **challenger/** — advanced simulation scenario.
- **tests/** — invalid maps used to verify parser validation and error handling.

The project was additionally validated using:

- flake8;
- mypy;
- mypy --strict.

## Design Decisions and Trade-offs
Several design decisions were made to keep the project modular and easy to extend.

- Pathfinding and simulation are completely separated. The routing algorithm computes paths, while the simulation manages movement and traffic.
- A custom graph implementation was preferred (and requested by the subject) over external libraries to better understand the underlying algorithms.
- Dijkstra's algorithm was implemented using a sorted list instead of a priority queue. Although less efficient for very large graphs, this approach remains simple and appropriate for the expected project size.
- The terminal visualizer is independent from the simulation and can be enabled or disabled without affecting the simulation logic.
- Priority zones are implemented as a tie-breaking criterion instead of modifying movement costs, preserving the shortest-path property while respecting the project specification.

## Resources
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python enum documentation](https://docs.python.org/3/library/enum.html)

- ANSI color codes:
  - [Build your own command line with ANSI escape codes](https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors)

- Breadth-first search:
  - [BFS on Wikipedia](https://es.wikipedia.org/wiki/B%C3%BAsqueda_en_anchura)
  - [BFS video tutorial](https://youtu.be/gHHAZNuSTII?si=Mez_13E0sNkB1EYr)

- Dijkstra's shortest-path algorithm:
  - [Dijkstra on Wikipedia](https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra)
  - [Dijkstra video tutorial](https://www.youtube.com/watch?v=gq3cTlBMJhs)

- GitHub repositories from other 42 Madrid students:
  - [Carlos Gil Nieto — Fly-in](https://github.com/carlosgilnieto/fly-in)
  - [cdonairevillen — Flyin](https://github.com/cdonairevillen/Flyin)

### Use of AI
Artificial intelligence was used exclusively as a learning and mentoring tool throughout the development of this project.

It assisted with:

- understanding Python language features;
- discussing object-oriented design decisions;
- reviewing algorithms and data structures;
- improving code readability and documentation;
- debugging configuration and validation issues involving Makefiles, mypy and flake8.

All final code, architecture and implementation decisions were developed by the author, with AI used only to clarify concepts, review ideas and support the learning process.