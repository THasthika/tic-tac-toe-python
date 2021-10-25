"""
Board Representation and State management class
"""

MARK_X = "x"
MARK_O = "o"
MARK_EMPTY = "-"

HORIZONTAL = [
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2))
]

VERTICAL = [
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2))
]

DIAGONAL = [
    ((0, 0), (1, 1), (2, 2)),
    ((2, 0), (1, 1), (0, 2))
]

ALL = [*HORIZONTAL, *VERTICAL, *DIAGONAL]


class Board:
    

    def __init__(self) -> None:

        self.activePlayer = MARK_X
        self.positions = [[MARK_EMPTY for _ in range(0, 3)] for _ in range(0, 3)]

    def get_position(self, i, j):
        return self.positions[i][j]

    @staticmethod
    def winner(state):

        item_list = list(map(
            lambda x: ''.join(list(map(
                lambda y: state[y[0]][y[1]], x)))
            , ALL))

        if any(filter(lambda x: x == 'xxx', item_list)):
            return 'x'

        if any(filter(lambda x: x == 'ooo', item_list)):
            return 'o'

        return None

    # isPlayable() - check if the game can be progressed
    def is_playable(self):

        playable = False

        # if all the positions are not empty we cannot proceed
        for i in self.positions:
            for x in i:
                if x == MARK_EMPTY:
                    playable = True

        return playable

    # getActivePlayer() - return the player who needs to make the move
    def get_active_payer(self) -> str:
        return self.activePlayer

    def mark_position(self, pi, pj):

        # get active player
        m = self.get_active_payer()

        # valid range
        if (pi not in [0, 1, 2]) or (pj not in [0, 1, 2]):
            return False

        # if not empty raise exception
        pv = self.positions[pi][pj]
        if pv != MARK_EMPTY:
            return False

        # else mark the position with the player mark
        self.positions[pi][pj] = m

        # switch active player
        if self.activePlayer == MARK_X:
            self.activePlayer = MARK_O
        else:
            self.activePlayer = MARK_X

        return True

    def __str__(self) -> str:
        ret = "\n"
        for i in range(0, 3):
            ret += "|"
            for j in range(0, 3):
                ret += self.positions[i][j]
                ret += "|"
            ret += "\n"
        return ret
