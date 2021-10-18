from board import Board, MARK_X, MARK_O
from ai import RandomAgent
from human_agent import HumanAgent

def main():

    print("Starting Game...")

    board = Board()
    players = {
        MARK_X: HumanAgent(MARK_X),
        MARK_O: RandomAgent(MARK_O)
    }

    prev_player = None

    while True:
        player = board.getActivePlayer()
        print("Player {} turn".format(player))
        print(board.getBoardString())

        (i, j) = players[player].getNextMove(board.positions)
        board.markPosition(i-1, j-1)
        prev_player = player

        # check for win
        if board.checkWinningCondition():
            print(board.getBoardString())
            print("Player {} Won!".format(prev_player))
            break
        elif not board.isPlayable():
            print("Draw!")
            break

if __name__ == "__main__":
    main()