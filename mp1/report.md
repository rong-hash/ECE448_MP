# MP1 Report

- **Team Members:** Zhirong Chen (zhirong4), Xiaoyang Chu (), Jiajun Hu (),  Yanbing Yang (yanbing7)
- **Date:** 3/17/2024

---

## Section I: Algorithms (Search)

In this section, we describe the algorithms and data structures used for implementing four search strategies: Depth-First Search (DFS), Breadth-First Search (BFS), Greedy Best-First Search (Greedy BFS), and A* Search.

### State and Node Representation

- **State:** In the context of your maze problem, a state represents the current condition or position within the maze. Specifically, it refers to a coordinate (x, y) indicating the location of the searcher (or agent) within the maze.  In both BFS and DFS implementations, a state is represented by the curNode or elements in the queue (for BFS) and stack (for DFS), which hold the current position in the maze.
- **Node:** In search algorithms, a node often refers to an element of the search tree that includes not just the state but also additional information such as the path taken to reach that state, the cost of the path, and potentially other metadata.
- **Difference:**  In BFS and DFS, the terms "node" and "state" are used interchangeably to refer to the position in the maze without additional metadata. Therefore, in this specific context, a node is essentially the same as a state.


### Frontier Management

The frontier is the set of all leaf nodes available for expansion at any given point in the search process. It's the "boundary" between the explored and unexplored areas of the search space.
- In BFS, the frontier is represented by the queue, which holds all the nodes that have been discovered but not yet explored.
- In DFS, the frontier is managed through the stack, containing nodes that have been discovered but whose neighbors haven't all been explored yet.

### Explored States List

An explored states list is a collection that keeps track of all the nodes (or states) that have been visited and explored, to prevent revisiting and re-exploring the same nodes, which ensures the efficiency of the search.
- In BFS, the parents dictionary serves a dual purpose: it maps each node to its parent (thereby implicitly tracking the path taken), and it also acts as a record of all nodes that have been visited (or explored), as nodes are added to parents once they are popped from the queue and processed.
- In DFS, explored nodes are implicitly tracked through the stack and the unreachable set. The unreachable set specifically helps to avoid revisiting nodes that have been determined to lead to dead ends or have already been explored.

### Repeated States Detection and Management
- BFS: Repeated states are managed through the parents dictionary. Before a node is added to the queue (i.e., the frontier), it is checked against the keys of the parents dictionary to ensure it hasn't been visited before.
- DFS: Repeated states are avoided by checking if a neighbor is already in the stack (which would indicate a loop) or if it is in the unreachable set (meaning it has been previously explored and found to lead to a dead end or has already been visited).

---

## Section II: Algorithms (A* and Greedy BFS)

This section focuses on the heuristic(s) used for A* and Greedy BFS, particularly for single-dot and multiple-dot scenarios.


### Heuristic(s) Used

#### Greedy Best-First Search (Greedy BFS)

- **Heuristic:** The heuristic function used for Greedy BFS calculates the Manhattan distance from the current node to the target node (the last objective). It is defined as `abs(target[0]-point.cord[0]) + abs(target[1]-point.cord[1])`, where `target` represents the coordinates of the target node, and `point.cord` represents the coordinates of the current node.
- **Single Dot Scenario:** In cases where there is only one dot (objective), this heuristic guides the search directly towards the goal, focusing solely on the distance to the goal without considering the cost of the path taken to reach that point.

#### A* Search

- **Heuristic:** The A* heuristic function combines the cost to reach the current node (`point.dist`, representing the distance from the start node to the current node) with the Manhattan distance to the target node. It is defined as `abs(target[0]-point.cord[0]) + abs(target[1]-point.cord[1]) + point.dist`.
- **Single Dot Scenario:** The heuristic effectively estimates the total cost of the cheapest solution through the current node, balancing the cost of reaching the current node and the estimated cost to reach the goal.
- **Multiple-Dot Situation:** `Needed to be finished by Xiaoyang`

### Admissibility of the A* Heuristic

A heuristic is admissible if it never overestimates the cost to reach the goal from any node in the search space. To prove the admissibility of the A* heuristic:

1. **Manhattan Distance:** The use of Manhattan distance as part of the heuristic ensures admissibility in a grid maze where only horizontal and vertical movements are allowed, as it exactly matches the minimum possible cost to reach the target from the current node (assuming a cost of 1 per step and no obstacles directly between the current node and the target).

