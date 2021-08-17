from django.shortcuts import render
from game import *
from AI.models import *
from game.models import *
from game.business import *
import random
from random import randint
from functools import reduce
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django import forms
from connection.models import User, User_data
from game.models import Game_Player, Game_State
from game.business import *
from game.services import *
from game.exceptions import *
from AI.models import AI
from django.db import transaction
import time

up = [-1,0]
down = [1,0]
right = [0,1]
left=[0,-1]
tab_direction=[up,down,right,left]

global Epsilon
Epsilon= []
global States
States = []


def play_ai(board,pos1,pos2,user,game_player,curr_player):
    ai = AI.manager.get(id = user.ai_id.id)
    eps = user.ai_id.epsilon
    board_db = verify_board(board,pos1,pos2,ai)
    direction = move(eps,board_db.q_table,board_db.position)
    while not verify_direction(direction,board,pos1,curr_player):
        direction = move(eps,board_db.q_table,board_db.position)
    if game_player.previous_state_ai:
        update_q_table(board,board_db,pos1,pos2,user.ai_id,game_player,game_player.old_direction, direction)
    direction_board = [tab_direction[direction],board_db]
    return direction_board

def epsilon_greedy(user):
    E=user.ai_id.epsilon
    i_partie=user.nb_games
    if i_partie % user.ai_id.speed_learning == 0:
        E = (E /100) * 95
    if E < 5: return 5
    return E

def move(eps,q_table,position):
    q_table=string_to_list(q_table)
    r=random.randint(0, 100)
    
    if qtable_count_value(q_table) == 0 or r < eps:
        direction = randint(0, 3)
    else:
        direction = q_table.index(max(q_table))
    return direction

def qtable_count_value(q_table):
    return reduce(lambda x,y: x+y, q_table)

def verify_direction(direction,board,pos,curr_player):
    x=pos[0]+tab_direction[direction][0]
    y=pos[1]+tab_direction[direction][1]
   
    if x < 0 or x > 7 or y < 0 or y > 7: 
        return False
    else:
        return board[x][y] ==curr_player+1 or board[x][y] == 0

def verify_board(searched_board,searched_position1,searched_position2,ai):
    board=str(searched_board)
    pos1=str(searched_position1)
    pos2=str(searched_position2)

    try:
        board_db = State.manager.get(board = board, position = pos1,position2 = pos2,ai_id=ai)
    except Exception as e:
        board_db = register_board(board,pos1,pos2,ai)
    return board_db

def register_board(board,position,position2,ai):
    state = State(board = board, position = position,position2 = position2 ,q_table = "[0,0,0,0]",ai_id = ai)
    state.save()
    return state

def update_q_table(board,board_db,pos1,pos2,ai,game_player,old_direction, direction): #0 = up , 1 = down , 2 = right , 3 = left
    old_q = string_to_list(game_player.previous_state_ai.q_table)
    q_table_list = string_to_list(board_db.q_table)
    max_q = max(q_table_list)
    recompense=calculate_reward(board,pos1,pos2,game_player)
    print("old direction 2",old_direction)
    print(old_q)
    print("recompense",recompense)
    if(old_direction is not None):
        old_q[old_direction] = old_q[old_direction] + ai.learning_rate*(recompense+0.9*max_q-old_q[old_direction])
    state=game_player.previous_state_ai
    state.q_table=old_q
    state.save()
    game_player.previous_state_ai.q_table=old_q
    game_player.old_direction = direction
    game_player.save()
    board_db.save()
    ai.save()
    print(old_q)
def count_boxes(board,num_player):
    return reduce(lambda x,y: x+y, board).count(num_player)

def best_reward_and_position(pos,previous_board,num_player,old_pos, board):  
    best_points = 0
    best_position = [pos[0]+tab_direction[0][0],pos[1]+tab_direction[0][1]]
    for i in tab_direction:
        pos[0]+=i[0]
        pos[1]+=i[1]
        #complete_boxes(previous_board,num_player,old_pos)
        previous_points = count_boxes(previous_board,num_player)
        new_points = count_boxes(board,num_player)
        reward = new_points - previous_points
        if reward > best_points:
            best_points = reward
            best_position = pos
    return best_points,best_position

def calculate_reward(board,ai_position,opp_position,gameplayer): 
    previous_state = gameplayer.previous_state_ai
    try:
        pos_ai = string_to_list( previous_state.position)
    except Exception as e:
        pos_ai =previous_state.position
    pos = opp_position
    try:
        previous_board = string_to_list(previous_state.board)
    except Exception as e:
        previous_board = previous_state.board

    try:
        previous_opp_pos = string_to_list(previous_state.position2)
    except Exception as e:
        previous_opp_pos = previous_state.position2
    num_opp = board[pos[0]][pos[1]]
    num_player = board[ai_position[0]][ai_position[1]]
    
    best_points_opp,best_position_opp = best_reward_and_position(pos,previous_board,num_opp,previous_opp_pos, board)
    best_points_ai,best_position_ai = best_reward_and_position(ai_position,previous_board,num_player,pos_ai, board)

    
    if ai_position == best_position_opp:
        if best_points_opp > best_points_ai:
            return best_points_opp
        else:
            return 1
    else:
        return count_cells(previous_board,board,num_player)


