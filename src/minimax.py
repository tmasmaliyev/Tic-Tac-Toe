from board import Board, State
from math import inf

from multiprocessing import Pool, Manager, cpu_count

from typing import Tuple, List, Dict, Optional

class MinimaxExtended:
    # manager = None
    # cache = None

    @classmethod
    def initialize_max_depth(cls, max_depth: int):
        cls.max_depth = max_depth
    
    # @classmethod
    # def initializer(cls, max_depth: int, shared_cache: Dict):
    #     cls.initialize_max_depth(max_depth)
    #     cls.cache = shared_cache

    @classmethod
    def invoke(cls, board: Board, player: State, max_depth: int) -> None:
        if max_depth <= 0:
            raise ValueError("Maximum depth must be greater than 0.")
    
        # if cls.cache is None:
        #     cls.manager = Manager()
        #     cls.cache = cls.manager.dict()

        if board.moves_count == 0:
            if board.board_width % 2 == 1:
                board.move(board.num_elements // 2)
            else:
                board.move(board.num_elements // 2 - board.board_width // 2 - 1)
        else:
            task_args = [(board.deepcopy(), player, 0, -inf, inf) for _ in board.get_available_moves()]

            with Pool(
                processes = cpu_count(),
                initializer = cls.initialize_max_depth,
                initargs = (max_depth, )
            ) as pool:
                results = pool.starmap(cls.minimax, task_args)
            
            best_move, _ = max(results, key=lambda x: x[1])

            board.move(best_move)

    @classmethod
    def minimax(
        cls,
        board: Board,
        player: State,
        depth: int,
        alpha: float,
        beta: float,
    ) -> Tuple[Optional[int], float]:
        if board.game_over:
            if board.winner == board.player_turn:
                return None, 1e12 - depth
            elif board.winner != board.player_turn:
                return None, -depth - 1e12
            else:
                return None, 0


        if depth == cls.max_depth:
            return None, cls.score(board, player)

        depth += 1

        if board.player_turn == player:
            # move, score = cls.maximize(board, player, depth, alpha, beta)
            return cls.maximize(board, player, depth, alpha, beta)
        else:
            # move, score = cls.minimize(board, player, depth, alpha, beta)
            return cls.minimize(board, player, depth, alpha, beta)
        
        # cls.cache[(board, player, depth)] = (move, score)
        
        # return move, score

    @classmethod
    def maximize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> Tuple[int, float]:
        best_move = -1

        available_moves = board.get_available_moves()

        for the_move in available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            _, score = cls.minimax(temp_board, player, depth, alpha, beta)

            if score > alpha:
                alpha = score
                best_move = the_move

            if alpha >= beta:
                break

        # if best_move != -1:
        #     board.move(best_move)

        return best_move, alpha

    @classmethod
    def minimize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> Tuple[int, float]:
        best_move = -1
        available_moves = board.get_available_moves()
        # random.shuffle(available_moves)

        for the_move in available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            _, score = cls.minimax(temp_board, player, depth, alpha, beta)

            if score < beta:
                beta = score
                best_move = the_move

            if alpha >= beta:
                break

        # if best_move != -1:
        #     board.move(best_move)

        return best_move, beta
    
    @classmethod
    def score(cls, board : Board, player : State) -> int:
        score = 0

        directions = [
            (1, 0),  # Horizontal
            (0, 1),  # Vertical
            (1, 1),  # Diagonal /
            (1, -1), # Diagonal \
        ]

        for x in range(board.board_width):
            for y in range(board.board_width):
                for dx, dy in directions:
                    line = []

                    for i in range(board.num_marks_to_win):
                        nx, ny = x + i * dx, y + i * dy

                        if 0 <= nx < board.board_width and 0 <= ny < board.board_width:
                            line.append(board.board[nx][ny])
                        else:
                            break

                    if len(line) == board.num_marks_to_win:
                        score += Minimax.evaluate_line(line, player)

        return score

    @classmethod
    def evaluate_line(cls, line : List[State], player : State) -> int:
        opponent = State.O if player == State.X else State.X

        player_count = line.count(player)
        opponent_count = line.count(opponent)

        score = 0

        if opponent_count == 0:
            if player_count > 0:
                score += 10 ** player_count
            
            if player_count == len(line) - 1:
                score += 750

        elif player_count == 0:
            if opponent_count > 0:
                score -= 10 ** opponent_count
            
            if opponent_count == len(line) - 1:
                score -= 500

        return score
    


class Minimax:
    # cache : dict = {}

    @classmethod
    def invoke(cls, board: Board, player: State, max_depth: int) -> None:
        if max_depth <= 0:
            raise ValueError("Maximum depth must be greater than 0.")

        cls.max_depth = max_depth
        # len(board.available_moves) == board.num_elements

        if board.moves_count == 0:
            if board.board_width % 2 == 1:
                board.move(board.num_elements // 2)
            else:
                board.move(board.num_elements // 2 - board.board_width // 2 - 1)
        else:
            best_move, _ = cls.minimax(board, player, 0, -inf, inf)

            board.move(best_move)

    @classmethod
    def minimax(
        cls,
        board: Board,
        player: State,
        depth: int,
        alpha: float,
        beta: float,
    ) -> Tuple[Optional[int], float]:
        # if (board, player, depth) in Minimax.cache:
        #     return Minimax.cache[(board, player, depth)]

        if board.game_over:
            if board.winner == board.player_turn:
                return None, 1e12 - depth
            elif board.winner != board.player_turn:
                return None, -depth - 1e12
            else:
                return None, 0

        if depth == cls.max_depth:
            return None, cls.score(board, player)

        depth += 1

        if board.player_turn == player:
            # move, score = cls.maximize(board, player, depth, alpha, beta)
            return cls.maximize(board, player, depth, alpha, beta)
        else:
            # move, score = cls.minimize(board, player, depth, alpha, beta)
            return cls.minimize(board, player, depth, alpha, beta)

        # Minimax.cache[(board, player, depth)] = (move, score)
        
        # return move, score

    @classmethod
    def maximize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> Tuple[int, float]:
        best_move = -1

        available_moves = board.get_available_moves()

        for the_move in available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            _, score = cls.minimax(temp_board, player, depth, alpha, beta)

            if score > alpha:
                alpha = score
                best_move = the_move

            if alpha > beta:
                break

        # if best_move != -1:
        #     board.move(best_move)

        return best_move, alpha

    @classmethod
    def minimize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> Tuple[int, float]:
        best_move = -1
        available_moves = board.get_available_moves()
        # random.shuffle(available_moves)

        for the_move in available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            _, score = cls.minimax(temp_board, player, depth, alpha, beta)

            if score < beta:
                beta = score
                best_move = the_move

            if alpha > beta:
                break

        # if best_move != -1:
        #     board.move(best_move)

        return best_move, beta
    
    @classmethod
    def score(cls, board : Board, player : State) -> int:
        score = 0

        directions = [
            (1, 0),  # Horizontal
            (0, 1),  # Vertical
            (1, 1),  # Diagonal /
            (1, -1), # Diagonal \
        ]

        for x in range(board.board_width):
            for y in range(board.board_width):
                for dx, dy in directions:
                    line = []

                    for i in range(board.num_marks_to_win):
                        nx, ny = x + i * dx, y + i * dy

                        if 0 <= nx < board.board_width and 0 <= ny < board.board_width:
                            line.append(board.board[nx][ny])
                        else:
                            break

                    if len(line) == board.num_marks_to_win:
                        score += Minimax.evaluate_line(line, player)

        return score

    @classmethod
    def evaluate_line(cls, line : List[State], player : State) -> int:
        opponent = State.O if player == State.X else State.X

        player_count = line.count(player)
        opponent_count = line.count(opponent)

        score = 0

        if opponent_count == 0:
            if player_count > 0:
                score += 10 ** player_count
            
            if player_count == len(line) - 1:
                score += 1000

        elif player_count == 0:
            if opponent_count > 0:
                score -= 10 ** opponent_count
            
            if opponent_count == len(line) - 1:
                score -= 500

        return score