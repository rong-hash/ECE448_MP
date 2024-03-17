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
This is the main entry Node for MP1. You should only modify code
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
    
def L1Dist(cordA,cordB):
    return abs(cordA[0]-cordB[0]) + abs(cordA[1]-cordB[1])
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
    
class edge():
    def __init__(self, cordA, cordB) -> None:
        self.dist = L1Dist(cordA,cordB)
        self.ends = {cordA, cordB}
        pass
    def other(self, cord):
        if cord == self.ends[0]: return self.ends[1]
        if (cord == self.ends[1]): return self.ends[0]
        raise Exception("Not from the edge!")
        return
    def __lt__(self, that) -> bool:
        if self.dist < that.dist: return True
        return False
    
class priorQueue:
    def __init__(self) -> None:
        self.queue = []
        self.itemset = set()
        return

    def pop(self):
        obj = heappop(self.queue)
        self.itemset.remove(obj)
        return obj
    
    def push(self,cord) -> None:
        heappush(self.queue, cord)
        self.itemset.add(cord)
        return
    
    def min(self):
        return self.queue[0]
    
    def isEmpty(self) -> bool:
        return (self.queue.__len__() == 0)
    
    def contain(self,node) -> bool:
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

    dists = dict()
    for i in range(len(objectives)):
        tpdict = dict()
        for j in range(len(objectives)):
            if i == j: continue
            tpdict = L1Dist(objectives[i],objectives[j])
        dists[objectives[i]] = tpdict
    
    def l1cost(point): #Manhatton Distance as Heuristic Function
        return L1Dist(objectives[-1],point.cord) + point.dist
    
    def unicost(point):
        return point.dist
        #return point.dist
    
    def mstcost(point): #MST Heuristic for MultiDot Search
        queue = priorQueue()
        toconnect = set(point.remain)
        val = 0
        for i in point.remain:
            queue.push(edge(point.cord,i))
        while (len(toconnect) != 0):
            stedge = queue.pop()
            expnodes = toconnect.intersection(stedge.ends)
            if len(expnodes) == 0: continue
            for j in expnodes: othernode = j
            #Connect
            toconnect.remove(othernode)
            val += stedge.dist
            for j in toconnect:
                queue.push(edge(othernode,j))
        return val+point.dist
    return _prSearchMulti(maze,mstcost,objectives) #Select Cost Function here
    # TODO: Write your code here
    # return path, num_states_explored




# For bigDots.txt nonoptimal A* search:

# 自定义返回 end_mode_list 中 h 最小的 end_node
def min_h_end_node(cur_node, end_node_list):
    h = []
    for end_node in end_node_list:
        h.append(abs(end_node[0] - cur_node[0]) + abs(end_node[1] - cur_node[1])) # 曼哈顿距离

    min_h_end_node = end_node_list[h.index(min(h))]

    return min_h_end_node

# 自定义返回 exploring_list 中 h 最小的 node
# 并将该 node 从open_node_list中删除
def min_h_open_node(exploring_list, end_node, exploring_g):
    f_list = []
    for node in exploring_list:
        h = abs(node[0] - end_node[0]) + abs(node[1] - end_node[1])
        f = h + exploring_g[node]
        f_list.append(f)
    min_index = f_list.index(min(f_list))

    return exploring_list.pop(min_index)

# 自定义路径生成函数
def build_path(cur_node, exploring_parent):
    path = [cur_node]

    # 若 Path 队尾节点父级不是 None → 继续构建
    while exploring_parent[path[-1]] != None:
        path.append(exploring_parent[path[-1]])
    path.reverse()
    return path

# 自定义A*搜索算法
# 算法思路：
#   每次选取 h 最小的 end_node
#   生成到该 end_node 的最短路径
#   重复步骤 + 拼接路径
def astar_nonoptimal(maze):

    num_states_explored = 0
    total_path = []

    start_node    = maze.getStart()
    end_node_list = maze.getObjectives()

    # 找出距离最小的 作为end_node
    end_node      = min_h_end_node(start_node, end_node_list)

    exploring_list    = [start_node]       #存放 待探索坐标
    exploring_parent  = {start_node:None}  #存放 待探索坐标父节点    
    exploring_g       = {start_node:0}     #存放 待探索坐标g值
    explored_list     = []                 #存放 已探索坐标

    while exploring_list:

        # 取出 exploring_list 中 f 值最小的节点探索
        # 这里包含回溯，如果走进死胡同没有继续的子节点，就会从上一个岔路拿出节点
        cur_node = min_h_open_node(exploring_list, end_node, exploring_g) # 第一次循环取出 cur_node = start_node
        explored_list.append(cur_node)  #测试#
        num_states_explored += 1

        # 若找到 end_node，将其从end_node_list 中删除 + 构建 Path
        # 这个 end_node 不一定是前面那个 h 最小的
        if cur_node in end_node_list:
            end_node_list.remove(cur_node)
            
            # 链表构建Path，这里的cur_node其实已经是一个 end_node了
            # 去掉起点 添加折返路径
            total_path = total_path[:-1] + build_path(cur_node,exploring_parent) 

            # 若所有 end_node 经过，程序结束
            if len(end_node_list) == 0:
                # print("Overall path: ", total_path)
                return total_path, num_states_explored
            
            # 找到一个 end_node 就重置 open_node_list，将 cur_node 作为新的起点
            end_node   = min_h_end_node(cur_node, end_node_list)

            exploring_list    = [cur_node]
            exploring_parent  = {cur_node:None}
            exploring_g       = {cur_node:0}
            explored_list     = []

        # 遍历 sub_node_list
        sub_node_list = maze.getNeighbors(cur_node[0], cur_node[1])
        for sub_node in sub_node_list:

            # 若sub_node没探索过，将其加入 exploring_list   
            if sub_node not in explored_list: 
                for node in exploring_list:
                    if sub_node == node and exploring_g[sub_node] < exploring_g[node]:
                        exploring_list.append(sub_node)
                        exploring_parent[sub_node] = cur_node
                        exploring_g[sub_node] = exploring_g[cur_node] + 1
                        break
            if sub_node not in exploring_list and sub_node not in explored_list:   
                exploring_parent[sub_node]   = cur_node
                exploring_g[sub_node]        = exploring_g[cur_node] + 1
                exploring_list.append(sub_node)

    return [], 0
