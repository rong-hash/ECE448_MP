import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        self.reset()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        # Discretize the state

        adjoining_wall_x = 0
        if state[0] == utils.GRID_SIZE:
            adjoining_wall_x = 1
        elif state[0] == utils.DISPLAY_SIZE-2*utils.GRID_SIZE:
            adjoining_wall_x = 2

        adjoining_wall_y = 0
        if state[1] == utils.GRID_SIZE:
            adjoining_wall_y = 1
        elif state[1] == utils.DISPLAY_SIZE-2*utils.GRID_SIZE:
            adjoining_wall_y = 2

        food_dir_x = 0
        if state[0] > state[3]:
            food_dir_x = 1
        elif state[0] < state[3]:
            food_dir_x = 2

        food_dir_y = 0
        if state[1] > state[4]:
            food_dir_y = 1
        elif state[1] < state[4]:
            food_dir_y = 2

        adjoining_body_top = 0
        if (state[0], state[1]-utils.GRID_SIZE) in state[2]:
            adjoining_body_top = 1
        
        adjoining_body_botton = 0
        if (state[0], state[1]+utils.GRID_SIZE) in state[2]:
            adjoining_body_botton = 1
        
        adjoining_body_left = 0
        if (state[0]-utils.GRID_SIZE, state[1]) in state[2]:
            adjoining_body_left = 1
        
        adjoining_body_right = 0
        if (state[0]+utils.GRID_SIZE, state[1]) in state[2]:
            adjoining_body_right = 1
        
        tindex = (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_botton, adjoining_body_left, adjoining_body_right)
        if self.s != None and self.a != None:
            # Update Q table
            if self._train:
                pindex = (self.s[0], self.s[1], self.s[2], self.s[3], self.s[4], self.s[5], self.s[6], self.s[7], self.a)
                reward = -0.1
                if (points > self.points): reward = 1
                elif dead: reward = -1
                self.Q[pindex] += self.C/(self.C + self.N[pindex]) * (reward + self.gamma * np.max(self.Q[tindex]) - self.Q[pindex])
            if dead:
                self.reset()
                return
        
        self.s = tindex
        maxq = -np.inf
        maxqarg = 0
        if self._train:
            for act in range(3, -1, -1):
                refidx = (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_botton, adjoining_body_left, adjoining_body_right,self.actions[act])
                if self.N[refidx] < self.Ne:
                    if maxq < 1: 
                        maxq = 1
                        maxqarg = act
                else:
                    if maxq < self.Q[refidx]:
                        maxq = self.Q[refidx]
                        maxqarg = act
            self.a = self.actions[maxqarg]
            refidx = (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_botton, adjoining_body_left, adjoining_body_right,self.a)
            self.N[refidx] += 1
            self.points = points
        else:
            for act in range(3, -1, -1):
                refidx = (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_botton, adjoining_body_left, adjoining_body_right,self.actions[act])
                if maxq < self.Q[refidx]:
                    maxq = self.Q[refidx]
                    maxqarg = act
            return self.actions[maxqarg]
        return self.a
