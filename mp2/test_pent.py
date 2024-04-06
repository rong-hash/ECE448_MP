import instances
import solve
from Pentomino import check_correctness
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    boards = {"3x20":instances.board_3x20, 
              "5x12":instances.board_5x12,
              "6x10":instances.board_6x10,
              "empty":instances.empty_chessboard}
    inos =  {"dominos":instances.dominos, 
              "triominos":instances.triominos,
              "pentnominos":instances.pentnominos}
    for board in boards.keys():
        for ino in inos.keys():
            print(f"Solve Board:{board} with {ino}...",end='')
            sol_list = solve.solve(boards[board], inos[ino])
            if check_correctness(sol_list, boards[board], inos[ino]):
                print("PASSED!")
            else:
                print("FAILED...")
            drawboard = np.copy(boards[board])
            for sol in sol_list:
                drawboard[sol[1][0]:sol[1][0]+sol[0].shape[0],sol[1][1]:sol[1][1]+sol[0].shape[1]] += sol[0]
            drawboard = drawboard.repeat(30, axis=0).repeat(30, axis=1)
            plt.imsave(f"img/{board}_{ino}.png",drawboard)
    pass
