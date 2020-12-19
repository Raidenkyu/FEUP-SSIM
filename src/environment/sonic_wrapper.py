import gym
import numpy as np

DOWN = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
LEFT = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
RIGHT = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
JUMP = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
JUMP_LEFT = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
JUMP_RIGHT = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
NOP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

actions = [DOWN, LEFT, RIGHT, JUMP, JUMP_LEFT, JUMP_RIGHT, NOP]


class SonicEnvWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super(SonicEnvWrapper, self).__init__(env)
        self._actions = actions
        self.action_space = gym.spaces.Discrete(len(self._actions))

    def action(self, a):
        return self._actions[a].copy()
