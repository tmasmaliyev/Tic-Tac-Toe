import os
import requests
from dotenv import load_dotenv
import json
from http import HTTPMethod


load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
user_id = os.getenv('USER_ID')

headers = {
    'x-api-key': api_key,
    'userId': user_id,
    'User-Agent': 'PostmanRuntime/7.43.3'
}

def send_request(method: HTTPMethod, data: dict, params: dict):
    if method == HTTPMethod.GET:
        response = requests.get(url=api_url, headers=headers, data=data, params=params)
    elif method == HTTPMethod.POST:
        response = requests.post(url=api_url, headers=headers, data=data, params=params)
    else:
        print("Unimplemented method type.")
    if response.text == "":
        return
    resp_json = json.loads(response.text)
    if(resp_json["code"] == "FAIL"):
        print(resp_json["message"])
        return
    return resp_json

def get_game_details(gameId: int):
    params = {"type":"gameDetails", "gameId": gameId}
    response = send_request(HTTPMethod.GET, None, params)
    if(response['game'] == '{}'):
        print("ERROR in get_game_details: Invalid gameId")
        return
    return json.loads(response['game'])

def isTeamsTurn(gameId: int, teamId: int):
    game_details = get_game_details(gameId)
    return int(game_details['turnteamid']) == teamId

def check_win(gameId: int, teamId: int):
    game_details = get_game_details(gameId)
    winner_team_id = game_details['winnerteamid']
    if winner_team_id == teamId:
        return 1
    elif winner_team_id == None:
        return 0
    else:
        return -1

def check_draw(gameId: int):
    game_details = get_game_details(gameId)
    board_size = int(game_details['boardsize'])
    return board_size * board_size == int(game_details['moves'])


def get_board_string(gameId: int):
    params = {"type": "boardString", "gameId": gameId}
    response = send_request(HTTPMethod.GET, None, params)
    return response['output']

def get_board_map(gameId: int):
    params = {"type": "boardMap", "gameId": gameId}
    response = send_request(HTTPMethod.GET, None, params)
    if response['output'] is None:
        return
    return json.loads(response['output'])

def make_move(gameId: int, teamId: int, move: str):
    data = {"type": "move", "gameId": gameId, "teamId": teamId, "move": move}
    response = send_request(HTTPMethod.POST, data, None)
    if response is not None:
        print(f"INFO: Team({teamId}) move on {move}")
    return response

def transform_to_grid(input_dict, rows=3, cols=3):
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    if input_dict is None:
        return grid
    for key, value in input_dict.items():
        r, c = map(int, key.split(','))
        grid[r][c] = value
    return grid


def find_new_key(dict1, dict2):
    key = (set(dict1) - set(dict2)).pop()
    return tuple(map(int, key.split(',')))

