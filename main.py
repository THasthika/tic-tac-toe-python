from board import Board, MARK_X, MARK_O
from ai import MinMaxNode, RandomAgent, MinMaxAgent
from human_agent import HumanAgent

import time

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--display", dest='display', action='store_true')
parser.add_argument("--no-display", dest='display', action='store_false')
parser.add_argument("--x-depth", type=int, default=1)
parser.add_argument("--o-depth", type=int, default=1)
parser.set_defaults(display=True)


def main(args):

    pargs = parser.parse_args(args)

    if pargs.display:
        print("Starting Game...")

    board = Board()
    players = {
        MARK_X: HumanAgent(MARK_X),
        MARK_O: MinMaxAgent(MARK_O, max_depth=pargs.o_depth)
    }

    while True:
        player = board.get_active_payer()
        
        if pargs.display:
            print("Player {} turn".format(player))
            print(board)

        validMove = False
        while not validMove:
            (i, j) = players[player].get_next_move(board.positions)
            validMove = board.mark_position(i - 1, j - 1)
            if not validMove:
                print("Warning: Not a valid move!... retry")

        # check for win
        winner = Board.winner(board.positions)
        if not winner is None:
            if pargs.display:
                print(board)
                print("Player {} Won!".format(winner))
            return winner
        elif not board.is_playable():
            if pargs.display:
                print("Draw!")
            return None

        # time.sleep(.5)

if __name__ == "__main__":
    main(sys.argv[1:])
