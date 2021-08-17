from game.models import Game_Player, Game_State

def save_data(entity):
    entity.save()

def get_gamestate_data(game_id):
    return Game_State.manager.get(auto_increment_id = game_id)

def get_all_player_from_gamestate(game_state_data):
    return Game_Player.manager.all().filter(game_state = game_state_data)
