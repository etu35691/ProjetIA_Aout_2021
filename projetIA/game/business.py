import ast
from game.exceptions import *
from functools import reduce
from game.services import *
from connection.models import *

def change_player(players,index_player):
    index_player = int(index_player)
    return players[0].auto_increment_id if index_player == len(players)-1 else players[index_player+1].auto_increment_id

def index_player(id_player, players):
    return players.index(reduce(lambda a, b: a if a.auto_increment_id == id_player else b, players))

    
def calculate_position(player_pos, movement):
    position =  [player_pos[0]+movement[0], player_pos[1]+movement[1]]
    if is_coord_valide(position):
        return position
    else:
        raise OufOfBoardError("Test", "OutOfBoardError has occured")

def is_coord_valide(coord):
    return len(list(filter(lambda x: x >= 0 and x < 8 , coord))) == 2

def update_board_content(board, player, num_player, previous_pos):
    position = player.pos
    if board[position[0]][position[1]] != num_player+1 and board[position[0]][position[1]] != 0:
        player.pos = previous_pos
        raise NotEmptyCellError("Test", "NotEmptyCellError has occured")
    board[position[0]][position[1]] = num_player+1
    return board, player.pos

def string_to_list(s):
    if isinstance(s, str):
        return ast.literal_eval(s)
    return s

def listing_game_players(game_players):
    return listing_player_pos(list(game_players))

def listing_player_pos(players):
    return [convert_pos(p) for p in players]

def convert_pos(player):
    player.pos = string_to_list(player.pos)
    return player


def build_game_state(game_state_data, players, curr_player, code_error):
    players = build_players_entities(players)
    game_state = {
        "game_id" : game_state_data.auto_increment_id,
        "board" : game_state_data.board,
        "players" : players,
        "current_player" : curr_player,
        "code" : code_error, 
    }
    return game_state

def build_players_entities(players):
    players_obj = []
    for player in players:
        dic = {
            "id":player.auto_increment_id,
            "name" : player.user.username,
            "color" : player.color,
            "position" : player.pos
        }
        players_obj.append(dic)
    return players_obj

def build_colors(users):
    colors = []
    for user in users:
        temp = []
        color1= user.color1
        color2= user.color2
        temp.append(color1)
        temp.append(color2)
        colors.append(temp)
    colors = sort_colors(colors)
    return colors


def sort_colors(colors):
    colorsReplace = ["salmon","pink","coral","gold","darkkhaki","orchid"] #a completer si + de 7 joueurs (longueur de colors replace >= nb joueurs-1)
    tabColors = []
    #print(colors[0][0])
    tabColors.append(colors[0][0])
    i = 1
    j=0
    while i < len(colors):
        temp = colors[i][0]
        if temp not in tabColors:
            tabColors.append(temp)
        else:
            temp = colors[i][1]
            if temp not in tabColors:
                tabColors.append(temp)
            else:
                tabColors.append(colorsReplace[j])
                j+=1
        i+=1
    return tabColors
    
def move_pos(player, movement, game_state, players):
    previous_pos = player.pos
    player.pos = calculate_position(player.pos, movement)
    game_state.board, player.pos = update_board_content(game_state.board, player, players.index(player), previous_pos)
    complete_boxes(game_state.board,players.index(player)+1,player.pos)
    return game_state

def search_player_by_id(players, id):
    return reduce(lambda a, b: a.user.username if a.auto_increment_id == id else b, players)



def count_elements(stats, element):
    if(stats.get(element,0)==0):
        stats[element] = 1
    else:
        stats.update({element:stats.get(element)+1})
    return stats

def define_winner(board):
    stats = {}
    for line in board:
        for cell in line:
            stats = count_elements(stats, cell)
    max = -1
    kmax = -1
    tie = False
    for key,element in stats.items():
        if max < element:
            kmax = key
            max = element
            tie = False
        elif max == element:
            tie = True
    return (kmax, max, tie)