2. **Path Cost Addition:** Adding the actual cost (`point.dist`) from the start node to the current node does not affect the admissibility because it is a concrete cost already incurred, not an estimate.

3. **Total Heuristic:** The total A* heuristic (`abs(target[0]-point.cord[0]) + abs(target[1]-point.cord[1]) + point.dist`) is the sum of the exact cost incurred to reach the current node and the admissible estimate of the remaining cost to the target. Since neither component overestimates the true cost, the overall heuristic is admissible.

In conclusion, the A* heuristic used in your implementation is admissible for the single dot scenario. For multiple-dot scenarios, while the heuristic remains admissible for reaching the final dot, the strategy does not inherently ensure an optimal path covering all dots, as it does not account for the necessity to visit each objective. 

---

## Section III: Results (Basic Pathfinding)

Present the results for each algorithm across different mazes. Include screenshots of the mazes with computed paths, solution costs, and the number of expanded nodes.

### DFS Results
- **Solution Cost and number of Expanded Nodes of DFS search trials:**
<div align ="center">
  
  |Maze|mediumMaze|bigMaze|openMaze|
  |:-:|:-:|:-:|:-:|
  |Solution Cost|131|211|299|
  |Number of Expanded Nodes|147|427|650|
</div>

- **Solution Graphs of DFS search trials:**
<div align ="center">
DFS search in mediumMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/ff1938de-dd42-49d6-a90d-217d00c65b5e width = "300" alt="image" /><br/><br/>
DFS search in bigMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/5f752363-a2cf-45f6-8bd3-2eb37d54ab37 width = "300" alt="image" /><br/><br/>
DFS search in openMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/fd5f8a8f-bffe-4cd9-98c2-77d80543f4ea width = "300" alt="image" /><br/><br/>
</div>
  
### BFS Results
- **Solution Cost and number of Expanded Nodes of BFS search trials:**
<div align ="center">
  
  |Maze|mediumMaze|bigMaze|openMaze|
  |:-:|:-:|:-:|:-:|
  |Solution Cost|69|211|55|
  |Number of Expanded Nodes|270|620|683|
</div>

- **Solution Graphs of BFS search trials:**
<div align ="center">
BFS search in mediumMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/181e3f5d-545a-42bb-95e9-05000ae2ac0e width = "300" alt="image" /><br/><br/>
BFS search in bigMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/9970e689-0b4b-4eba-87ef-96c953bd1054 width = "300" alt="image" /><br/><br/>
BFS search in openMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/d80781e9-2c0d-4157-9006-2ebaf73c57f0 width = "300" alt="image" /><br/><br/>
</div>

### Greedy Results
- **Solution Cost and number of Expanded Nodes of greedy search trials:**
<div align ="center">
  
  |Maze|mediumMaze|bigMaze|openMaze|
  |:----:|:----:|:----:|:----:|
  |Solution Cost|153|211|55|
  |Number of Expanded Nodes|158|457|212|
</div>

- **Solution Graphs of greedy search trials:**
<div align ="center">
Greedy search in mediumMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/db0cdb9b-0542-4164-97b2-0e23011fc5e2 width = "300" alt="image" /><br/><br/> 
Greedy search in bigMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/2cba816c-6ef7-4fa2-9ddf-707d689c1c46 width = "300" alt="image" /><br/><br/>
Greedy search in openMaze<br/>
<img src=https://github.com/SwordTechCorp/ece448_mp/assets/88780831/7a49cd65-5f90-4501-aee3-9ad632e185ec width = "300" alt="image" /><br/><br/>
</div>

### A* Results

- (Repeat the structure used for DFS results)

---

## Section IV: Results (Search with Multiple Dots)

Discuss the outcomes of employing your A* algorithm on mazes with multiple dots. Include screenshots, solution costs, and the number of expanded nodes.

### Tiny Maze

- (Image), Solution Cost, Number of Expanded Nodes

### Small Maze

- (Image), Solution Cost, Number of Expanded Nodes

### Medium Maze

- (Image), Solution Cost, Number of Expanded Nodes

---


## Statement of Contribution
- Zhirong Chen: Write the report
- Jiajun Hu: BFS, DFS
- Xiaoyang Chu: A*, Greedy
- Yanbing Yang: Greedy, Code Review

---

