from math import inf
import api
import sys
import time
from board import Board
from minimax import Minimax

if len(sys.argv) != 4:
    print("Usage: py game_loop.py --game_id --team_id --depth")
    sys.exit()

game_id = int(sys.argv[1])
team_id = int(sys.argv[2])
depth = int(sys.argv[3])

print("INFO: Starting the loop.")
print("INFO: Game details:")
game_details = api.get_game_details(game_id)
board_map = api.get_board_map(game_id)
print(f"\ttarget: {game_details['target']}\n\tstatus: {game_details['status']}\n\twinnerTeamId: {game_details['winnerteamid']}\n\tturnTeamId: {game_details['turnteamid']}")
n = int(game_details['boardsize'])
m = int(game_details['target'])
game_state = Board(n, m)
game_state.board = api.transform_to_grid(board_map, n, n)
game_state.moves_count = int(game_details['moves'])
player_icon = 'O' if int(game_details['team1id']) == team_id else 'X'

if int(game_details['turnteamid']) == team_id:
    if player_icon == 'O':
        game_state.switch_turn()

is_team_turn = int(game_details['turnteamid']) == team_id

while True:
    print("INFO: Current board state:")
    game_state.draw_board()

    while not is_team_turn:
        print("INFO: Waiting for the other team to move...")
        time.sleep(1)
        is_team_turn = api.isTeamsTurn(game_id, team_id)
        print(f"INFO: Calling isTeamsTurn with game_id = {game_id}, team_id = {team_id}, result = {is_team_turn}")

        if not is_team_turn:
            print("DEBUG: Calling check_win...")
            is_won = api.check_win(game_id, team_id)
            print(f"DEBUG: check_win returned: {is_won}")
            if is_won == -1:
                print(api.get_board_string(game_id))
                print("INFO: The other team has won the game.")
                sys.exit()
        else:
            board_map_played = api.get_board_map(game_id)
            played_move = api.find_new_key(board_map_played, board_map)
            board_map = board_map_played.copy()
            game_state.move(game_state.board_position_to_index(played_move[0], played_move[1]))
            print(f"INFO: The other team has played on {played_move[0]},{played_move[1]}")
            print("INFO: Current board state:")
            game_state.draw_board()
            break

    print("INFO: It's your turn. Waiting for the heuristic function to recommend a move...")
    move_idx = -1
    Minimax.max_depth = depth
    if game_state.moves_count == 0:
        if game_state.board_width % 2 == 1:
            move_idx = game_state.num_elements // 2
        else:
            move_idx = game_state.num_elements // 2 - game_state.board_width // 2 - 1
    else:
        move_idx, _ = Minimax.minimax(game_state, game_state.player_turn, 0, -inf, inf)
    if move_idx == -1:
        print("INFO: There are no moves left to play.")
        break
    move = game_state.index_to_board_position(move_idx)
    move_req = f"{move[0]},{move[1]}"
    print(f"INFO: Preparing to play at {move_req}")

    move_resp = api.make_move(game_id, team_id, move_req)
    while not move_resp:
        print("ERROR: There was a problem playing the move. Please enter the move manually: ")
        inp_move = input()
        move_resp = api.make_move(game_id, team_id, inp_move)
        move = tuple(map(int, inp_move.split(',')))

    game_state.move(game_state.board_position_to_index(move[0], move[1]))
    board_map = api.get_board_map(game_id)
    game_state.draw_board()

    print("INFO: Checking for win...")
    win = api.check_win(game_id, team_id)
    if win == 1:
        print("INFO: You have won the game. Congratulations!")
        break
    elif win == -1:
        print("INFO: The other team has won the game.")
        break
    else:
        draw = api.check_draw(game_id)
        if draw:
            print("INFO: The game has ended in a draw.")
            break
        else:
            print("INFO: The game is still ongoing.")

    is_team_turn = False
