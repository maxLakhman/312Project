from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_socketio import SocketIO, emit, disconnect
from flask_login import current_user
from app import socketio
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
from routes.table import table_collection
import random


@socketio.on("init_game")
def init_game(data):

    table_id = data["table_id"]
    table = table_collection.find_one({"table_id": table_id})

    if table.get("started") and time_out == 0:
        emit("error", {"message": "Game already started.", "table_id": table_id})
        return
    
    elif table.get("started") == "In progress..." and time_out > 0:
        emit("init_players", {"message": "Welcome", "table_id": table_id})
        return
    
    table_collection.update_one({"table_id": table_id}, {"$set": {"started": "In progress..."}})
    time_out = 10
    while time_out > 0:
        emit("init_players", {"table_id": table_id , "message": f"Waiting {time_out} seconds for players to join."}, broadcast=True)
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

        timer = 30
        while timer > 0 and not user_collection.find_one({"username": current_player},{"_id":0, "has_moved": 1})["has_moved"]:
            emit("current_player", {"username": current_player, "table_id": table_id, "time": timer}, broadcast=True)
            socketio.sleep(1)
            timer -= 1
        
        if not user_collection.find_one({"username": current_player},{"_id":0,"has_moved": 1})["has_moved"]:
            emit("current_player", {"username": current_player, "table_id": table_id, "time": 0}, broadcast=True)
            handle_fold_back(current_player, table_id)
            socketio.sleep(1)

        game_over = table_collection.find_one({"table_id": table_id}).get("game_over")
        if game_over:
            table_collection.delete_one({"table_id":table_id})
            break

        next_turn(table_id)
    if game_over:
        # Do something
        print(" hello there")


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
    user_collection.update_one({"username": player}, {"$set": {"hand": [], "has_moved": True}})
    table_collection.update_one({"table_id": table_id}, {"$pull": {"players": player}})
    emit("update_hand", {"player_hand": [], "username": player, "table_id": table_id}, broadcast=True)
    players_remaining = table_collection.find_one({"table_id": table_id}, {"_id": 0, "players": 1})["players"]
    if len(players_remaining) == 0:
        socketio.sleep(2)
        table_collection.update_one({"table_id": table_id}, {"$set": {"game_over": True}})
        
    #### Todo: What to do with person who folds? Disconnect?

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
    current_player_index = player_list.index(table["current_player"])
    next_player = player_list[(current_player_index + 1) % len(player_list)]
    
    table_collection.update_one({"table_id": table_id}, {"$set": {"current_player": next_player}})
    user_collection.update_one({"username": next_player}, {"$set": {"has_moved": False}})

    emit("next_turn", {"username": next_player, "table_id": table_id}, broadcast=True)


def update_deck(table_id, deck):
    table_collection.update_one({"table_id": table_id}, {"$set": {"deck": deck}})

def update_dealer_hand(table_id, hand):
    table_collection.update_one({"table_id": table_id}, {"$set": {"dealer_hand": hand}})

def update_player_hand(username, hand):
    user_collection.update_one({"username": username}, {"$set": {"hand": hand}})




