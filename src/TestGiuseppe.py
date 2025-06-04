from src.db.conf import client
from src.db.model.Tempo import Tempo
from src.db.model.goal import Goal
from src.db.model.player import Player
from src.db.model.red_card import Red_Card
from src.db.repository.match_repository import MatchRepository
from src.db.repository.player_repository import PlayerRepository

mr = MatchRepository(client)
match = mr.search_match_by_id(2024491)
print(match)
"""temp = Tempo(10,10)

redcard = Red_Card("SECOND_HALF","Jaroslav Pollák","TCH",temp)
mr.insert_red_card(4024,redcard)"""
"""
goal = Goal("Jaroslav Pollák",temp,"SCORED")
mr.insert_goal(4024,goal,"Ronaldo")

"""