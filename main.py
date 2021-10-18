from board import Board, MARK_X, MARK_O
from ai import RandomAgent, MinMaxAgent
from human_agent import HumanAgent

import time

def main():

    print("Starting Game...")

    board = Board()
    players = {
        MARK_X: HumanAgent(MARK_X),
        MARK_O: MinMaxAgent(MARK_O)
    }

    prev_player = None

    while True:
        player = board.getActivePlayer()
        print("Player {} turn".format(player))
        print(board)

        validMove = False
        while not validMove:
            (i, j) = players[player].getNextMove(board.positions)
            validMove = board.markPosition(i-1, j-1)
            if not validMove:
                print("Warning: Not a valid move!... retry")

        prev_player = player

        # check for win
        if board.checkWinningCondition():
            print(board)
            print("Player {} Won!".format(prev_player))
            break
        elif not board.isPlayable():
            print("Draw!")
            break

        time.sleep(.5)

if __name__ == "__main__":
    main()