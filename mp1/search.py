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

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
        "extra":test,
        "extra2":test2
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









# LZP 的魔改 A*

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
def test2(maze):

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

            # 若sub_node没探索过，将其加入 exploring_list   # 这里存在逻辑错误???????????????????????????????????????????
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




# 我自己的 A* 算法
class Node:
    def __init__(self, parent=None, position=None, end_node_list = []):
        self.parent   = parent
        self.position = position
        self.g = 0  # 从起点到当前节点的成本
        self.h = 0  # 从当前节点到终点的启发式成本
        self.f = 0  # 总成本
        self.target = end_node_list # 终点列表

    def load(self,cur_node,heristic_func):
        self.h = heristic_func(self)
        self.g = cur_node.g + 1
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.position == other.position

def heristic_func(node):
    end_node_list = node.target
    return min([abs(node.position[0] - end.position[0]) + abs(node.position[1] - end.position[1]) for end in end_node_list])
    #return 0

def reconstruct_path(cur_node):
    path = []
    while cur_node is not None:
        path.append(cur_node.position)
        cur_node = cur_node.parent
    path.reverse()  # 将路径反转，从起点开始
    return path

def single_astar_search(start_node, end_node_list, maze):
    exploring_list = [start_node]  # 待探索的节点
    explored_list  = []            # 已探索的节点

    while exploring_list:
        
        # 优先级排序
        exploring_list.sort(key=lambda x: x.f)
        cur_node = exploring_list.pop(0)

        # 检查是否到达了 end_node_list 中的任何一个节点
        for end_node in end_node_list:
            if cur_node == end_node:
                return reconstruct_path(cur_node), len(explored_list)

        explored_list.append(cur_node)

        # 遍历子节点
        for sub_node_position in maze.getNeighbors(cur_node.position[0], cur_node.position[1]):
            
            # 打包 sub_node 数据类型
            sub_node = Node(cur_node, sub_node_position,end_node_list)
            sub_node.load(cur_node,heristic_func)

            # A* 核心逻辑

            # 若子节点 已探索 → 跳过
            if sub_node in explored_list:
                continue
            
            # 若子节点 未探索
            # 若子节点 不在待探索列表 → 添加
            # 若子节点 在待探索列表 → 比较 g
            if sub_node not in exploring_list:
                if sub_node not in exploring_list:
                    exploring_list.append(sub_node)
                if sub_node in exploring_list:
                    for node in exploring_list:
                        if node.position == sub_node.position and node.g > sub_node.g:
                            node.g = sub_node.g
                            node.parent = sub_node.parent
                            continue

    return []

def test(maze):
    start_pos = maze.getStart()
    end_pos_list = maze.getObjectives()

    total_path = []
    total_explored_nodes = 0

    start_node    = Node(None, start_pos)
    end_node_list = [Node(None, pos) for pos in end_pos_list]

    while end_node_list:
        path, explored_nodes = single_astar_search(start_node, end_node_list, maze)
        if path:
            total_path.extend(path[1:])        # 避免重复添加起始节点
            total_explored_nodes += explored_nodes
            start_node = Node(None, path[-1])  # 更新起始点为最近找到的终点
            end_node_list.remove(start_node)   # 从目标列表中移除已达到的目标

    return total_path, total_explored_nodes













from collections import deque
from heapq import heappop,heappush

class Node_t():
    def __init__(self, s:tuple, costFunc, remain:tuple,  parent = None) -> None:
        self.cord = s
        self.parent = parent
        self.remain = remain
        if (parent != None):
            self.dist = parent.dist + 1
        else:
            self.dist = 0
        self.cost = costFunc(self)
    
    # less than
    def __lt__(self, that) -> bool:
        if self.cost < that.cost: return True
        if (self.cost == that.cost) and (self.__hash__())<hash(that.__hash__()): return True #Break Tie
        return False
    
    def __hash__(self) -> int:
        return hash(self.cord)^hash(self.remain)
    
    # ==
    def __eq__(self, that) -> bool:
        if (that == None): return False
        return (self.cord == that.cord and self.remain == that.remain)


class priorQueue:
    def __init__(self) -> None:
        self.queue = []
        self.itemset = set()
        return

    def pop(self)->Node_t:
        obj = heappop(self.queue)
        self.itemset.remove(obj)
        return obj
    
    def push(self,cord:Node_t) -> None:
        heappush(self.queue, cord)
        self.itemset.add(cord)
        return
    
    def min(self):
        return self.queue[0]
    
    def isEmpty(self) -> bool:
        return (self.queue.__len__() == 0)
    
    def ifcontain(self,Node_t:Node_t) -> bool:
        return self.itemset.__contains__(Node_t)
        

def _prSearchMulti(maze,costFunc, objectives):   
    
    # 初始化优先级队列
    queue = priorQueue()
    explored = dict() #Serch Node_t -> Cost

    remainSet = tuple(objectives)
    cur_Node = Node_t(maze.getStart(),costFunc, remainSet)

    # 加入curNode
    queue.push(cur_Node)                 # 未探索 队列
    explored[cur_Node] = cur_Node.cost   # 已探索 存放已探索节点的g
    while(not queue.isEmpty()):

        cur_Node = queue.pop()
        remainSet = set(cur_Node.remain)

        # 找到一个终点
        if cur_Node.cord in remainSet:
            remainSet.remove(cur_Node.cord)

            # 找到所有终点
            if (len(remainSet) == 0):
                break

        # 遍历子节点
        for sub_node_cord in maze.getNeighbors(cur_Node.cord[0], cur_Node.cord[1]):
            sub_Node = Node_t(sub_node_cord, costFunc, tuple(remainSet), cur_Node) # 打包数据类型

            # 若sub_Node 没探索过 + 不在探索队列中 → 添加到队列
            if (sub_Node not in explored.keys()):
                if (not queue.ifcontain(sub_Node)): queue.push(sub_Node)
            
            # 若sub_Node 探索过 + g更小 → 更新g
            else:
                if(sub_Node.cost < explored[sub_Node]):
                    explored.__delitem__(sub_Node)
                    queue.push(sub_Node)
                    pass
        explored[cur_Node] = cur_Node.cost
    

    # 重构路径
    if (len(remainSet) != 0):
        return [], 0
    else:
        path = []
        while(cur_Node != None):
            path.append(cur_Node.cord)
            cur_Node = cur_Node.parent
        path.reverse()
        return path, len(explored)


def astar_search(maze):
    objectives = maze.getObjectives()
    target = objectives[-1] # 最后一个目标点

    # f = h + g 不一定找到最短
    # Path = 171
    # explored = 861171
    def single_cost(Node):
        return abs(target[0]-Node.cord[0]) + abs(target[1]-Node.cord[1]) + Node.dist
    
    # f = h + g 不一定找到最短
    # Path = 169
    # explored = 1026385
    def min_h_cost(Node):
        return min([abs(Node.cord[0] - end[0]) + abs(Node.cord[1] - end[1]) for end in objectives]) + Node.dist
    
    # f = 0 + g 均匀搜索
    # Path = 169
    # explored = 1088829
    def uniform_cost(Node):
        return Node.dist
    
    # return _prSearchMulti(maze,single_cost,objectives)
    return _prSearchMulti(maze,single_cost,objectives)

    # TODO: Write your code here
    # return path, num_states_explored


def astar(maze):



    return astar_search(maze)








