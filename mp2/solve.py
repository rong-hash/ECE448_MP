# -*- coding: utf-8 -*-
import numpy as np
import instances

def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1
class Pentomino:
    def __init__(self, arrdef:np.ndarray) -> None:
        self.arrdef = arrdef
        self.mask = (arrdef != 0)
        self.typeIdx = get_pent_idx(arrdef) - 1
        self.hash = hash(str(arrdef))
        pass

    def __str__(self) -> str:
        return str(self.arrdef)

    def __hash__(self) -> int:
        return self.hash
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Pentomino):
            return False
        if np.all(self.arrdef == value.arrdef):
            return True
        return False

class Cell:
    def __init__(self, coord:tuple) -> None:
        self.viables = set()
        self.coord:tuple = coord
        pass
    def add_pent(self,pent:Pentomino,coord:tuple[int,int]) -> None:
        self.viables.add((pent,coord))
        pass
    def remove_pent(self,pent:Pentomino,coord:tuple[int,int]) -> list:
        self.viables.remove((pent,coord))
        return [(self, (pent,coord))]
    def remove_pent_index(self, idx:int) -> set:
        rl = set()
        i:tuple[Pentomino, tuple]
        for i in self.viables:
            if i[0].typeIdx == idx: rl.add((self,(i[0],i[1])))
        for i in rl:
            self.viables.remove(i[1])
        return rl

class Board:
    def __init__(self,arr:np.ndarray, pents_num:int) -> None:
        self.arr = np.zeros((arr.shape), dtype=object)
        self.taken = np.zeros((arr.shape), dtype=bool)
        self.taken[arr == 0] = True
        for i in range(arr.size):
            self.arr[i // arr.shape[1], i % arr.shape[1]] = Cell((i // arr.shape[1], i % arr.shape[1]))
        self.reflex:dict[tuple, set[Cell]] = dict()
        self.indexs = [set() for i in range(pents_num)]
        pass

    def add_reflex(self, key:tuple,cell:Cell):
        if (key in self.reflex.keys()):
            self.reflex[key].add(cell)
        else:
            new_set = set()
            new_set.add(cell)
            self.reflex[key] = new_set
    
def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You may assume there will always be a solution.
    """
    pent_list = []
    for i in range(len(pents)):
        pent = pents[i]
        for flipnum in range(3):
            p = np.copy(pent)
            if flipnum > 0:
                p = np.flip(pent, flipnum-1)
            for rot_num in range(4):
                pent_list.append(Pentomino(p))
                p = np.rot90(p)


    place = list()

    solve_board = Board(board, len(pents))

    for pent in pent_list:
        _conv(pent, solve_board)

    used = np.zeros(shape=(len(pents)),dtype=bool)
    
    if _solve(solve_board, used, place): return place

    return None

def _solve(board:Board,  used:np.ndarray, place:list[tuple[np.ndarray, tuple[int,int]]]) -> bool:
    if np.all(used): return True
    blanks = board.arr[np.logical_not(board.taken)].tolist()
    kloc:Cell = min(blanks,key=lambda x: len(x.viables))
    if len(kloc.viables) == 0: return False
    root_viables:set[tuple[Pentomino,tuple[int,int]]] = set.copy(kloc.viables)
    for viable in root_viables:
        pent = viable[0]
        coord = viable[1]
        #place i there
        
        #get affected cells
        affected:set[tuple[Cell,tuple[Pentomino,tuple[int,int]]]] = set()

        #affected index
        k:Cell
        affected = affected.union(board.indexs[pent.typeIdx])
        submatrix = board.arr[coord[0]:coord[0]+pent.arrdef.shape[0], coord[1]:coord[1]+pent.arrdef.shape[1]]
        for k in submatrix[pent.arrdef != 0]:
            affected = affected.union(k.viables)
        recovery_list:list[tuple[Cell,tuple]] = []
        for key in affected:
            cell:Cell
            for cell in board.reflex[key]:
                if key in cell.viables:
                    cell.viables.remove(key)
                    recovery_list.append((cell, key))

        #remove the options

        #update taken
        board.taken[coord[0]:coord[0]+pent.arrdef.shape[0], coord[1]:coord[1]+pent.arrdef.shape[1]][pent.mask] = True 
        used[pent.typeIdx] = True
        place.append((pent.arrdef, coord))
        
        #recursive
        if _solve(board, used, place): return True
        #recover
        place.pop()
        used[pent.typeIdx] = False
        board.taken[coord[0]:coord[0]+pent.arrdef.shape[0], coord[1]:coord[1]+pent.arrdef.shape[1]][pent.mask] = False


        #recover the options

        for record in recovery_list:
            record[0].viables.add(record[1])

        
    return False


def _conv(pent:Pentomino, board:Board) -> None:
    row = board.arr.shape[0]-pent.arrdef.shape[0]+1
    col = board.arr.shape[1]-pent.arrdef.shape[1]+1
    if (row <= 0 or col <= 0): return
    mask = np.zeros(shape=board.arr.shape,dtype=bool)
    mask[0:pent.arrdef.shape[0], 0:pent.arrdef.shape[1]] = (pent.arrdef > 0)

    for i in range(row):
        for j in range(col):
            submatrix = board.taken[i:i+pent.arrdef.shape[0], j:j+pent.arrdef.shape[1]]
            if np.any(np.logical_and(submatrix,(pent.arrdef > 0))):
                continue
            else:
                viable = (pent,(i,j))
                board.indexs[pent.typeIdx].add(viable)
                pmask = np.roll(mask,i,axis=0)
                pmask = np.roll(pmask,j,axis=1)
                obj:Cell
                for obj in board.arr[pmask]:
                    obj.viables.add(viable)
                    board.add_reflex(viable,obj)


if __name__ == "__main__":

    k:list = solve(instances.board_3x20,instances.pentnominos)
    print(k)
    pass