def count_cells(old_board, new_board, num_player):
    old_nb_boxes = count_boxes(old_board,num_player)
    new_nb_boxes = count_boxes(new_board,num_player)

    return new_nb_boxes - old_nb_boxes
    
    
#train

def setup_training(ai1, ai2):
    Epsilon.append(ai1)
    Epsilon.append(ai2)

def get_limit():
    return len(States)

def get_data_from_training():
    return Epsilon, States

def clear_data():
    global States
    States = []
    Epsilon = []

def training_play (board, pos1, pos2, game_player, curr_player, ai, old_direction):
    eps = ai.epsilon
    board_db = verify_board_training(board,pos1,pos2,ai)
    direction = move(eps,board_db.q_table,board_db.position)
    while not verify_direction(direction,board,pos1,curr_player):
        direction = move(eps,board_db.q_table,board_db.position)
    if game_player.previous_state_ai:
        update_q_table_training(board,board_db,pos1,pos2,ai,game_player,old_direction)
    direction_board = [tab_direction[direction],board_db]
    return direction_board, direction

def epsilon_greedy_training(ai): 
    i_partie=ai.nb_games_training 
    E,i = find_epsilon(ai)
    if i_partie % ai.speed_learning == 0:
        E = (E /100) * 95
    if E < 5: 
        E = 5
    Epsilon[i].epsilon = E
    return E

def find_epsilon(ai):
    for ia in Epsilon:
        if ia.id == ai.id:
            return ia.epsilon, Epsilon.index(ia)
    return 0


def verify_board_training(searched_board,searched_position1,searched_position2,ai):
    board=str(searched_board)
    pos1=str(searched_position1)
    pos2=str(searched_position2)
    board_db,i = find_state(board, pos1, pos2, ai)
    if i == 0: #Stocké en interne
        States.append(State(board = board, position = pos1,position2 = pos2 ,q_table = "[0,0,0,0]",ai_id = ai))
        board_db = States[-1]
    elif i == -1: #Stocké en DB
        States.append(State(id = board_db.id, board = board, position = pos1,position2 = pos2 ,q_table = board_db.q_table,ai_id = ai))
    return board_db

def find_state(board, pos1, pos2, ai):
    for state in States:
        if state.ai_id == ai and state.board == board and state.position == pos1 and state.position2 == pos2:
            return state, States.index(state)
    try:
        state = State.manager.get(board = board, position = pos1,position2 = pos2,ai_id=ai)
        return state,-1
    except Exception as e:
        return 0,0

   

def update_q_table_training(board,board_db,pos1,pos2,ai,game_player,old_direction):
    old_q = string_to_list(game_player.previous_state_ai.q_table)
    q_table_list = string_to_list(board_db.q_table)
    max_q = max(q_table_list)
    recompense=calculate_reward(board,pos1,pos2,game_player)
    if old_direction is not None:
        old_q[old_direction] = old_q[old_direction] + ai.learning_rate*(recompense+max_q-old_q[old_direction])
    state = game_player.previous_state_ai    
    s, i = find_state(state.board, state.position, state.position2, state.ai_id)
    States[i].q_table = old_q

class NewGameForm(forms.Form):
    ia1 = forms.CharField(label="IA 1")
    ia2 = forms.CharField(label="IA 2")
    nb_games = forms.IntegerField(label="Number of games")

    def clean(self):
        cd = self.cleaned_data

        c_ia1 = cd.get("ia1")
        c_ia2 = cd.get("ia2")
        c_nb_games = cd.get("nb_games")


        try:
            ia1 = User.manager.get(username = c_ia1)
        except User.DoesNotExist:
            raise forms.ValidationError("IA1 doesn't exist")

        try:
            ia2 = User.manager.get(username = c_ia2)
        except User.DoesNotExist:
            raise forms.ValidationError("IA2 doesn't exist")

        if c_nb_games < 1:
            raise forms.ValidationError("The number of games must be more than 0")

        return cd


def train(request):
    if request.method == "GET":
        form = NewGameForm(auto_id='id_for_%s')
        return render(request, "train/train.html", { "form": form })

    if request.method == "POST": 
        form = NewGameForm(request.POST)
        if form.is_valid():
            nb_games = form.cleaned_data.get("nb_games")
            ia1 = User.manager.get(username=form.cleaned_data.get("ia1"))
            ia2 = User.manager.get(username=form.cleaned_data.get("ia2"))
            setup_games(ia1, ia2, nb_games)
            return HttpResponse("Training done, check the log file for more data.")
        return render(request, "train/train.html", { "form": form })

