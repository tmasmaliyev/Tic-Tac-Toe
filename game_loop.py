import api

game_id = 5250
team_id = 1456



print("INFO: Starting the loop.")
print("INFO: Game details:")
game_details = api.get_game_details(game_id)
print(f"\ttarget: {game_details['target']}\n\tstatus: {game_details['status']}\n\twinnerTeamId: {game_details['winnerteamid']}\n\tturnTeamId: {game_details['turnteamid']}")
    

def heurestic():    
    return

is_team_turn = api.isTeamsTurn(game_id, team_id)

while True:
    print("INFO: Current board state:")
    print(api.get_board_string(game_id))
    while not is_team_turn:
        print("INFO: Waiting for the other time to move...")
        print("INFO: If they have played, write 1 :")
        resp = input()
        if(int(resp) == 1):
            is_team_turn = api.isTeamsTurn(game_id, team_id)
            if not is_team_turn:
                print("INFO: It seems like they haven't played yet.")
            else:
                print("INFO: Current board state:")
                print(api.get_board_string(game_id))
                break

    print("INFO: Its your turn. Waiting for the heurestic function to recommend a move.")
    move = heurestic()
    print(f"INFO: Preparing to play at {move}")

    move_resp = api.make_move(game_id, team_id, move)
    while not move_resp:
        print("ERROR: There was a problem playing the move. Please enter the move manually: ")
        inp_move = input()
        move_resp = api.make_move(game_id, team_id, inp_move)

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
