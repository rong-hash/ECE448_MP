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
    end_node = maze.getObjectives()
    queue.append(curNode)
    parents[curNode] = None
    while(queue.count != 0):
        curNode = queue.popleft()
        if curNode in end_node:
            break
        for node in maze.getNeighbors(curNode[0], curNode[1]):
            if node not in parents.keys():
                queue.append(node)
                parents[node] = curNode
    if (curNode not in end_node):
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
    return [], 0


# def dfs(maze):
#     # BFS思想 = 队列维护
#     # DFS思想 = 栈维护
#     # [B站讲解] https://www.bilibili.com/video/BV1Ks411579J/?spm_id_from=333.337.search-card.all.click&vd_source=4c878cdda4a827e2590557bcbb57b3e5

#     # 初始化 -------------------------------------------------------------
#     cur_node      = maze.getStart()        # 获取 初始位置
#     end_node_list = maze.getObjectives()   # 获取 终点位置 列表

#     print(end_node_list)

#     path = []                         # 初始化栈   
#     parents = dict()                  # 初始化父节点 

#     path.append(cur_node)             # 将初始位置加入栈
#     parents[cur_node] = None          # 初始位置没有父节点

#     # 搜索算法 -----------------------------------------------------------
#     while(path.count != 0):           # 当栈不为空时,从栈顶 取出一个节点 (弹栈) 
#         cur_node = path.pop()        

#         # 如果是当前位置是终点，从终点列表中删除
#         # 如果终点列表为空，结束搜索
#         if cur_node in end_node_list:      
#             end_node_list.remove(cur_node) 
#             print(end_node_list)

#             if len(end_node_list) == 0:  
#                 end_node_list = maze.getObjectives()  # 主要给最后判断服务
#                 break

#         # 遍历现节点的子节点
#         #   若sub_node没探索过 (不在 parents.key 中)
#         #   将sub_node加入栈顶
#         #   将sub_node的父节点设置为cur_node
#         for sub_node in maze.getNeighbors(cur_node[0], cur_node[1]): 
#             if sub_node not in parents.keys(): 
#                 path.append(sub_node)          
#                 parents[sub_node] = cur_node   

#     # 返还程序 -----------------------------------------------------------
#     if (cur_node not in end_node_list):
#         return [], 0
#     else:
#         path = []
#         while(cur_node != None):
#             path.append(cur_node)
#             cur_node = parents[cur_node]
#         path.reverse()
#         return path, len(parents.keys()) # 返回路径path和探索节点数量

#     return [], 0

def dfs(maze):
    start_node = maze.getStart()          # 获取初始位置
    end_node_list = maze.getObjectives()  # 获取终点位置列表
    visited_end_nodes = set()             # 已访问的终点集合
    total_path = []                       # 最终路径
    total_visited = set()                 # 所有访问过的节点集合

    # 从当前节点到下一个目标节点的DFS搜索
    def dfs_to_next(cur_node, end_node):
        path = []  # 初始化栈
        parents = dict()  # 初始化父节点

        path.append(cur_node)  # 将当前节点加入栈
        parents[cur_node] = None  # 当前节点没有父节点

        while path:
            cur_node = path.pop()

            if cur_node == end_node:  # 找到目标节点
                break

            # 遍历当前节点的子节点
            for sub_node in maze.getNeighbors(cur_node[0], cur_node[1]):
                if sub_node not in parents.keys():  # 若sub_node没探索过
                    path.append(sub_node)  # 将sub_node加入栈顶
                    parents[sub_node] = cur_node  # 设置父节点

        # 回溯以构建路径
        cur_path = []
        while cur_node:
            cur_path.append(cur_node)
            cur_node = parents[cur_node]
        cur_path.reverse()

        return cur_path

    cur_node = start_node

    # 若不是所有 end_node 都访问过，则继续循环
    while len(visited_end_nodes) < len(end_node_list):
        nearest_end_node = None
        nearest_path     = None

        # 寻找最近的未访问目标点
        for end_node in end_node_list:
            if end_node not in visited_end_nodes:
                path = dfs_to_next(cur_node, end_node)
                
                if nearest_end_node is None or len(path) < len(nearest_path):
                    nearest_end_node = end_node
                    nearest_path = path

        # 更新总路径和访问过的节点
        if nearest_path:
            total_path.extend(nearest_path[1:])     # 排除起点重复
            visited_end_nodes.add(nearest_end_node)
            total_visited.update(nearest_path)
            cur_node = nearest_end_node

    return total_path, len(total_visited)



def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0







# 定义 Node 类
class Node:
    def __init__(self, parent=None, position=None): # Node 包含 parent,position,g,h,f
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    # def __eq__(self, other): # 判断两个节点位置是否相同
    #     return self.position == other.position
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.position == other.position


# 注意下边的 node 代表节点结构体，节点位置为 node.position
def astar(maze):
    # 初始化 ---------------------------------------------------`----------
    open_list  = []
    close_list = []

    start_pos = maze.getStart()           # 获取 起点
    end_pos   = maze.getObjectives()[0]   # 获取 终点  # 先测试走一个终点的

    start_node = Node(None, start_pos)    # 起点 结构体 f()=g()=h()=0
    end_node   = Node(None, end_pos)      # 终点 结构体

    open_list.append(start_node)          # 将起点加入 open list

    # 测试接口
    print('-----------------')
    print('start_pos           =' + str(start_pos))
    print('start_node.position =' + str(start_node.position))
    print('end_pos             =' + str(end_pos))
    print('end_node.position   =' + str(end_node.position))
    print(start_node.parent)

    count = 1
    # 搜索算法 -------------------------------------------------------------
    while(open_list):

        # 从 open_list 中选取优先级最高的节点 作为cur_node探索
        # 将探索过的 cur_node 添加到 close_list 中
        open_list.sort(key=lambda x: x.f) 
        cur_node = open_list.pop(0)
        close_list.append(cur_node)

        # 如果现节点是终点 终止递归, 注意 终点可能有几个 ？
        if cur_node.position == end_node.position:    
            break
        
        children = []

        # 遍历 cur_node 的子节点，将坐标与父节点打包成 Node 数据类型
        for sub_node_position in maze.getNeighbors(cur_node.position[0], cur_node.position[1]): 
            
            sub_node = Node(cur_node, sub_node_position) 
            sub_node.g = cur_node.g + 1
            sub_node.h = abs(sub_node.position[0] - end_node.position[0]) + abs(sub_node.position[1] - end_node.position[1]) # 启发式函数 h(n) 这里采用曼哈顿距离
            sub_node.f = sub_node.g + sub_node.h

            if sub_node in close_list: 
                continue

            # 判断 sub_node 位置是否与 open_list 中的某些未探索节点相同 + 比较 sub_node 与 open list 中的这个节点的 g(n)
            # 如果 位置相同 + g(n)更小 → 添加到 open_list中
            if any([open_node for open_node in open_list if sub_node == open_node and sub_node.g > open_node.g]): 
                continue

            open_list.append(sub_node)        
        
    # 返还程序 -----------------------------------------------------------
    if (cur_node != end_node): # if (cur_node not in end_node): 原始代码
        return [], 0
    else:
        path = []
        while(cur_node.parent != None):
            path.append(cur_node.position)
            cur_node = cur_node.parent   # 链表
        path.reverse()

        return path, len(close_list)     # 测试
        # return path, len(parents.keys()) # 返回路径path和探索节点数量
    return [], 0