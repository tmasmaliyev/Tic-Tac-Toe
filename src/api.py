import os
import requests
from dotenv import load_dotenv
import json
from http import HTTPMethod

from board import State


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
    try:
        if method == HTTPMethod.GET:
            response = requests.get(url=api_url, headers=headers, data=data, params=params, timeout=15)
        elif method == HTTPMethod.POST:
            response = requests.post(url=api_url, headers=headers, data=data, params=params, timeout=15)
        else:
            print("Unimplemented method type.")
        if response.text == "":
            return
        resp_json = json.loads(response.text)
        if(resp_json["code"] == "FAIL"):
            print(resp_json["message"])
            return
        return resp_json
    except requests.exceptions.Timeout as e:
        print("ERROR: The request timed out after 15 seconds.")
        return {}


def get_game_details(gameId: int):
    try:
        params = {"type":"gameDetails", "gameId": gameId}
        response = send_request(HTTPMethod.GET, None, params)
        if(response['game'] == '{}'):
            print("ERROR in get_game_details: Invalid gameId")
            return
        return json.loads(response['game'])
    except Exception as e:
        print(e)

def isTeamsTurn(gameId: int, teamId: int):
    game_details = get_game_details(gameId)
    print(game_details)
    return int(game_details['turnteamid']) == teamId

def check_win(gameId: int, teamId: int):
    try:
        game_details = get_game_details(gameId)
        winner_team_id = game_details['winnerteamid']
        if winner_team_id == None:
            return 0
        winner_team_id = int(winner_team_id)
        if winner_team_id == teamId:
            return 1
        else:
            return -1
    except Exception as e:
        print(e)

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
        return dict()
    return json.loads(response['output'])

def make_move(gameId: int, teamId: int, move: str):
    data = {"type": "move", "gameId": gameId, "teamId": teamId, "move": move}
    response = send_request(HTTPMethod.POST, data, None)
    if response is not None:
        print(f"INFO: Team({teamId}) move on {move}")
    return response

def transform_to_grid(input_dict, rows=3, cols=3):
    grid = [[State.Blank for _ in range(cols)] for _ in range(rows)]
    if input_dict is None:
        return grid
    for key, value in input_dict.items():
        r, c = map(int, key.split(','))
        player = State.X if value == 'X' else State.O
        grid[r][c] = player
    return grid


def find_new_key(dict1, dict2):
    key = (set(dict1) - set(dict2)).pop()
    return tuple(map(int, key.split(',')))

