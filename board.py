"""
Board Representation and State management class
"""

MARK_X = "x"
MARK_O = "o"
MARK_EMPTY = "-"

class Board():

    activePlayer = MARK_X
    positions = [[MARK_EMPTY for _ in range(0, 3)] for _ in range(0, 3)]

    def __init__(self) -> None:
        pass

    def getPosition(self, i, j):
        return self.positions[i][j]

    def checkWinningCondition(self):
        
        # check horizontal
        for i in range(0, 3):
            f = False
            pv = None
            for j in range(0, 3):
                x = self.positions[i][j]
                if x == MARK_EMPTY:
                    f = False
                    break
                if pv == None:
                    pv = x
                    f = True
                if pv != x:
                    f = False
                    break
            if f == True:
                return True
        
        # check vertical
        for j in range(0, 3):
            f = False
            pv = None
            for i in range(0, 3):
                x = self.positions[i][j]
                if x == MARK_EMPTY:
                    f = False
                    break
                if pv == None:
                    pv = x
                    f = True
                if pv != x:
                    f = False
                    break
            if f == True:
                return True

        # check top-left to lower-right diagonal
        for l in [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]:
            f = False
            pv = None
            for (i, j) in l:
                x = self.positions[i][j]
                if x == MARK_EMPTY:
                    f = False
                    break
                if pv == None:
                    pv = x
                    f = True
                if pv != x:
                    f = False
                    break
            if f == True:
                return True

        return False

    # isPlayable() - check if the game can be progressed
    def isPlayable(self):
        
        playable = False

        # if all the positions are not empty we cannot proceed
        for i in self.positions:
            for x in i:
                if x == MARK_EMPTY:
                    playable = True

        return playable

    # getActivePlayer() - return the player who needs to make the move
    def getActivePlayer(self) -> str:
        return self.activePlayer

    def markPosition(self, pi, pj):

        # get active player
        m = self.getActivePlayer()

        # if not empty raise exception
        pv = self.positions[pi][pj]
        if pv != MARK_EMPTY:
            raise Exception("Cannot Overwrite Position")

        # else mark the position with the player mark
        self.positions[pi][pj] = m

        # switch active player
        if self.activePlayer == MARK_X:
            self.activePlayer = MARK_O
        else:
            self.activePlayer = MARK_X

    # getBoardString() -> return string formatted board to be printed
    def getBoardString(self) -> str:
        ret = "\n"
        for i in range(0, 3):
            ret += "|"
            for j in range(0, 3):
                ret += self.positions[i][j]
                ret += "|"
            ret += "\n"
        return ret
