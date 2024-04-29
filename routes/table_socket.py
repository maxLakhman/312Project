from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_socketio import SocketIO, emit, disconnect
from flask_login import current_user
from app import socketio
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
from routes.table import table_collection
import random

# If player folds/disconnects from table session I add this to end of username in table
suffix = ".)G&*9q2ih}kc$RKiCN*e3#v]);Gp=[_pXd!FcjLY@;7cx]$8N"

@socketio.on("init_game")
def init_game(data):
    table_id = data["table_id"]
    table = table_collection.find_one({"table_id": table_id})

    # Joining game that already started
    if table.get("started") == True:
        emit("error", {"message": "Game already started.", "table_id": table_id})
        return
    
    # Joining game that's in init phase
    elif table.get("started") == "In progress...":
        emit("init_players", {"message": "Welcome", "table_id": table_id})
        return
    
    # Making game for first time
    table_collection.update_one({"table_id": table_id}, {"$set": {"started": "In progress..."}})
    time_out = 60
    player_ready = table_collection.find_one({"table_id": table_id},{"_id":0,"player_ready":1})["player_ready"]
    while time_out > 0 and not player_ready:
        player_ready = table_collection.find_one({"table_id": table_id},{"_id":0,"player_ready":1})["player_ready"]
        emit("init_players", {"table_id": table_id , "message": f"Waiting {time_out} seconds for players to join or click button to start now."}, broadcast=True)
        socketio.sleep(1)
        time_out -= 1

    time_out = 0

    table_collection.update_one({"table_id": table_id}, {"$set": {"started": True}})
    emit("init_players", {"message": "Game starting...", "table_id": table_id}, broadcast=True)
    socketio.sleep(2)


    start_game(table_id)

# @socketio.on("start_game")
def start_game(table_id):
    
    table = table_collection.find_one({"table_id": table_id})
    player_list = table.get("players")
    deck = table.get("deck")

    # Shuffle Deck
    random.shuffle(deck)

    # Dealer
    dealer_hand = deck[:2]
    deck = deck[2:]
    update_dealer_hand(table_id, dealer_hand)
    update_deck(table_id, deck)
    emit("update_hand", {"dealer_hand": dealer_hand, "table_id": table_id}, broadcast=True)
    
    # Giving everyone there their first hand
    for player in player_list:
        player_hand = deck[:2]
        deck = deck[2:]
        update_player_hand(player, player_hand)
        update_deck(table_id, deck)
        emit("update_hand", {"player_hand": player_hand, "username": player, "table_id": table_id}, broadcast=True)

    # First player
    current_player = table["players"][0]
    table_collection.update_one({"table_id": table_id}, {"$set": {"current_player": current_player}})
    user_collection.update_one({"username": current_player}, {"$set": {"has_moved": False}})
    
    # Game Loop Start
    game_over = table.get("game_over")
    while not game_over:
        current_player = table_collection.find_one({"table_id": table_id},{"_id":0, "current_player": 1})["current_player"]
        user_collection.update_one({"username": player}, {"$set": {"has_moved": False}})

        timer = 30
        while not game_over and timer > 0 and not user_collection.find_one({"username": current_player},{"_id":0, "has_moved": 1})["has_moved"]:
            check_if_game_over(table_id)
        
            emit("current_player", {"username": current_player, "table_id": table_id, "time": timer}, broadcast=True)
            socketio.sleep(1)
            timer -= 1
        
        check_if_game_over(table_id)
        
        if not user_collection.find_one({"username": current_player},{"_id":0,"has_moved": 1})["has_moved"]:
            emit("current_player", {"username": current_player, "table_id": table_id, "time": 0}, broadcast=True)
            handle_fold_back(current_player, table_id)
            socketio.sleep(1)
        
        check_if_game_over(table_id)

        game_over = table_collection.find_one({"table_id": table_id}).get("game_over")
        if game_over:
            table_collection.delete_one({"table_id":table_id})
            break

        if not next_turn(table_id):
            # Dealers turn
            print("HAND =================================================")
            hand = table_collection.find_one({"table_id": table_id}, {"_id": 0, "dealer_hand": 1})["dealer_hand"]
            hand_value = calculateHand(hand)
            print(hand)
            print(hand_value)

            if hand_value < 17:
                table_info = table_collection.find_one({"table_id": table_id})

                # add a new card to the user's hand
                deck = table_info.get("deck")
                random.shuffle(deck)
                new_card = deck[0]
                deck = deck[1:]
                hand.append(new_card)

                # update the user's hand in the database
                update_dealer_hand(table_id, hand)

                # update the table's deck in the database
                update_deck(table_id, deck)

                # emit the new card to the user
                emit("update_hand", {"dealer_hand": hand, "table_id": table_id}, broadcast=True)

                game_over = True
                table_collection.update_one({"table_id": table_id}, {"$set": {"game_over": True}})
                break

    print("END OF GAME =============================")


