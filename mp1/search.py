# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

from collections import deque
from heapq import heappop,heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    queue = deque()
    parents = dict()
    curNode = maze.getStart()
    objectives = maze.getObjectives()
    queue.append(curNode)
    parents[curNode] = None
    while(queue.count != 0):
        curNode = queue.popleft()
        if curNode in objectives:
            break
        for node in maze.getNeighbors(curNode[0], curNode[1]):
            if node not in parents.keys():
                queue.append(node)
                parents[node] = curNode
    if (curNode not in objectives):
        return [], 0
    else:
        path = []
        while(curNode != None):
            path.append(curNode)
            curNode = parents[curNode]
        path.reverse()
        return path, len(parents.keys())

def dfs(maze):
    objectives = maze.getObjectives()
    unreachable = set()
    stack = deque()
    states = 1
    def _dfs(stack:deque) -> bool:
        nonlocal states
        if (stack[-1] in objectives):
            return True
        else:
            neighbors = maze.getNeighbors(stack[-1][0],stack[-1][1])
            if (neighbors.count == 0):
                    return False
            else:
                for neighbor in neighbors:
                    if (stack.__contains__(neighbor) or neighbor in unreachable): continue
                    stack.append(neighbor)
                    states += 1
                    rst = _dfs(stack)
                    if (not rst): 
                        stack.pop()
                    else:
                        return True
                unreachable.add(stack[-1])
                return False
    stack.append(maze.getStart())
    _dfs(stack)
    # TODO: Write your code here
    # return path, num_states_explored
    return list(stack), states 


def _prSearch(maze,costFun, objectives ):

    class comparableCord():
        def __init__(self, s:tuple) -> None:
            self.cord = s
        def __lt__(self, that) -> bool:
            costSelf = costFun(self.cord)
            costThat = costFun(that.cord)
            if costSelf < costThat: return True
            if (costSelf == costThat) and (self.cord[0] < that.cord[0]): return True
            if (costSelf == costThat) and (self.cord[0] == that.cord[0])and (self[1].cord < that[1].cord): return True
            return False  
    class priorQueue:
        def __init__(self) -> None:
            self.queue = []
            pass
        def pop(self)->tuple:
            return heappop(self.queue).cord
        
        def push(self,cord:tuple) -> None:
            heappush(self.queue,comparableCord(cord))
            return
        def min(self) -> tuple:
            return self.queue[0].cord
        def isEmpty(self) -> bool:
            return (self.queue.__len__() == 0)

   
    queue = priorQueue()
    parents = dict()
    curNode = maze.getStart()
    queue.push(curNode)
    parents[curNode] = None
    while(not queue.isEmpty()):
        curNode = queue.pop()
        if curNode in objectives:
            break
        for node in maze.getNeighbors(curNode[0], curNode[1]):
            if node not in parents.keys():
                queue.push(node)
                parents[node] = curNode
    if (curNode not in objectives):
        return [], 0
    else:
        path = []
        while(curNode != None):
            path.append(curNode)
            curNode = parents[curNode]
        path.reverse()
        return path, len(parents.keys())
    # TODO: Write your code here
    # return path, num_states_explored

def greedy(maze):
    objectives = maze.getObjectives()
    target = objectives[-1]
    def heurf(point):
        return abs(target[0]-point[0]) + abs(target[1]-point[1])
    return _prSearch(maze,heurf,objectives)


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0