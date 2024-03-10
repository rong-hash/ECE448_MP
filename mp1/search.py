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

    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def dfs(maze):
    # BFS思想 = 队列维护
    # DFS思想 = 栈维护
    # [B站讲解] https://www.bilibili.com/video/BV1Ks411579J/?spm_id_from=333.337.search-card.all.click&vd_source=4c878cdda4a827e2590557bcbb57b3e5

    # 初始化 -------------------------------------------------------------
    cur_node = maze.getStart()        # 获取 初始位置
    objectives = maze.getObjectives() # 获取 终点位置

    stack = []                        # 初始化栈      [使用数组]
    parents = dict()                  # 初始化父节点  {使用字典}

    stack.append(cur_node)            # 将初始位置加入栈
    parents[cur_node] = None          # 初始位置没有父节点

    # 搜索算法 -----------------------------------------------------------
    while(stack.count != 0):          # 当栈不为空时,从栈顶 取出一个节点 (弹栈) 
        cur_node = stack.pop()        

        if cur_node in objectives:    # 如果现节点是终点 终止递归
            break
        
        for sub_node in maze.getNeighbors(cur_node[0], cur_node[1]): # 遍历现节点的子节点，cur_node[0]是行，cur_node[1]是列
            if sub_node not in parents.keys(): # 如果子节点不在父节点中
                stack.append(sub_node)         # 将子节点加入栈顶
                parents[sub_node] = cur_node   # 将子节点的父节点设置为现节点 在parent中创建名为node的key，其值为 cur_node

                # cur_node  现节点
                #    ↓
                # sub_node  子节点

    # 返还程序 -----------------------------------------------------------
    if (cur_node not in objectives):
        return [], 0
    else:
        path = []
        while(cur_node != None):
            path.append(cur_node)
            cur_node = parents[cur_node]
        path.reverse()
        return path, len(parents.keys()) # 返回路径path和探索节点数量

    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0