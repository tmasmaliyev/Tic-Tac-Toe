import api
from main import *

game_id = 5263
team_id = 1455
depth = 5



print("INFO: Starting the loop.")
print("INFO: Game details:")
game_details = api.get_game_details(game_id)
board_map = api.get_board_map(game_id)
print(f"\ttarget: {game_details['target']}\n\tstatus: {game_details['status']}\n\twinnerTeamId: {game_details['winnerteamid']}\n\tturnTeamId: {game_details['turnteamid']}")
n = int(game_details['boardsize'])
m = int(game_details['target'])
game_state = GameState(n, m)
game_state.board = api.transform_to_grid(board_map, n, n)
player_icon = 'O' if int(game_details['team1id']) == team_id else 'X'

if int(game_details['turnteamid']) == team_id:
    if player_icon == 'O':
        game_state.switch_player()


is_team_turn = int(game_details['turnteamid']) == team_id

while True:
    print("INFO: Current board state:")
    game_state.print_board()
    while not is_team_turn:
        print("INFO: Waiting for the other team to move...")
        print("INFO: If they have played, write 1 :")
        resp = input()
        if(int(resp) == 1):
            is_team_turn = api.isTeamsTurn(game_id, team_id)
            if not is_team_turn:
                print("INFO: It seems like they haven't played yet.")
            else:
                board_map_played = api.get_board_map(game_id)
                played_move = api.find_new_key(board_map_played, board_map)
                board_map = board_map_played.copy()
                game_state = game_state.make_move(*played_move)
                print(f"INFO: The other team has played on {played_move[0]},{played_move[1]}")
                print("INFO: Current board state:")
                game_state.print_board()
                break

    print("INFO: Its your turn. Waiting for the heurestic function to recommend a move...")
    _, move = minimax(game_state, depth, -math.inf, math.inf, True, game_state.current_player)
    if move is None:
        print("INFO: There are no moves left to play.")
        break
    move_req = f"{move[0]},{move[1]}"
    print(f"INFO: Preparing to play at {move_req}")

    move_resp = api.make_move(game_id, team_id, move_req)
    while not move_resp:
        print("ERROR: There was a problem playing the move. Please enter the move manually: ")
        inp_move = input()
        move_resp = api.make_move(game_id, team_id, inp_move)
        move  = tuple(map(int, inp_move.split(',')))
    game_state = game_state.make_move(*move)

    print(f"INFO: Checking for win...")
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
            print("INFO: The game is stil ongoing.")
    is_team_turn = api.isTeamsTurn(game_id, team_id)
