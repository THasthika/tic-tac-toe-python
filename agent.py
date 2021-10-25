from abc import ABC, abstractmethod
from typing import Union


class Agent(ABC):

    @abstractmethod
    def get_next_move(self, state) -> Union[int, int]:
        pass
