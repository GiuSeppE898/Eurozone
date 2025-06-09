from pymongo import MongoClient

from db.model.player import Player

class PlayerRepository:
    def __init__(self, client: MongoClient, db_name="eurozone", collection_name="players"):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_player(self, player: Player):
        return self.collection.insert_one(player.to_dict())

    def find_player_by_id_and_match(self, player_id: int, match_id: int):
        data = self.collection.find_one({'id_player': player_id, 'id_match': match_id})
        return Player.from_dict(data) if data else None

    def update_player(self, player: Player):
        return self.collection.update_one(
            {"id_player": player.id_player}, 
            {"$set": player.to_dict()}
        )

    def delete_player(self, player_id: int):
        return self.collection.delete_one({"id_player": player_id})


    # Trovato tramite nome
    def find_player_by_name(self, name: str):
        data = self.collection.find_one({'name': name})
        return Player.from_dict(data) if data else None

    # Trovato tramite id
    def find_player_by_id(self, id_player: int) -> Player:
        data = self.collection.find_one({'id_player': id_player})
        return Player.from_dict(data) if data else None