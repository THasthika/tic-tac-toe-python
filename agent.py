from abc import ABC, abstractmethod
from typing import Union

class Agent(ABC):

    @abstractmethod
    def getNextMove(self, state) -> Union[int, int]:
        pass