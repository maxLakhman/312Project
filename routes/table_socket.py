from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect
from flask_login import current_user
from app import socketio
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
import random


@socketio.on('first_hand')
def handle_first_hand(data):
    if not current_user.is_authenticated:
        disconnect()

    MongoClient = MongoClient("db")
    db = MongoClient["BlackJack"]
    user_collection = db["user"]
    table_collection = db["tables"]

    # find the current user in the database
    username = current_user.id
    user = user_collection.find_one({"username": username})

    # find the table id
    table = user.get("table_id")
    table_info = table_collection.find_one({"table_id": table})

    # give the newly joined user their hand
    deck = table_info.get("deck")
    
    # shuffle the deck and randomly select 2 cards for the user
    random.shuffle(deck)
    hand = deck[:2]
    deck = deck[2:]

    # update the user's hand in the database
    user_collection.update_one(
        {"username": username},
        {"$set": {"hand": hand}}
    )

    # update the table's deck in the database
    table_collection.update_one(
        {"table_id": table},
        {"$set": {"deck": deck}}
    )


    # emit the user's hand to the user
    emit('hand', {'hand': hand}, room=username)

    


@socketio.on('deal_card')
def handle_deal_card(data):

    if not current_user.is_authenticated:
        disconnect()

    MongoClient = MongoClient("db")
    db = MongoClient["BlackJack"]
    user_collection = db["user"]
    table_collection = db["tables"]

    # find the current user in the database
    username = current_user.id
    user = user_collection.find_one({"username": username})
    print(user)

    # find the table id
    table = user.get("table_id")
    print(table)
    table_info = table_collection.find_one({"table_id": table})
    print(table_info)







@socketio.on('play_card')
def handle_play_card(data):
    room = data['table_id']
    player_id = data['player_id']
    card = data['card']
    emit('card_played', {'player_id': player_id, 'card': card}, room=room)
