import os
from io import StringIO
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cargos = get_available_cargos()  # Pega a lista de cargos disponíveis
    cargo_selected = None
    nome = None
    notas = pd.DataFrame()  # DataFrame vazio
    
    if request.method == 'POST':
        cargo_selected = request.form.get('cargo')
        nome = request.form.get('nome')
        
        if cargo_selected:
            notas = get_data(cargo_selected)
        
        if nome and not notas.empty:
            notas = search_candidate(cargo_selected, nome)
    
    return render_template('index.html', notas=notas, cargos=cargos, cargo_selected=cargo_selected, nome=nome)

CARGO_MAP = {
"cargo1": "Cargo 1 - BANCO DE DADOS",
"cargo2": "Cargo 2 - REDES",
"cargo3": "Cargo 3 - SOFTWARES BÁSICOS",
"cargo4": "Cargo 4 - ANALISTA DE SISTEMAS"
}
REVERSE_CARGO_MAP = {v: k for k, v in CARGO_MAP.items()}

def get_data(cargo):
    file_name = REVERSE_CARGO_MAP.get(cargo, cargo)
    with open(f'data/{file_name}.txt', 'r') as file:
        content = file.read()

    notas = pd.read_csv(StringIO(content), sep=',')
    return notas  # Adicionado o retorno das notas

def search_candidate(cargo, nome_do_candidato):
    file_name = REVERSE_CARGO_MAP.get(cargo, cargo)
    with open(f'data/{file_name}.txt', 'r') as file:
        content = file.read() 

    notas = pd.read_csv(StringIO(content), sep=',')
    return notas[notas['Nome'].str.contains(nome_do_candidato, case=False)]

def get_available_cargos():
    files = [file[:-4] for file in os.listdir('data') if file.endswith('.txt')]
    return [CARGO_MAP.get(file, file) for file in files]

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