# money stuff
@socketio.on("increase_bet")
def handle_increase_bet(data):
    if not current_user.is_authenticated:
        disconnect()

    table_id = data["table_id"]
    
    user = user_collection.find_one({"username": current_user.id})

    balance = user.get("balance")
    bet = user.get("bet")

    if balance > bet + 1:
        bet += 1
        balance -= 1
        user_collection.update_one({"username": current_user.id}, {"$set": {"bet": bet, "balance": balance}})

        emit("update_bet", {"username": current_user.id, "balance": balance, "bet": bet, "table_id": table_id}, broadcast=True)
    
@socketio.on("decrease_bet")
def handle_decrease_bet(data):
    if not current_user.is_authenticated:
        disconnect()

    table_id = data["table_id"]
    
    user = user_collection.find_one({"username": current_user.id})

    balance = user.get("balance")
    bet = user.get("bet")

    if bet > 0:
        bet -= 1
        balance += 1
        user_collection.update_one({"username": current_user.id}, {"$set": {"bet": bet, "balance": balance}})
        
        emit("update_bet", {"username": current_user.id, "balance": balance, "bet": bet, "table_id": table_id}, broadcast=True)

@socketio.on("fold")
def handle_fold_front(data):
    if not current_user.is_authenticated:
        disconnect()

    table_id = data["table_id"]

    current_player = table_collection.find_one({"table_id": table_id},{"_id": 0, "current_player": 1})

    if "current_player" not in current_player:
        return
    current_player = current_player["current_player"]
    
    if current_user.id == current_player:
        handle_fold_back(current_player, table_id)
    else:
        return

def handle_fold_back(player, table_id):
    player_index = get_player_index(table_id, player)
    new_username = player + suffix
    table_collection.update_one({"table_id": table_id}, {"$set": {f"players.{player_index}": new_username}})

    user_collection.update_one({"username": player}, {"$set": {"hand": [], "has_moved": True}})
    
    emit("update_hand", {"player_hand": [], "username": player, "table_id": table_id}, broadcast=True)

@socketio.on("hit")
def handle_hit(data):

    if not current_user.is_authenticated:
        disconnect()

    table_id = data["table_id"]
    current_player = table_collection.find_one({"table_id": table_id},{"_id": 0, "current_player": 1})

    if "current_player" not in current_player:
        return
    current_player = current_player["current_player"]
    if current_player != current_user.id:
        return
    
    user = user_collection.find_one({"username": current_player})

    # find the table id
    table_info = table_collection.find_one({"table_id": table_id})

    # add a new card to the user's hand
    hand = user.get("hand")
    deck = table_info.get("deck")
    random.shuffle(deck)
    new_card = deck[0]
    deck = deck[1:]
    hand.append(new_card)

    # update the user's hand in the database
    update_player_hand(current_player, hand)

    # update the table's deck in the database
    update_deck(table_id, deck)

    user_collection.update_one({"username": current_player}, {"$set": {"has_moved": True}})


    # emit the new card to the user
    emit("update_hand", {"player_hand": hand, "username": current_player, "table_id": table_id}, broadcast=True)

