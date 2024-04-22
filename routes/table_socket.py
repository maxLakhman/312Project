from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_socketio import SocketIO, emit, disconnect
from flask_login import current_user
from app import socketio
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
import random


@socketio.on('first_hand')
def handle_first_hand():
    if not current_user.is_authenticated:
        disconnect()

    mongo = MongoClient("db")
    db = mongo["BlackJack"]
    user_collection = db["user"]
    table_collection = db["tables"]

    # find the current user in the database
    username = current_user.id
    user = user_collection.find_one({"username": username})
    print(user)

    # find the table id
    table = user.get("table")
    print(table)
    table_info = table_collection.find_one({"table_id": table})

    # give the newly joined user their hand
    deck = table_info.get("deck")
    
    # shuffle the deck and randomly select 2 cards for the user
    random.shuffle(deck)
    hand = deck[:2]
    deck = deck[2:]

    # also generate a hand for the dealer
    dealer_hand = deck[:2]
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

    # update the dealer hand
    table_collection.update_one(
        {"table_id": table},
        {"$set": {"dealer_hand": dealer_hand}}
    )

    # emit the user's hand to the user and their username
    emit('hand', {'hand': hand, 'dealer_hand': dealer_hand, 'username': username}, broadcast=True)




@socketio.on('hit')
def handle_deal_card():

    if not current_user.is_authenticated:
        disconnect()

    mongo = MongoClient("db")
    db = mongo["BlackJack"]
    user_collection = db["user"]
    table_collection = db["tables"]

    # find the current user in the database
    username = current_user.id
    user = user_collection.find_one({"username": username})
    print(user)
    
    # find the table id
    table = user.get("table")
    print(table)
    table_info = table_collection.find_one({"table_id": table})
    print(table_info)

    # add a new card to the user's hand
    hand = user.get("hand")
    deck = table_info.get("deck")
    random.shuffle(deck)
    new_card = deck[0]
    deck = deck[1:]
    hand.append(new_card)

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

    # emit the new card to the user
    emit('hand', {'hand': hand, 'username': username}, broadcast=True)







@socketio.on('stand')
def handle_play_card(data):
    pass


