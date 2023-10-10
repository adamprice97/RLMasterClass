import gymnasium 
from gymnasium import spaces
import numpy as np

class maze_game(gymnasium.Env):

    def __init__(self, difficulty):
        self.x = 0
        self.y = 0
        if difficulty == 'very hard':
            self.maze = np.array([[' ', 'X', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' '],
                                  [' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
                                  [' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' '],
                                  [' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                  [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' '],
                                  [' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
                                  [' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', 'X', 'X'],
                                  ['X', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' '],
                                  [' ', 'X', ' ', 'X', 'X', 'X', ' ', ' ', 'X ', ' '],
                                  [' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', 'X ', 'G']])
        elif difficulty == 'hard':
            self.maze = np.array([[' ', 'X', ' ', ' ', ' ', 'X', 'X'],
                                [' ', 'X', ' ', 'X', ' ', ' ', ' '],
                                [' ', ' ', ' ', 'X', 'X', 'X', ' '],
                                [' ', 'X', ' ', ' ', ' ', ' ', ' '],
                                [' ', 'X', ' ', 'X', ' ', 'X', ' '],
                                [' ', 'X', ' ', 'X', 'X', 'X', ' '],
                                [' ', ' ', ' ', ' ', ' ', 'X', 'G']])
        else:
            self.maze = np.array([[' ', 'X', ' ', ' ', ' '],
                                [' ', 'X', ' ', 'X', ' '],
                                [' ', ' ', ' ', 'X', 'X'],
                                [' ', 'X', ' ', ' ', ' '],
                                [' ', 'X', ' ', 'X', 'G']])
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(self.maze.shape[0]**2)
        self.steps = 0

    @property
    def cords_as_index(self):
        return self.x * self.maze.shape[0] + self.y
    
    @property
    def reward(self):
        if self.maze[self.x, self.y] == 'G':
            return 10
        else:
            return -0.1

    @property 
    def done(self):
        return self.maze[self.x, self.y] == 'G' or self.steps > 200

    def step(self, action):
        self.maze[self.x, self.y] = ' '
        #Hanlde the action
        if action == 0:
            if self.y != 0:
                if self.maze[self.x, self.y-1] != 'X':
                    self.y -= 1
        elif action == 1:
            if self.x != self.maze.shape[0]-1:
                if self.maze[self.x+1, self.y] != 'X':
                    self.x += 1
        elif action == 2:
            if self.y != self.maze.shape[0]-1:
                if self.maze[self.x, self.y+1] != 'X':
                    self.y += 1
        else:
            if self.x != 0:
                if self.maze[self.x-1, self.y] != 'X':
                    self.x -= 1
        self.steps += 1
        if self.maze[self.x, self.y] != 'G': self.maze[self.x, self.y] = 'A'
        return {'state': self.cords_as_index}, self.reward, self.done, False, {}
    
    def reset(self):
        self.x = 0
        self.y = 0
        self.steps = 0
        self.maze[self.x, self.y] = 'A'
        return {'state': self.cords_as_index}