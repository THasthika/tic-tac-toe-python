
from typing import Union
from agent import Agent


class HumanAgent(Agent):

    def __init__(self, _player) -> None:
        pass

    def getNextMove(self, state) -> Union[int, int]:
        inp = input("Enter Location: ")
        inp = inp.split(" ")
        i = int(inp[0])
        j = int(inp[1])
        return (i, j)
