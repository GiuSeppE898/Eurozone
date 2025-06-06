from flask import Flask, render_template
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from db.conf import client
from db.model.player import Player
from db.repository.match_repository import MatchRepository
from db.repository.player_repository import PlayerRepository

from flask import request
from datetime import datetime

app = Flask(__name__)
mr = MatchRepository(client)
@app.route('/')
def index():
    editions = []
    for x in range(1960,2025,4):
        editions.append(x) 
    editions.sort() # Ordina gli anni
    editions.reverse()
 
    return render_template("index.html", editions=editions)


@app.route('/results/<int:edition>')
def results_page(edition):
    results = mr.get_match_from_edition(edition)
    
    # HACK: home_penalty e away_penalty possono essere NaN, li converto in None
    # va rifatto il db
    for result in results:
        if result['home_penalty'] != result['home_penalty']:
            result['home_penalty'] = None 
        if result['away_penalty'] != result['away_penalty']:
            result['away_penalty'] = None
            
    grouped_results = {}
    for result in results: 
        round_name = result['round']
        if round_name not in grouped_results:
            grouped_results[round_name] = []
        grouped_results[round_name].append(result)
    
    unique_winner_reasons = set()
    for result in results:
        if 'winner_reason' in result and result['winner_reason']:
            unique_winner_reasons.add(result['winner_reason'])
    
    return render_template('results.html', edition=edition, results=grouped_results, localized=rounds_it)
 
@app.route("/match/<match_id>") 
def match_detail(match_id):
    match = mr.search_match_by_id(int(match_id))

    # Legge l'ordine richiesto (di default: ascendente)
    order = request.args.get("order", "asc").lower()

    # Ordina gli eventi
    if "events" in match:
        match["events"].sort(
            key=lambda e: (
                e["time_minute"] if isinstance(e.get("time_minute"), (int, float)) else 999,
                e["time_second"] if isinstance(e.get("time_second"), (int, float)) else 0
            ),
            reverse=(order == "desc")
        )
    
    players: list[Player] = []
 
    pr = PlayerRepository(client)

    for lineup in match['home_lineups']: 
        player_info = pr.find_player_by_id(int(lineup['id_player']))
        if player_info: 
            player_info.team_side = 'home' 
            player_info.field = lineup['start'] == "field"
            players.append(player_info)

    for lineup in match['away_lineups']:
        player_info = pr.find_player_by_id(int(lineup['id_player']))
        if player_info:
            player_info.team_side = 'away'
            player_info.field = lineup['start'] == "field"
            players.append(player_info)
            
    match['date'] = format_date_human(match['date_time'])
            
    assign_player_positions(players)

    return render_template("match_detail.html", match=match, players=players, localized_roles=roles_it, localized_winner_reason=winner_reason_it, localized_misc=misc_it)


@app.route("/player/<int:player_id>")
def player_detail(player_id):
    pr = PlayerRepository(client)
    player = pr.find_player_by_id(player_id)

    # Formatta la data in formato GG/MM/AAAA
    if player and player.birth_date:
        try:
            player.birth_date = datetime.strptime(player.birth_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception as e:
            print("Errore formattazione data:", e)

    goal= mr.count_goals_by_player_name(player.name)

    assist = mr.count_assists_by_player_id(player_id)

    total_game = mr.count_matches_played_by_player_id(player_id)

    starter = mr.count_matches_started_by_player_id(player_id)

    if not player:
        return "Giocatore non trovato", 404

    # Recupera statistiche, eventi, partite, ecc. (puoi ampliare in seguito)
    return render_template("player_detail.html", player=player, goals=goal, assists=assist, appearances=total_game, starters=starter)


def assign_player_positions(players):
    """
    funzione di utility per assegnare le posizioni ai giocatori
    """
    from collections import defaultdict

    def generate_positions(y_fixed, count):
        if count == 1:
            return [(50, y_fixed)]
        else:
            interval = 70 / (count - 1)
            return [(15 + i * interval, y_fixed) for i in range(count)]

    Y_COORDS_HOME = {
        "Goalkeeper": 10,
        "Defender": 20,
        "Midfielder": 30,
        "Forward": 40,
    }

    Y_COORDS_AWAY = {
        "Goalkeeper": 90,
        "Defender": 80,
        "Midfielder": 70,
        "Forward": 60,
    }
 
    players_by_team_role = {
        'home': defaultdict(list),
        'away': defaultdict(list),
    }

    for player in players:
        if player.field:
            players_by_team_role[player.team_side][player.position_field].append(player)

    for team_side, y_coords in [('home', Y_COORDS_HOME), ('away', Y_COORDS_AWAY)]:
        for role, players_list in players_by_team_role[team_side].items():
            y_fixed = y_coords.get(role, 50)  # default 50 se ruolo non definito
            count = len(players_list)
            positions = generate_positions(y_fixed, count)

            for player, (x, y) in zip(players_list, positions):
                player.x = x
                player.y = y
                print(f"{team_side.upper()} - {player.name} ({role}) → ({x}, {y})")

    for player in players:
        if not hasattr(player, 'x') or not hasattr(player, 'y'):
            player.x, player.y = 0, 0



def format_date_human(iso_date_str, utc_offset_hours=0):
    from datetime import datetime, timedelta

    dt = datetime.strptime(iso_date_str.rstrip("Z"), "%Y-%m-%dT%H:%M:%S")
    dt = dt + timedelta(hours=utc_offset_hours)
    return dt.strftime("%d %B %Y, %H:%M")


rounds_it = {
    "FINAL": "Finale",
    "SEMIFINAL": "Semifinale",
    "QUARTER_FINALS": "Quarti di finale",
    "ROUND_OF_16": "Ottavi di finale",
    "GROUP_STANDINGS": "Fase a gironi",
}

roles_it = {
    "Goalkeeper": "Portiere",
    "Defender": "Difensore",
    "Midfielder": "Centrocampista",
    "Forward": "Attaccante",
    "Other": "Altro",
}

winner_reason_it = {
    "DRAW": "Pareggio",
    "WIN_ON_PENALTIES": "Vittoria ai rigori",
    "WIN_ON_EXTRA_TIME": "Vittoria ai tempi supplementari",
    "WIN_REGULAR": "Vittoria nei tempi regolamentari",
}

misc_it = {
    "PENALTY" : "Calci di rigore",
    "YELLOW_CARD": "Cartellino giallo",
    "RED_CARD": "Cartellino rosso",
    "SUBSTITUTION": "Sostituzione",
    "GOAL": "Gol",
    "OWN_GOAL": "Autogol",
    "INJURY_TIME": "Tempo di recupero",
    "END_PHASE": "Fine dell'intertempo",
    "START_PHASE": "Inizio dell'intertempo",
    "CORNER": "Calcio d'angolo",
    "OFFSIDE": "Fuorigioco",
    "EXTRA_TIME": "Tempi supplementari",
    "EXTRA_TIME_SECOND_HALF": "Secondo tempo supplementare",
    "EXTRA_TIME_FIRST_HALF": "Primo tempo supplementare",
    "SECOND_HALF": "Secondo tempo",
    "FIRST_HALF": "Primo tempo",
}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
    
    