def setup_games(ia1, ia2, nb_games):
    setup_training(ia1.ai_id, ia2.ai_id)
    chronos = []
    for i in range(nb_games):
        print("Game "+str(i+1)+" en cours")
        debut_game = time.time()
        play(ia1, ia2)
        fin_game = time.time()
        duree_game = fin_game - debut_game
        chronos.append(duree_game)
        print(str(duree_game)+" secondes")
        print("Game "+str(i+1)+" terminée")
    print("Les variables globales ont été nettoyées")
    temps_total = reduce(lambda x,y: x+y,chronos)
    print("Les "+str(nb_games)+" parties ont pris "+str(round(temps_total,2))+" secondes à se réaliser, soit "+str(round(temps_total/nb_games,2))+" secondes par partie en moyenne.")    

def play(u1, u2):
    """
    SETUP DE LA GAME
    """
    board = [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]]
    #board = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,2]]
    game_state_data = Game_State(current_player=1, board=board)
    game_state_data.save()
    game_player1 = Game_Player(user=u1, game_state=game_state_data, pos=[0,0])
    game_player2 = Game_Player(user=u2, game_state=game_state_data, pos=[7,7])
    #game_player1 = Game_Player(user=u1,game_state=game_state_data, pos=[0,0])
    #game_player2 = Game_Player(user=u2,game_state=game_state_data, pos=[3,3])
    game_player1.user.ai_id.nb_games_training+=1
    game_player1.user.ai_id.save()
    game_player2.user.ai_id.nb_games_training+=1
    game_player2.user.ai_id.save()
    current_player = None
    u1.ai_id.epsilon = epsilon_greedy_training(u1.ai_id)
    u2.ai_id.epsilon = epsilon_greedy_training(u2.ai_id)
    game_players = [game_player1, game_player2]
    indice=0
    game_state = build_game_state(game_state_data, [game_player1, game_player2], game_player1.auto_increment_id,0)  
    """
    DEBUT DE LA PARTIE
    """
    direction = None
    while is_current_player_ai(game_players[indice]) and not end_of_game(game_state_data.board):
        user = get_user_from_player(u1, u2, game_players[indice])
        movement, direction = do_play(board, game_players,indice, user, direction)
        game_state_data = move_pos(game_players[indice], movement, game_state_data, game_players)
        indice = switch_player(indice)
        game_state = build_game_state(game_state_data, [game_player1, game_player2], game_player2.auto_increment_id,0)
        if end_of_game(game_state_data.board):
            """
            FIN DE LA PARTIE
            """
            game_state = build_game_state(game_state_data, game_players, current_player, 0)
            winner_id, nb_cell_winner, tie = define_winner(game_state.get("board"))
            data_winner = {"name": game_players[winner_id-1].user.username, "nb_cell": nb_cell_winner, "tie":tie}
            game_state["winner"] =  data_winner
            game_players[winner_id-1].user.ai_id.nb_games_training_wins+=1
            game_players[winner_id-1].user.ai_id.save()
            save_data_from_training()
            clear_data()
            with open("log.txt", "a") as f:
                f.write("Tie\n"if game_state.get("winner").get("tie") else ""+ game_state.get("winner").get("name")+" with "+str(game_state.get("winner").get("nb_cell"))+" cells.\n")

def switch_player(indice):
    return 1 if indice == 0 else 0
    
def do_play(board, game_players, indice, user, direction):
    if indice == 1:
        i_o = 0
    else:
        i_o = 1
    direction_board, direction =training_play(board,game_players[indice].pos,game_players[i_o].pos,game_players[indice],indice, user.ai_id, direction)
    movement = direction_board[0]
    game_players[indice].previous_state_ai = direction_board[1]
    return movement, direction


def get_user_from_player(u1,u2, game_player):
    return u1 if game_player.user.username == u1.username else u2

"""
Difference between Atomic Transaction and Bulk create:
For 50000 saves
Atomic Transaction takes: 27s
Bulk create takes: 3.5s
https://pmbaumgartner.github.io/blog/the-fastest-way-to-load-data-django-postgresql/
"""

@transaction.atomic 
def save_data_from_training():
    ai_s, states = get_data_from_training()
    for ai in ai_s:
        ai.save()
    for state in states:
        state.save()
    print(str(len(states))+" nouveaux états créés")


"""
The problem with the bulk_create method is that it doesn't do update.
It only does create statement, which is a problem because we often update State.
If we decide to fix this with conditions, we will probably be slower than with an atomic transaction due to conditions.
"""
"""
def save_data_from_training():
    ai_s, states = get_data_from_training()
    states_list = []
    for ai in ai_s:
        ai.save()
    for state in states:
        states_list.append(state)
    State.manager.bulk_create(states_list)
    print(str(len(states_list))+" nouveaux états créés")
   """ 
