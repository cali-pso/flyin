*This project has been created as part of the 42 curriculum by rapoggi*

## Description

This is my implementation of the Fly-In project from 42's curriculum. It aims 
to help a fleet of drones navigate from a given start point to a given end point 
within a given map. This involves parsing a text file representing the map and 
holding the relevant metadata, then using a path-finding algorithm that handles 
not solely space but also time - we need to organize our fleet's movements in turns 
such that drones don't crash into each other, or end up in the wrong place at 
the wrong time. 

## Instructions

This project uses uv for automatic virtual environment management.  
  
A Makefile has been provided. Run:  

```Bash
    make install
```
> to install dependencies needed by the project.
  
To execute run:  
```Bash
    make run
```
> this will pass the config.txt file in the repository as a map to the program 
   
To use a custom map, either change the config.txt file or run:
```Bash
    uv run python3 main.py [CUSTOM_MAP] --visual
```


To remove cached folders and files, as well as venv and info created by uv:  
```Bash
    make clean
```
 
To run flake8 and mypy on current directory:  
```Bash
    make lint
```

## Resources

<https://en.wikipedia.org/wiki/A*_search_algorithm>  
For reference about the A* search algorithm: the one I've used in this project.  
<https://en.wikipedia.org/wiki/Admissible_heuristic>  
<https://en.wikipedia.org/wiki/Consistent_heuristic>  
<https://en.wikipedia.org/wiki/Glossary_of_graph_theory>  
For a better understanding of the concepts that support my algorithm, and of 
graph theory overall.

AI was used as a way to discover the different algorithms I could implement, 
and ways I could optimize the one I've chosen. 
As well as a help understanding complex heuristics-related concepts, rewording 
some of the Wikipedia articles.

## Algorithm explanation

I chose to implement a space-time variant of the A* pathfinding algorithm.
This implied the use of a 'reservation table' to keep track of the drones 
movements through time, while the A* figured out the movement themselves.
Before making a move, the algorithm asks the table wether it's target hub 
at it's target turn is available. The table checks the hub's current and 
maximum capacity, and answers accordingly, allowing the algorithm to make 
it's choice. 

The A* algorithm works by comparing every possible move by their 'f_score'.
This f score is the addition of the steps taken to move to the point we 
are currently at, and the estimated amount of steps needed to get to our goal. 
The estimation is done by a simple, admissible and consistent heuristic function. 
I have chosen to use the Manhattan Distance function as my heuristic. Although 
meant for grid based problems, it works satisfyingly well in our graph case.
It simply returns this:
```Python
abs(current_hub.x - goal_hub.x) + abs(current_hub.y - goal_hub.y)
```

So we have a ReservationTable class, a PathFinder class (applies A*), a Scout 
class (checks for map being solvable with BFS before moving onto complex A*) and 
a SearchState class. The search state is a specific point in our A* search tree. 
It holds a point in space (hub), a point in time (turn), a history of hubs 
traversed to get here, and the f_score obtained from our heuristic function.

Here is a pseudocode breakdown of the PathFinder's A*:

```Pseudo
- Initialize a priority queue with a first search state made from start_node
        (This queue will hold search states ordered by their f_score)


- While the queue is not empty:

    - Pop first node from queue (lowest f_score) and make it current state

    - If current state's hub is goal_hub, return current state's history

    - Ask table for current state's hub availability at next turn.
        - If possible, push a new search state into the queue:
            current state's hub, next turn, appropriate history and f_score
            (this is our waiting option - crucial for availability management)

    - For each of the current state's hub neighbours:
        - Establish target turn : next if normal/priority, next + 1 if restricted
        - Ask table if neighbour is available at target turn
            - If available, push a new search state into the queue:
            neighbour, target turn, appropriate history and f_score
            (f_score is artificially lowered for priority hubs - this makes them 
             automatically prefered when popping from queue at loop start)


- Once the goal has been reached and the history (path) returned, reserve each 
   of it's hubs at each turn in the table, prevents collisions from future drones.
```

The search states are automatically ordered within the queue thanks to dataclasses
and heapq. Heapq automatically sorts pushed elements, and dataclasses allows for 
the sorting key to be a SearchState's f_score.

## About the visualiser

Built with pygame, it is meant to be minimalist while providing all the useful 
information and a useful animation of the simulation. In the top-left corner 
is displayed turns information as
``` Python
f"{current_turn}"/f"{total_turns}"
```
If a hub has a type different from normal - wether it is start, end, obstacle, 
restricted or priority - this information is displayed at the top-right corner 
of said hub. On it's top-left corner is usage at current turn - if not 0.
The hubs are drawn in the color specified in the map. The visualiser closes 
automatically at the end of the simulation. No controls other than closing the 
window safely have been implemented.

## Expected input/output

Example input:

```Text

nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Expected output for example input:

```Text
D1-waypoint1 D2-start
D1-waypoint2 D2-waypoint1
D2-waypoint2 D1-goal
D2-goal
```