@socketio.on("stand")
def handle_stand(data):
    if not current_user.is_authenticated:
        disconnect()
    
    table_id = data["table_id"]
    
    current_player = table_collection.find_one({"table_id": table_id},{"_id": 0, "current_player": 1})

    if "current_player" not in current_player:
        return
    current_player = current_player["current_player"]
    if current_player != current_user.id:
        return
    
    user_collection.update_one({"username": current_player}, {"$set": {"has_moved": True}})

    pass

def next_turn(table_id):
    table = table_collection.find_one({"table_id": table_id})
    player_list = table["players"]

    try:
        current_player_index = player_list.index(table["current_player"])
    except ValueError:
        current_player_index = player_list.index(table["current_player"] + suffix)

    print("CURRENT PLAYER INDEX")
    print(current_player_index)


    next_player = player_list[(current_player_index + 1) % len(player_list)]
    
    # If one or more players disconnected/folded
    max_players = 5
    while next_player.endswith(suffix):
        current_player_index += 1
        
        next_player = player_list[(current_player_index + 1) % len(player_list)]

        max_players -= 1
        # If all players disconnected/folded
        if max_players < 0:
            table_collection.update_one({"table_id": table_id}, {"$set": {"game_over": True}})
            break
    
    if (current_player_index + 1) % len(player_list) == 0:
        return False
        

    table_collection.update_one({"table_id": table_id}, {"$set": {"current_player": next_player}})
    user_collection.update_one({"username": next_player}, {"$set": {"has_moved": False}})

    emit("next_turn", {"username": next_player, "table_id": table_id}, broadcast=True)

    return True


def update_deck(table_id, deck):
    table_collection.update_one({"table_id": table_id}, {"$set": {"deck": deck}})

def update_dealer_hand(table_id, hand):
    table_collection.update_one({"table_id": table_id}, {"$set": {"dealer_hand": hand}})

def update_player_hand(username, hand):
    user_collection.update_one({"username": username}, {"$set": {"hand": hand}})

def get_player_index(table_id, player):
    table_players = table_collection.find_one({"table_id": table_id}, {"_id": 0, "players": 1})
    player_index = table_players["players"].index(player)
    return player_index

def check_if_game_over(table_id):
    player_list = table_collection.find_one({"table_id": table_id}, {"_id": 0, "players": 1})["players"]

    disconnected_players = 0
    for player in player_list:
        if player.endswith(suffix):
            disconnected_players += 1

    if disconnected_players == len(player_list):
        table_collection.update_one({"table_id": table_id}, {"$set": {"game_over": True}})

@socketio.on("user_connect")
def handle_connect(data):
    table_id = user_collection.find_one({"username": data["username"]}, {"_id": 0, "table": 1})
    emit("user_connected", {"username": data["username"], "table_id": table_id}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    print("DISCONNECCCCCTEDDDDD")
    if current_user.id:
        
        table_id = user_collection.find_one({"username": current_user.id}, {"_id": 0, "table": 1})

        # If table exists
        if table_collection.find_one({"table_id": table_id},):
            players = table_collection.find_one({"table_id": table_id}, {"_id": 0, "players": 1})["players"]
            
            # If user is part of the table:
            if current_user.id in players:
                new_username = current_user.id + suffix
                player_index = get_player_index(table_id, current_user.id)
                table_collection.update_one({"table_id": table_id}, {"$set": {f"players.{player_index}": new_username}})

        user_collection.update_one({"username": current_user.id}, {"$set": {"table": None, "hand": None, "has_moved": None}})

        emit("user_disconnected", {"username": current_user.id, "table_id": table_id}, broadcast=True)

@socketio.on("player_ready")
def handle_player_ready(data):
    table_id = data["table_id"]
    table_collection.update_one({"table_id":table_id},{"$set":{"player_ready":True}})
def calculateHand(hand):
    total_value = 0
    ace_count = 0
    
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    
    for card in hand:
        # Get value
        rank = card[:-1]
        total_value += card_values[rank]
        
        if rank == 'A':
            ace_count += 1
    
    # Adjust total value for Aces
    while total_value > 21 and ace_count > 0:
        total_value -= 10
        ace_count -= 1
    
    return total_value