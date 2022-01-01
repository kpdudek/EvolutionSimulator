#!/usr/bin/env python3

from lib.PriorityQueue import PriorityQueue
from lib.Logger import Logger
import time, math
import numpy as np

class AStar(object):
    def __init__(self,map,debug_mode=False):
        self.debug_mode = debug_mode
        self.map = map
        self.queue = PriorityQueue()
        self.logger = Logger()
    
    def reset(self,map):
        self.map = map
        self.queue = PriorityQueue()

    def get_plan(self,start_idx,goal_idx):
        '''
            Returns a 2xn array of coordinates
        '''
        idx_closed = []
        self.queue.insert(start_idx,0)
        self.map.tiles[start_idx].backpointer_cost = 0

        self.logger.log(f"Plan requested from node: [{start_idx}] to [{goal_idx}]")
        sx,sy = self.map.tiles[start_idx].pose
        gx,gy = self.map.tiles[goal_idx].pose
        self.logger.log(f"\tCoordinates are: ({sx},{sy}) ({gx},{gy})")

        tic = time.time()
        iter_count = 0
        history = []
        while not self.queue.is_empty():
            iter_count += 1
            idx_next,cost = self.queue.min_extract()
            history.append(idx_next)
            idx_closed.append(idx_next)

            if idx_next == goal_idx:
                toc = time.time()
                self.logger.log(f'Path found in {toc-tic} seconds!')
                break
            
            neighbors = self.expand_list(idx_next,idx_closed)
            for idx_neighbor in range(0,len(neighbors)):
                self.expand_node(idx_next,goal_idx,neighbors[idx_neighbor])
            
            if self.debug_mode:
                self.logger.log(f'Iteration {iter_count}:')
                self.logger.log(f'\tExpanding node: {idx_next}')
                self.logger.log(f'\tNeighbors: {neighbors}')
        
        path = self.get_path(start_idx,goal_idx)

        return path, history

    def expand_list(self,idx_next,idx_closed):
        neighbors = []
        neighbors = self.map.tiles[idx_next].neighbors.copy()
        for idx in idx_closed:
            if idx in neighbors:
                neighbors.remove(idx)
        if idx_next in neighbors:
            neighbors.remove(idx_next)

        return neighbors
    
    def expand_node(self,idx_next,goal_idx,neighbor):
        backpointer_cost = self.map.tiles[idx_next].backpointer_cost
        heuristic = self.graph_heuristic(neighbor,goal_idx)
        idx_cost = self.map.tiles[idx_next].neighbors.index(neighbor)
        step_cost = self.map.tiles[idx_next].backpointer_cost + self.map.tiles[idx_next].neighbors_cost[idx_cost]

        if self.queue.is_member(neighbor):
            if self.debug_mode:
                self.logger.log(f'\tNeighbor {neighbor}: is already in the queue')
            if step_cost < self.map.tiles[neighbor].backpointer_cost:
                self.map.tiles[neighbor].backpointer_cost = step_cost
                self.map.tiles[neighbor].backpointer = idx_next
                if self.debug_mode:
                    self.logger.log(f'\tNeighbor {neighbor}: was reassigned a lower backpointer')
        else:
            self.map.tiles[neighbor].backpointer_cost = step_cost
            self.map.tiles[neighbor].backpointer = idx_next
            self.queue.insert(neighbor, step_cost+heuristic)

    def graph_heuristic(self,idx_start,idx_end):
        start = self.map.tiles[idx_start].pose
        end = self.map.tiles[idx_end].pose

        return math.pow((math.pow(start[0]-end[0],2) + math.pow(start[1]-end[1],2)),.5)

    def get_path(self,start_idx,goal_idx):
        path = self.map.tiles[goal_idx].pose.reshape(2,1)
        if start_idx==goal_idx:
            return path

        idx_current = self.map.tiles[goal_idx].backpointer
        if idx_current == None:
            self.logger.log("No path found!")
            return None

        while idx_current != start_idx:
            path = np.append(path,self.map.tiles[idx_current].pose.reshape(2,1),axis=1)
            idx_current = self.map.tiles[idx_current].backpointer
        path = np.append(path,self.map.tiles[start_idx].pose.reshape(2,1),axis=1)

        path = np.fliplr(path)
        return path