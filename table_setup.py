from pymongo import MongoClient

def add_player(player_data):
    client = MongoClient('mongodb://localhost:27017/')

    db = client['blackjack']
    collection = db['tables']

    result = collection.insert_one(player_data)

    print(f"Player added with ID: {result.inserted_id}")

    client.close()