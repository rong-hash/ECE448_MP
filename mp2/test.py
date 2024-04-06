import instances
import solve
from Pentomino import check_correctness

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
    pass
