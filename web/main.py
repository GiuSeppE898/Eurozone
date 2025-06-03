import os
from flask import Flask, render_template, url_for

from src.db.conf import client
from src.db.repository.match_repository import MatchRepository
from src.db.repository.player_repository import PlayerRepository

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
    return render_template('results.html', edition=edition, results=results)

if __name__ == '__main__':
    app.run(debug=True)
