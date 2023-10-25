import gymnasium 
from gymnasium import spaces
import numpy as np
from Environments.gen_maze import create_maze

class maze_game(gymnasium.Env):

    def __init__(self):
        self.x = 1
        self.y = 0
        self.wall = 1
        self.cell = 0
        self.agent = 2
        self.goal = 3

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict({'maze': spaces.MultiBinary((16,16)), 'agent': spaces.MultiBinary((16,16)), 'goal': spaces.MultiBinary((16,16))})
        self.steps = 0
        self.reset()

    @property
    def cords_as_index(self):
        return self.x * self.maze.shape[0] + self.y
    
    @property
    def reward(self):
        if self.maze[self.x, self.y] == self.goal:
            return 50
        else:
            return -0.1

    @property 
    def done(self):
        return self.maze[self.x, self.y] == self.goal or self.steps >= 500

    def step(self, action):
        self.maze[self.x, self.y] = self.cell
        #Hanlde the action
        if action == 0:
            if self.y != 0:
                if self.maze[self.x, self.y-1] != self.wall:
                    self.y -= 1
        elif action == 1:
            if self.x != self.maze.shape[0]-1:
                if self.maze[self.x+1, self.y] != self.wall:
                    self.x += 1
        elif action == 2:
            if self.y != self.maze.shape[0]-1:
                if self.maze[self.x, self.y+1] != self.wall:
                    self.y += 1
        else:
            if self.x != 0:
                if self.maze[self.x-1, self.y] != self.wall:
                    self.x -= 1
        self.steps += 1
        if self.maze[self.x, self.y] != self.goal: self.maze[self.x, self.y] = self.agent
        return self.create_state(), self.reward, self.done, False, {}
    
    def reset(self, seed=0, options={}):
        self.x = 0
        self.y = 1
        self.steps = 0
        list_maze = create_maze()
        self.maze = np.zeros((12,12))
        for i in range(12):
            for k in range(12):
                self.maze[i,k] = list_maze[i][k] == 'X'
        self.maze[self.x, self.y] = self.agent
        self.maze[-1,10] = self.goal
        return self.create_state(), {}
    
    def create_state(self):
        state = {}
        state['maze'] = np.array(self.maze==self.wall, dtype=np.int8)
        state['agent'] = np.array(self.maze==self.agent, dtype=np.int8)
        state['goal'] = np.array(self.maze==self.goal, dtype=np.int8)
        return state
