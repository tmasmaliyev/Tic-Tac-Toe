from algorithms import Algorithms
from board import Board, State

class TicTacToe:
    def __init__(self, board: Board) -> None:
        self.game_board = board
        self.ai = True

    def play_move(self) -> None:
        if self.ai:
            Algorithms.minimax(self.game_board)
        else:
            Algorithms.random(self.game_board)

        return

    def play(self) -> None:
        while True:
            self.game_board.draw_board()

            if self.game_board.game_over:
                if self.game_board.winner != State.Blank:
                    print(f'{self.game_board.winner.value} is the winner !')
                else:
                    print(f'Game is draw !')

                break

            self.play_move()
            self.ai = not self.ai