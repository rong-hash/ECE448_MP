# MP1 Report

- **Team Members:** Zhirong Chen (zhirong4), Xiaoyang Chu (), Jiajun Hu (),  Yanbing Yang ()
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

### Heuristics Description

- **Single Dot Scenario:** Describe the heuristic(s) used and justify their selection.
- **Multiple Dot Scenario:** Explain how the heuristic(s) are adapted or developed for handling multiple goals.

### Admissibility of Heuristics

- Provide proof or a strong argument for the admissibility of the heuristics used in A*.

---

## Section III: Results (Basic Pathfinding)

Present the results for each algorithm across different mazes. Include screenshots of the mazes with computed paths, solution costs, and the number of expanded nodes.

### DFS Results

- **Medium Maze:** (Image), Solution Cost, Number of Expanded Nodes
- **Big Maze:** (Image), Solution Cost, Number of Expanded Nodes
- **Open Maze:** (Image), Solution Cost, Number of Expanded Nodes

### BFS Results

- (Repeat the structure used for DFS results)

### Greedy BFS Results

- (Repeat the structure used for DFS results)

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

## Extra Credit

If applicable, describe any additional work undertaken that you believe warrants extra credit.

---

## Statement of Contribution


---

