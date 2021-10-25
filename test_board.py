import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        b = Board()

        assert b.mark_position(0, 0) is True
        assert b.mark_position(0, 1) is True
        assert b.mark_position(1, 1) is True
        assert b.mark_position(0, 2) is True
        assert b.mark_position(2, 2) is True
        assert b.mark_position(1, 2) is True

        assert Board.winner(b.positions) == 'x'


if __name__ == "__main__":
    unittest.main()
