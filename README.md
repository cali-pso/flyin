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
> this will fetch the config.txt file in the repository and use it as map  
   
```Bash
    make clean
```
> removes cached folders and files, as well as venv and info created by uv  
 
```Bash
    make lint
```
> runs flake8 and mypy on current directory  

## Resources

<https://en.wikipedia.org/wiki/A*_search_algorithm>  
For reference about the A* search algorithm: the one I've used in this project.  
<https://en.wikipedia.org/wiki/Admissible_heuristic>  
<https://en.wikipedia.org/wiki/Consistent_heuristic>  
<https://en.wikipedia.org/wiki/Glossary_of_graph_theory>  
For a better understanding of the concepts that support my algorithm, and of 
graph theory overall.

AI was used as a way to discover the different algorithms I could implement, 
as well as an help understanding complex heuristics-related concepts, 
rewording some of the Wikipedia articles.

## About the algorithm

I chose to implement the A* pathfinding algorithm paired with a 'reservation 
table' system. The A* takes care of the space dimension, while the table handles 
time. 
The reservation table is a nested dictionnary : one entry for each turn, 
and at each entry a dictionnary that holds one drone's position per entry.
 
At the very beginning, a quick BFS is ran to ensure start_hub and end_hub are 
linked by connections and the map can be resolved.

Starting from a random first drone : 
 
The A* algorithm works in such a way that each of the steps taken is a choice made 
from mainly two numbers: first, the number of steps it took us to get here. 
Then, the estimated cost to get to the end, obtained by a consistent, admissible 
heuristic function. This means that the cost will never be over-estimated - nor 
running the function in an identical situation will result in a different 
estimation. 
It also ensures the move is possible within the rules specific to our context : 
The hub is not an obstacle, and it is not overcrowded at the current turn.
In case of a restricted hub, or an overcrowded hub, waiting is an option.
If neighbour is a priority hub, it will without fault be prioritized.
 
Once the drone has reached it's goal, it's path is reserved within the table:
Hubs' loads at each turn are updated. This allows for the remaining drones to 
avoid overcrowding said hubs.

This resolves in a very cost efficient planned route: the infamous challenger map 
is solved in exactly 45 turns.

## About the visualiser

Built with pygame, it is meant to be minimalist while providing all the useful 
information and provide a useful render of the simulation. In the top-left corner 
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
