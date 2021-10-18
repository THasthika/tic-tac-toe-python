import random
from typing import List, Union

from agent import Agent
from board import MARK_O, MARK_X, MARK_EMPTY
import copy

"""
node (move, value=None)
"""

class MinMaxNode(object):

    def __init__(self, move, state, depth, value=None, parent=None) -> None:
        self.move = move
        self.state = state
        self.value = value
        self.depth = depth
        self.children = []
        self.parent = parent

    def set_value(self, value) -> None:
        self.value = value

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def add_child(self, child) -> None:
        self.children.append(child)

    def next_child(self):
        for c in self.children:
            yield c

    def __str__(self) -> str:
        return "Parent({}) -> Move: {} | Value: {} | Depth: {} | # Children: {}".format(None if self.parent is None else self.parent.move, self.move, self.value, self.depth, len(self.children))

class MinMaxTree():

    def __init__(self, root) -> None:
        self.root = root

    def __depth_first_str(self) -> str:
        # depth first traversal
        s = ""
        nodes = [self.root]
        while len(nodes) > 0:
            c_node = nodes.pop(-1)
            s += str(c_node) + "\n"
            nodes.extend(c_node.children)
        return s
    
    def __str__(self) -> str:
        return self.__depth_first_str()
    

class RandomAgent(Agent):

    def __init__(self, player) -> None:
        self.player = player

    def getNextMove(self, state) -> Union[int, int]:
        ri = random.randint(1, 3)
        rj = random.randint(1, 3)
        while state[ri-1][rj-1] != MARK_EMPTY:
            ri = random.randint(1, 3)
            rj = random.randint(1, 3)
        return (ri, rj)

class MinMaxAgent(Agent):

    def __init__(self, player) -> None:
        self.player = player
        self.opponent = MARK_X if player == MARK_O else MARK_O

    def evaluate_item(self, c, t):
        if c == self.player and t > 0:
            t *= 2
        elif c == self.opponent:
            t *= -3 if t > 0 else 3
        return t

    def evaluate(self, state) -> int:

        """
        return the current score for the player

        horizontal, vertical and diagonal -> empty or like values increase score otherwise decrease
        """

        h_s = 0

        ## check horizontal

        for r in state:
            t = 1
            for c in r:
                t = self.evaluate_item(c, t)
            h_s += t

        ## check vertical

        v_s = 0

        for i in range(0, 3):
            t = 1
            for j in range(0, 3):
                c = state[j][i]
                t = self.evaluate_item(c, t)
            v_s += t

        ## check diagonal

        d_s = 0

        for d in [-1, 1]:
            t = 1
            for i in range(0, 3):
                j = i if d == 1 else (2 - i)
                c = state[i][j]
                t = self.evaluate_item(c, t)
            d_s += t

        s = h_s + v_s + d_s

        return s

    def makeMove(self, move, state, player):
        new_state = copy.deepcopy(state)
        new_state[move[0]-1][move[1]-1] = player
        return new_state


    def generateMoves(self, state) -> List[Union[int, int]]:

        moves = []

        for (ri, r) in enumerate(state):
            for (ci, c) in enumerate(r):
                if c == MARK_EMPTY:
                    moves.append((ri+1, ci+1))
        
        return moves

    def constructMinMaxTree(self, state, max_depth=1):
        
        root_node = MinMaxNode(None, state, 0)
        nodes = [root_node]
        c_player = self.player

        need_calculation = []

        while len(nodes) > 0:
            c_node = nodes.pop(0)
            moves = self.generateMoves(c_node.state)
            for move in moves:
                new_state = self.makeMove(move, c_node.state, c_player)
                node = MinMaxNode(move, new_state, c_node.depth+1, parent=c_node)
                c_node.add_child(node)
                if node.depth < max_depth:
                    nodes.append(node)
                    if node.depth + 1 == max_depth:
                        need_calculation.append(node)
                else:
                    # calculate score
                    node.set_value(self.evaluate(node.state))
            # switch player
            c_player = self.player if c_player == self.opponent else self.opponent

        if len(need_calculation) == 0:
            need_calculation = [root_node]

        while len(need_calculation) > 0:
            c_node = need_calculation.pop(0)

            if not c_node.value is None:
                continue

            isMax = True if c_node.depth % 2 == 0 else False

            v = None
            ## loop over all children and find the min or max
            for child in c_node.next_child():
                if v is None:
                    v = child.value
                    continue
                if isMax:
                    if v < child.value:
                        v = child.value
                else:
                    if v > child.value:
                        v = child.value
            c_node.value = v

            if not c_node.parent is None:
                need_calculation.append(c_node.parent)

        tree = MinMaxTree(root_node)

        return tree

    def getBestMove(self, tree) -> Union[int, int]:
        root_node = tree.root
        rv = root_node.value
        for c in root_node.next_child():
            if rv == c.value:
                return c.move

    def getNextMove(self, state) -> Union[int, int]:
        # construct min max tree

        # evaluate move score
        # return (0, 0)

        # current_score = self.evaluate(state)

        t = self.constructMinMaxTree(state, max_depth=6)
        print(t.root)
        for x in t.root.next_child():
            print(x)

        move = self.getBestMove(t)

        return move