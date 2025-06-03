import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    editions = []
    for x in range(1960,2025,4):
        editions.append(x)
    editions.sort() # Ordina gli anni
    editions.reverse()

    return render_template("index.html", editions=editions)


@app.route('/edizione/<year>')
def edizione_detail(year):
    return f"<h1>Dettagli per l'edizione {year}</h1><p>Qui verranno mostrati i contenuti di {year}.json.</p><a href='{url_for('index')}'>Torna alla Home</a>"

if __name__ == '__main__':
    app.run(debug=True)
