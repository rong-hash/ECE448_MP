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

In 20 games, our agent beat predefined agent for all times. Here's the selected representative games. Our agent is the maxPlayer.
```
Game  0
O _ X X O O O X _
_ X _ X _ _ _ X _
X _ _ _ _ _ _ _ _

O X _ _ _ O _ _ _
_ _ _ O _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

expand nodes [277, 599, 933, 1219, 1498, 1792, 2131, 2412, 2691, 2960, 3331, 3587, 3854, 4142, 4340]
The winner is maxPlayer!!!

Game  1
X _ O _ _ _ O _ X
X _ _ _ _ _ O _ _
X _ _ _ _ _ _ _ _

O _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
X _ _ _ _ _ _ _ _

O _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

expand nodes [284, 599, 836, 1087, 1300, 1566, 1845, 2070, 2322, 2482]
The winner is maxPlayer!!!

Game  2
X _ O O _ X X O _
X O _ _ X _ _ O _
X _ _ _ _ _ _ _ _

_ _ _ O X X _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

O O _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

expand nodes [284, 617, 904, 1194, 1432, 1729, 1994, 2322, 2532, 2829, 3093, 3297, 3560, 3771, 3989, 4132]
The winner is maxPlayer!!!

Game  3
X _ O O _ X X O _
_ O _ O _ _ _ O _
_ _ _ _ _ _ _ _ _

_ _ _ X X X _ _ _
X O _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _

expand nodes [277, 599, 933, 1219, 1498, 1785, 2123, 2412, 2690, 2978, 3221, 3587, 3929, 4213]
The winner is maxPlayer!!!
```

The main reason that our agent is better than the predefined agent is, the predefined agent's evaluation function only calculate the score of its own chess piece, but don't consider the opponent chess piece. For example, in the initial game, which both side use minimax strategy, the result is
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
```
The last move done by minPlayer 'O' chooses to place its piece on the left upper corner in the second local board. However, next iteration, maxPlayer will definitely win the game, because it already has 2 'X' in a row in the first local board. Because the minPlayer only calculate the benefit of its own piece, but doesn't calculate the loss caused by its move, the minPlayer lose the game.

Therefore, based on this shortcoming, we add a loss score in our evaluation function. The maxPlayer will not only add score in the total score, but also delete the score when it find its move will benefit the opponent much more than itself, for instance, let the opponent win directly. Based on this evaluation function, our agent beat the original predefined agent 20 times out of 20 times.

---
## Section IV: Ultimate Tic-Tac-Toe: Human v.s. Agent



---

## Statement of Contribution
- Zhirong Chen: Implement the uttt code.
- Jiajun Hu: BFS, DFS
- Xiaoyang Chu: CSP
- Yanbing Yang: Greedy, Code Review

---



