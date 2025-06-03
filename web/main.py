import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    #dataset_path = "../json_dump/match"
    dataset_path = "json_dump\\match"
    editions = []
    if os.path.exists(dataset_path) and os.path.isdir(dataset_path):
        for f_name in os.listdir(dataset_path):
            if f_name.endswith(".json"):
                editions.append(f_name.replace(".json", ""))
        editions.sort() # Ordina gli anni
        editions.reverse()
    else:
        print(f"Attenzione: La cartella '{dataset_path}' non esiste o non è una directory.")
        # Potresti voler gestire questo caso in modo diverso, es. mostrando un errore all'utente

    return render_template("index.html", editions=editions)


@app.route('/edizione/<year>')
def edizione_detail(year):
    return f"<h1>Dettagli per l'edizione {year}</h1><p>Qui verranno mostrati i contenuti di {year}.json.</p><a href='{url_for('index')}'>Torna alla Home</a>"

if __name__ == '__main__':
    app.run(debug=True)
