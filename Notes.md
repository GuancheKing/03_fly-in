Zone
- name
- coords
- zone_type: normal / blocked / restricted / priority
- max_drones
- color
- current_occupancy

Connection
- origin
- destination
- max_capacity
- current_usage

Drone
- id
- current_zone
- target_zone
- path
- status: waiting / moving / delivered
- current step

Graph
- zones
- connections
- adjacency list

PathFinder - calculates routes
- receives Graph
- finds possible routes
- calculates route cost
- ignores blocked zones

TrafficManager
- receives drones + graph state
- proposes/validates movements
- solves conflicts
- decides who waits

Simulation - decides movements
- owns the main loop
- current_turn
- asks TrafficManager what happens
- applies valid movements
- stops when all drones arrive

Renderer - shows results
- prints mandatory output
- optionally prints visual themed output

Parser
- reads map file
- validates syntax
- builds Graph, Zones, Connections, drones count