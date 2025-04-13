from board import Board
import random


class Random:
    @classmethod
    def invoke(cls, board: Board) -> None:
        index = random.choice(list(board.available_moves))

        board.move(index)
