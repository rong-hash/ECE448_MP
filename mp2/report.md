# MP2 Report

- **Team Members:** Zhirong Chen (zhirong4), Xiaoyang Chu (xzhu58), Jiajun Hu (jiajunh5),  Yanbing Yang (yanbing7)
- **Date:** 4/6/2024

---

## Section I: Constraint Satisfaction Problem

In this section, we describe the algorithms and data structures used for searching a solution for pentomino tiling.

The approach we adopt is depth first search with least remaining value heuristic. Before we start, we construct a matrix of cells. Each cell will keep a record of all the viable pentominos placements(including differnet ways to place a pentomino, e.g. roation or fliping) that will cover the cell. During the dpeth first search, we will find out the cell with the least number of viable placement, and try to fill that cell in that iteration. After placing a pentomino in such a way that the cell is covered, we will propagate the newly introduced constraints to the all the cells. There are two kinds of new constraints. Firstly, the used pentomino will no longer be available for further use. Second, the viable placements stored in all the cells that are covered by the current placement of pentomino are nolonger valid, which may influcing neighboring cells. 

In case there are cells which doesn't have any viable placement, the search will return and the board will be restored to the state before the placement of that pentomino. If all the pentominos are used, a valid solution is found and the search will return with success. 

The following images illustrate the solutions found by the algorithm on the boards provided.

<div align ="center">

<img src=./img/3x20_pentnominos.png width = "300" alt="image" /><br/>
Fig. 3x20 Chessboard<br/>
<img src=./img/5x12_pentnominos.png width = "300" alt="image" /><br/>
Fig. 5x12 Chessboard<br/>
<img src=./img/6x10_pentnominos.png width = "300" alt="image" /><br/>
Fig .6x10 Chessboard<br/>
<img src=./img/empty_pentnominos.png width = "300" alt="image" /><br/>
Fig. Empty Chessboard<br/>
</div>

---

## Section II: Ultimate Tic-Tac-Toe: Results

minimax vs minimax, max first
```
O _ X O _ _ O X _
_ X _ _ _ _ _ _ _
X _ _ _ _ _ _ _ _

_ _ _ X _ O _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[704, 1391, 2000, 2656, 3175, 3749, 4308, 4895, 5246]
The winner is maxPlayer!!!
```
minimax vs alpha_beta, max first
```
O _ X O _ _ O X _
_ X _ _ _ _ _ _ _
X _ _ _ _ _ _ _ _

_ _ _ X _ O _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[704, 1037, 1646, 1934, 2453, 2723, 3282, 3591, 3942]
The winner is maxPlayer!!!
```
alpha_beta vs minimax, max first
```
O _ X O _ _ O X _
_ X _ _ _ _ _ _ _
X _ _ _ _ _ _ _ _

_ _ _ X _ O _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[284, 971, 1258, 1914, 2152, 2726, 2987, 3574, 3737]
The winner is maxPlayer!!!
```
alpha_beta vs alpha_beta, max first
```
O _ X O _ _ O X _
_ X _ _ _ _ _ _ _
X _ _ _ _ _ _ _ _

_ _ _ X _ O _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[284, 617, 904, 1192, 1430, 1700, 1961, 2270, 2433]
The winner is maxPlayer!!!
```
minimax vs minimax, min first
```
X _ O X _ X X O _
_ O _ _ _ _ _ O _
O _ _ _ _ _ _ _ _

_ _ _ O _ X _ O _
_ _ _ _ _ X _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[704, 1391, 2000, 2656, 3175, 3749, 4308, 4895, 5361, 5828, 6371, 6851, 7164]
The winner is minPlayer!!!
```
minimax vs alphabeta, min first
```
X _ O X _ X X O _
_ O _ _ _ _ _ O _
O _ _ _ _ _ _ _ _

_ _ _ O _ X _ O _
_ _ _ _ _ X _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[284, 971, 1258, 1914, 2152, 2726, 2993, 3580, 3792, 4259, 4551, 5031, 5208]
The winner is minPlayer!!!
```
alphabeta vs minimax, min first
```
X _ O X _ X X O _
_ O _ _ _ _ _ O _
O _ _ _ _ _ _ _ _

_ _ _ O _ X _ O _
_ _ _ _ _ X _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[704, 1037, 1646, 1934, 2453, 2723, 3282, 3624, 4090, 4362, 4905, 5181, 5494]
The winner is minPlayer!!!
```
alphabeta vs alphabeta, min first
```
X _ O X _ X X O _
_ O _ _ _ _ _ O _
O _ _ _ _ _ _ _ _

_ _ _ O _ X _ O _
_ _ _ _ _ X _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

[284, 617, 904, 1192, 1430, 1700, 1967, 2309, 2521, 2793, 3085, 3361, 3538]
The winner is minPlayer!!!
```

---
## Section III: Ultimate Tic-Tac-Toe: Agent Performance



---
## Section IV: Ultimate Tic-Tac-Toe: Human v.s. Agent



---

## Statement of Contribution
- Zhirong Chen: Implement the uttt code.
- Jiajun Hu: BFS, DFS
- Xiaoyang Chu: CSP
- Yanbing Yang: Greedy, Code Review

---



