import pprint
import pandas as pd

from data.match_loader import MatchLoader
import data.player_loader as pl
from src.db.model.player import Player
from src.db.repository.player_repository import PlayerRepository
from src.db.conf import client
from src.db.model.match import Match
from src.db.repository.match_repository import MatchRepository


def load_player_data_from_csv(debug: bool = True) -> pd.DataFrame:
    player_loader = pl.PlayerLoader("./data/euro_lineups.csv")
    data = player_loader.load()
    if debug:
        print(data)
    
    stats = player_loader.kowalsky()
    stats_without_na_counts = {key: value for key, value in stats.items() if key != 'na_counts'}
    
    if debug:
        pprint.pprint(stats_without_na_counts)
        print(stats['na_counts'])
    
    cleaned_data = player_loader.clean_data()
    if debug:
        print(cleaned_data)
    
    # Stampo l'id minore della colonna id_club
    min_id_club = cleaned_data['id_club'].min()
    if debug:
        print(f"Min id_club: {min_id_club}")
    
    # Stampo l'id minore della colonna id_player
    min_id_player = cleaned_data['id_player'].min()
    if debug:
        print(f"Min id_player: {min_id_player}")
    
    sanitized_data = player_loader.sanitize_data()
    if debug:
        print(sanitized_data)
    
    # Ottengo tutti i valori unici della colonna position_national
    unique_positions = sanitized_data['position_national'].unique()
    if debug:
        print(f"Unique positions: {unique_positions}")
    
    # Rieseguo una analisi
    stats = player_loader.kowalsky()
    stats_without_na_counts = {key: value for key, value in stats.items() if key != 'na_counts'}
    
    if debug:
        pprint.pprint(stats_without_na_counts)
        print(stats['na_counts'])
    
    # Salvo i dati puliti in un nuovo file json
    player_loader.dump_to_json("./json_dump/players.json")

    # Stampo i giocatori unici in base alla colonna id_player
    if debug:
        print(f"Non unique players: {len(sanitized_data)}")
    unique_players = sanitized_data['id_player'].unique()
    if debug:
        print(f"Unique players: {len(unique_players)}")
        
    return sanitized_data

def save_players_to_db(data: pd.DataFrame):
    # Carico i dati all'interno del database
    player_repository = PlayerRepository(client)

    total_rows = len(data)
    for index, row in data.iterrows():
        player = Player(
            name=row['name'],
            name_shirt=row['name_shirt'],
            jersey_number=row['jersey_namber'],
            position_national=row['position_national'],
            position_field=row['position_field'],
            birth_date=row['birth_date'],
            id_match=row['id_match'],
            id_player=row['id_player'],
            start=row['start'],
            year=row['year'],
            id_club=row['id_club'],
            id_national_team=row['id_national_team']
        )
        
        player_repository.insert_player(player)
        
        # Mostro il progresso ogni 15 iterazioni e alla fine
        if index % 15 == 0 or index == total_rows - 1:
            p = ((index + 1) / total_rows) * 100
            print(f"Percentuale di caricamento: {p:.2f}%", end="\r")


def load_match_data_from_csv(debug: bool = True):
    match_loader = MatchLoader("./data/matches/matches/euro")
    match_loader.load_and_save('./json_dump/match')
def save_matches_to_db(match_data: list):
    match_repository = MatchRepository(client)

    total = len(match_data)
    for index, row in enumerate(match_data):
        # Metti qui il controllo: stampa il dizionario raw
        if index == 0:  # controlla solo il primo per non intasare il terminale
            import pprint
            print("\n--- RAW DATA ---")
            pprint.pprint(row)

        try:
            match = Match.from_dict(row)

            # Stampa anche il risultato dopo conversione in dict
            if index == 0:
                print("\n--- AFTER from_dict e to_dict ---")
                pprint.pprint(match.to_dict())

            match_repository.insert_match(match)
        except Exception as e:
            print(f"Errore nel match all'indice {index}: {e}")

        if index % 15 == 0 or index == total - 1:
            percentuale = ((index + 1) / total) * 100
            print(f"Percentuale di caricamento: {percentuale:.2f}%", end="\r")
if __name__ == "__main__":
    #player_data = load_player_data_from_csv(debug=False)
    #save_players_to_db(player_data)
    match_loader = MatchLoader("/Users/giuseppepiosorrentino/PycharmProjects/NoSQLMAtches/data/matches/matches/euro")
    match_data = match_loader.load(debug=False)  # ritorna lista di dizionari
    save_matches_to_db(match_data)
    
    
    
