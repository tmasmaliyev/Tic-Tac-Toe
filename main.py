import math
import copy

class GameState:
    def __init__(self, n, m):
        self.n = n  
        self.m = m 
        self.board = [['.' for _ in range(n)] for _ in range(n)]

        self.current_player = 'X'

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_available_moves(self):
        return [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == '.']

    def make_move(self, row, col):
        new_state = copy.deepcopy(self)
        new_state.board[row][col] = self.current_player
        new_state.switch_player()

        return new_state

    def is_terminal(self):
        return self.check_winner('X') or self.check_winner('O') or not self.get_available_moves()

    def check_winner(self, player):
        n, m, B = self.n, self.m, self.board

        def check_line(line):
            count = 0
            for cell in line:
                count = count + 1 if cell == player else 0
                if count == m:
                    return True
            return False

        for i in range(n):
            if check_line(B[i]) or check_line([B[j][i] for j in range(n)]):
                return True

        for i in range(n):
            for j in range(n):
                if i + m <= n and check_line([B[i + k][j] for k in range(m)]):
                    return True
                if j + m <= n and check_line([B[i][j + k] for k in range(m)]):
                    return True
                if i + m <= n and j + m <= n and check_line([B[i + k][j + k] for k in range(m)]):
                    return True
                if i + m <= n and j - m + 1 >= 0 and check_line([B[i + k][j - k] for k in range(m)]):
                    return True
                
        return False

    def evaluate(self, player):
        opponent = 'O' if player == 'X' else 'X'

        return self.heuristic(player) - self.heuristic(opponent)

    def heuristic(self, player):
        score = 0
        n, m, B = self.n, self.m, self.board

        def line_score(line):
            max_seq = 0
            cnt = 0
            for cell in line:
                if cell == player:
                    cnt += 1
                    max_seq = max(max_seq, cnt)
                    
                elif cell != '.':
                    cnt = 0

            return 10 ** max_seq if max_seq > 0 else 0

        for i in range(n):
            score += line_score(B[i])
            score += line_score([B[j][i] for j in range(n)])

        for i in range(n - m + 1):
            for j in range(n - m + 1):
                diag1 = [B[i + k][j + k] for k in range(m)]
                diag2 = [B[i + k][j + m - 1 - k] for k in range(m)]
                score += line_score(diag1)
                score += line_score(diag2)

        return score

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()


def minimax(state, depth, alpha, beta, maximizing, player):
    if depth == 0 or state.is_terminal():
        return state.evaluate(player), None

    best_move = None

    if maximizing:
        max_eval = -math.inf

        for move in state.get_available_moves():
            new_state = state.make_move(*move)

            eval, _ = minimax(new_state, depth - 1, alpha, beta, False, player)

            if eval > max_eval:
                max_eval, best_move = eval, move

            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval, best_move
    
    else:
        min_eval = math.inf

        for move in state.get_available_moves():
            new_state = state.make_move(*move)

            eval, _ = minimax(new_state, depth - 1, alpha, beta, True, player)

            if eval < min_eval:
                min_eval, best_move = eval, move

            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval, best_move


def play(n = 5, m = 4, depth = 4):
    state = GameState(n, m)

    while not state.is_terminal():
        state.print_board()

        _, move = minimax(state, depth, -math.inf, math.inf, True, state.current_player)
        print(move)
        if move is None:
            print("No moves left.")
            break

        state = state.make_move(*move)

    state.print_board()

    if state.check_winner('X'):
        print("X wins!")

    elif state.check_winner('O'):
        print("O wins!")

    else:
        print("Draw!")

if __name__ == '__main__':
    # play(n=3, m=3, depth=6)
    state = GameState(3, 3)
    _, move = minimax(state, 6, -math.inf, math.inf, True, state.current_player)
    move_req = f"{move[0]},{move[1]}"
    print(move_req)