def end_of_game(board):
    return all([line.count(0)==0 for line in board])

def complete_boxes(board,player,coord):
    list_coor=[]
    completed_list=[]
    if coord[0]>0 and board[coord[0]-1][coord[1]]==0:
        coord1=[coord[0]-1,coord[1]]
        list_coor.append(coord1)       
    if coord[0]<len(board)-1 and board[coord[0]+1][coord[1]]==0:
        coord2=[coord[0]+1,coord[1]]
        list_coor.append(coord2)
    if coord[1]>0 and board[coord[0]][coord[1]-1]==0:
        coord3=[coord[0],coord[1]-1]
        list_coor.append(coord3)
    if coord[1]<len(board)-1 and board[coord[0]][coord[1]+1]==0:
        coord4=[coord[0],coord[1]+1]
        list_coor.append(coord4)
    if len(list_coor)>0:
        x=list_coor[0]
        for x in list_coor:        
            for y in x:
                if y < 0:               
                    del x[y]
            if len(x)%2==1:           
                    list_coor.remove(x)
    list_of_boxes_to_fill(list_coor,board,player,completed_list)    
    tab=clean_tab(completed_list)
    board=complete_board(tab,board,player)    
    
def list_of_boxes_to_fill(liste,board,player,full_liste):
    for elem in liste:
        temp_liste=[elem]
        i=0
        while i<len(temp_liste):
            val=temp_liste[i]                       
            temp_liste=free_boxes(val,board,player,temp_liste)
            i=i+1            
        full_liste.append(temp_liste)    
    return full_liste  

def free_boxes(coord,board,player,temp_liste):   
    if coord[0]>0 and board[coord[0]-1][coord[1]]==0:
        coord1=[coord[0]-1,coord[1]]
        if coord1 not in temp_liste:
            temp_liste.append(coord1)
    else: 
        if coord[0]>0 and board[coord[0]-1][coord[1]]!=player:
            temp_liste=[]
            return temp_liste
    if coord[0]<len(board)-1 and board[coord[0]+1][coord[1]]==0:
        coord2=[coord[0]+1,coord[1]]
        if coord2 not in temp_liste:
            temp_liste.append(coord2)
    else: 
        if coord[0]<len(board)-1 and board[coord[0]+1][coord[1]]!=player:
            temp_liste=[]
            return temp_liste
    if coord[1]>0 and board[coord[0]][coord[1]-1]==0:
        coord3=[coord[0],coord[1]-1]
        if coord[1]>0 and coord3 not in temp_liste:
            temp_liste.append(coord3)
    else: 
        if coord[1]>0 and board[coord[0]][coord[1]-1]!=player:
            temp_liste=[]
            return temp_liste
    if coord[1]<len(board)-1 and board[coord[0]][coord[1]+1]==0:
        coord4=[coord[0],coord[1]+1]
        if coord4 not in temp_liste:
            temp_liste.append(coord4)
    else: 
        if coord[1]<len(board)-1 and board[coord[0]][coord[1]+1]!=player:
            temp_liste=[]
            return temp_liste    
    return temp_liste

def clean_tab(list_):
    return list([element for e in list_ for element in e])

def complete_board(tab,board,player):
    for coord in tab:
        board[coord[0]][coord[1]]=player
    return board

def print_winner(game_state, game_player):
    winner_id, nb_cell_winner, tie = define_winner(game_state.get("board"))
    data_winner = {"name": game_player.user.username, "nb_cell": nb_cell_winner, "tie":tie}
    game_state["winner"] =  data_winner
    return game_state

def is_current_player_ai(game_player):
    return game_player.user.ai_id

def save_game_turn(game_state_data, game_players):
    save_data(game_state_data)
    for game_player in game_players:
        save_data(game_player)

def get_game_player(username,game_state_data, pos,col, num_player):
    u = User.manager.get(username = username)
    game_player = Game_Player(user=u, game_state=game_state_data, pos=pos , color = col, num_player = num_player)
    game_player.save()
    return game_player