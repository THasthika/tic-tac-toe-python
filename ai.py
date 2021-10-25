import random
from typing import List, Union, Tuple, Any

from agent import Agent
from board import MARK_O, MARK_X, MARK_EMPTY, ALL, Board
import copy

"""
node (move, value=None)
"""

class MinMaxNode:

    def __init__(self, move, state, depth, player, value=None, parent=None) -> None:
        self.move = move
        self.state = state
        self.value = value
        self.depth = depth
        self.player = player
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
        return "Parent({}) -> Move: {} | Value: {} | Depth: {} | Player: {} | # Children: {}".format(None if self.parent is None else self.parent.move, self.move, self.value, self.depth, self.player, len(self.children))

class MinMaxTree:

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

    def get_next_move(self, state) -> Tuple[int, int]:
        ri = random.randint(1, 3)
        rj = random.randint(1, 3)
        while state[ri-1][rj-1] != MARK_EMPTY:
            ri = random.randint(1, 3)
            rj = random.randint(1, 3)
        return ri, rj

class MinMaxAgent(Agent):

    def __init__(self, player, max_depth=1) -> None:
        self.player = player
        self.max_depth = max_depth
        self.opponent = MARK_X if player == MARK_O else MARK_O

    def evaluate(self, state) -> int:

        """
        return the current score for the player

        horizontal, vertical and diagonal -> empty or like values increase score otherwise decrease
        """

        score = 0

        for r in ALL:
            pv = None
            for (i, j) in r:
                if pv is None:
                    pv = state[i][j]
                    continue
                if pv == MARK_EMPTY:
                    pv = None
                    break
                if pv != state[i][j]:
                    pv = None
                    break
            if pv is None:
                continue
            if pv == self.player:
                score += 1
            elif pv == self.opponent:
                score -= 1

        return score

    @staticmethod
    def make_move(move, state, player):
        new_state = copy.deepcopy(state)
        new_state[move[0]-1][move[1]-1] = player
        return new_state


    @staticmethod
    def generate_moves(state) -> List[Tuple[Union[int, Any], Union[int, Any]]]:

        moves = []

        # check playable
        if not Board.winner(state) is None:
            return moves

        for (ri, r) in enumerate(state):
            for (ci, c) in enumerate(r):
                if c == MARK_EMPTY:
                    moves.append((ri+1, ci+1))
        
        return moves

    def evaluate_node(self, node):
        node.set_value(self.evaluate(node.state))

    def process_node(self, node: MinMaxNode):

        ## if evaluated no need to work
        if node.value is not None:
            return
        
        ## if no children evaluate
        if len(node.children) == 0:
            self.evaluate_node(node)
            return

        
        ## if there are children, evaluate the children first
        for n in node.children:
            self.process_node(n)
        
        m = None

        ## after evaluating the children take the max or minimum WRT
        if node.player == self.player:
            ## get maximum
            m = node.children[0].value
            for i in range(1, len(node.children)):
                t = node.children[i].value
                if m < t:
                    m = t
        else:
            ## get minimum
            m = node.children[0].value
            for i in range(1, len(node.children)):
                t = node.children[i].value
                if m > t:
                    m = t

        node.value = m
        

    def construct_min_max_tree(self, state, max_depth=1):
        
        root_node = MinMaxNode(None, state, 0, self.player)
        nodes = [root_node]

        while len(nodes) > 0:
            c_node = nodes.pop(-1)
            c_player = c_node.player

            moves = []
            if c_node.depth < max_depth:
                moves = self.generate_moves(c_node.state)

            # handle nodes that generate no moves
            # either board is full, someone has won or max depth reached
            if len(moves) == 0:
                self.evaluate_node(c_node)

            for move in moves:
                new_state = self.make_move(move, c_node.state, c_player)
                player = self.player if c_player == self.opponent else self.opponent
                node = MinMaxNode(move, new_state, c_node.depth + 1, player, parent=c_node)
                c_node.add_child(node)
                nodes.append(node)

        self.process_node(root_node)

        tree = MinMaxTree(root_node)

        return tree

    @staticmethod
    def get_best_move(tree) -> Union[int, int]:
        root_node = tree.root
        rv = root_node.value
        moves = []
        for c in root_node.children:
            if rv == c.value:
                moves.append(c.move)
        i = random.randint(0, len(moves)-1)
        return moves[i]

    def get_next_move(self, state) -> Union[int, int]:
        t = self.construct_min_max_tree(state, max_depth=self.max_depth)
        move = self.get_best_move(t)
        return move