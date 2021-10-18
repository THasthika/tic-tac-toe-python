import random
from typing import Union

from agent import Agent

class RandomAgent(Agent):

    def __init__(self, player) -> None:
        self.player = player

    def getNextMove(self, state) -> Union[int, int]:
        ri = random.randint(1, 3)
        rj = random.randint(1, 3)
        while state[ri-1][rj-1] != "-":
            ri = random.randint(1, 3)
            rj = random.randint(1, 3)
        return (ri, rj)

class MinMaxAgent(Agent):

    def __init__(self, player) -> None:
        self.player = player

    def getNextMove(self, state) -> Union[int, int]:
        # construct min max tree

        # evaluate move score
        return (0, 0)

## how to construct a min max tree

# +1 for every symbol of the player
# -5 if not the symbol of player or empty
# 0 if empty
# calculate each horizontal, vertical and diagonal and return the max