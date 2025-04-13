from board import Board
from tictactoe import TicTacToe
from typing import List
import sys

def main(args: List[str]) -> None:
    board_width = 5
    num_marks_to_win = 3

    if len(args) > 2:
        board_width, num_marks_to_win = map(int, args[1:3])

        if num_marks_to_win > board_width:
            raise ValueError("Number of marks to win must not exceed board width.")

    board = Board(board_width, num_marks_to_win)

    tictactoe = TicTacToe(board)
    tictactoe.play()

if __name__ == "__main__":
    main(sys.argv)
