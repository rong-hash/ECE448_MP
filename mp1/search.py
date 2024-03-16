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
    
class searchNode():
    def __init__(self, s:tuple, costFun, remain:tuple,  parent = None) -> None:
        self.cord = s
        self.parent = parent
        self.remain = remain
        if (parent != None):
            self.dist = parent.dist + 1
        else:
            self.dist = 0
        self.cost = costFun(self)
    def __lt__(self, that) -> bool:
        if self.cost < that.cost: return True
        if (self.cost == that.cost) and (self.__hash__())<hash(that.__hash__()): return True #Break Tie
        return False
    def __hash__(self) -> int:
        return hash(self.cord)^hash(self.remain)
    def __eq__(self, that) -> bool:
        if (that == None): return False
        return (self.cord == that.cord and self.remain == that.remain)
    
class priorQueue:
    def __init__(self) -> None:
        self.queue = []
        self.itemset = set()
        return

    def pop(self)->searchNode:
        obj = heappop(self.queue)
        self.itemset.remove(obj)
        return obj
    
    def push(self,cord:searchNode) -> None:
        heappush(self.queue, cord)
        self.itemset.add(cord)
        return
    
    def min(self):
        return self.queue[0]
    
    def isEmpty(self) -> bool:
        return (self.queue.__len__() == 0)
    
    def contain(self,node:searchNode) -> bool:
        return self.itemset.__contains__(node)
        

def _prSearchMulti(maze,costFun, objectives):   
    queue = priorQueue()
    explored = dict() #Serch Node -> Cost

    remainSet = tuple(objectives)
    curNode = searchNode(maze.getStart(),costFun, remainSet)

    queue.push(curNode)
    explored[curNode] = curNode.cost
    while(not queue.isEmpty()):
        curNode = queue.pop()
        remainSet = set(curNode.remain)
        if curNode.cord in remainSet:
            remainSet.remove(curNode.cord)
            if (len(remainSet) == 0):
                break
        for node in maze.getNeighbors(curNode.cord[0], curNode.cord[1]):
            nextNode = searchNode(node, costFun, tuple(remainSet), curNode)
            if (nextNode not in explored.keys()):
                if (not queue.contain(nextNode)): queue.push(nextNode)
            else:
                if(nextNode.cost < explored[nextNode]):
                    explored.__delitem__(nextNode)
                    queue.push(nextNode)
                    pass
        explored[curNode] = curNode.cost
    if (len(remainSet) != 0):
        return [], 0
    else:
        path = []
        while(curNode != None):
            path.append(curNode.cord)
            curNode = curNode.parent
        path.reverse()
        return path, len(explored)

def greedy(maze):
    objectives = maze.getObjectives()
    target = objectives[-1]
    def cost(point):
        return abs(target[0]-point.cord[0]) + abs(target[1]-point.cord[1])
    return _prSearchMulti(maze,cost,objectives)


def astar(maze):
    objectives = maze.getObjectives()
    target = objectives[-1]
    def cost(point):
        return abs(target[0]-point.cord[0]) + abs(target[1]-point.cord[1]) + point.dist
    
    def unicost(point):
        return point.dist
        #return point.dist
    return _prSearchMulti(maze,unicost,objectives)
    # TODO: Write your code here
    # return path, num_states_explored