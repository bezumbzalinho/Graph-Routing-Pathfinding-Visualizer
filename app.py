from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import re
from Backend import My_Map, Algorithms

app = Flask(__name__)
CORS(app)

algorithms = None

result = None

cities = []

algorithm = None

debug = None

error = None

def initialize():
    graph = My_Map()

    to_faro = {}

    global cities
    with open("./MapaLigacoes.csv", 'r', encoding='utf-8-sig') as file:
        conteudo_ficheiro = file.read()
        conteudo = re.split(',|\n', conteudo_ficheiro)
        for i in range(0, len(conteudo)-1, 3):
            item = conteudo[i:i+3]
            graph.connect(item[0], item[1], int(item[2]))
            if item[0] not in cities:
                cities.append(item[0])
            elif item[1] not in cities:
                cities.append(item[1])
    with open("./DistanceToFaro.csv", 'r', encoding='utf-8-sig') as file:
        conteudo_ficheiro = file.read()
        conteudo = re.split(',|\n', conteudo_ficheiro)
        for i in range(0, len(conteudo)-1, 2):
            item = conteudo[i:i+2]
            to_faro.setdefault(item[0], int(item[1]))

    global algorithms
    algorithms = Algorithms(graph, to_faro=to_faro)

@app.route('/', methods=['GET', 'POST'])
def index():
    global result, cities, algorithm, debug, error
    if request.method == 'GET':
        return render_template('index.html', result=result, cities=cities, algorithm=algorithm, debug=debug, error=error)
    else:
        result = None; algorithm = None; debug = None; error = None
        if 'algorithm' in request.form and 'start' in request.form:
            if 'end' in request.form and request.form['start'] != request.form['end']:
                match request.form['algorithm']:
                    case "dfs":
                        result = algorithms.depth_first_search(request.form['start'], request.form['end'])
                        algorithm = "Deep First Search"
                    case "ucs":
                        result = algorithms.uniform_cost(request.form['start'], request.form['end'])
                        algorithm = "Uniform Cost Search"
            elif request.form['start'] != 'Faro' and 'end' not in request.form:
                match request.form['algorithm']:
                    case "gs (pure)":
                        result = algorithms.greedy_search(request.form['start'], pure=True)
                        algorithm = "Greedy Search (Pure)"
                    case "gs":
                        result = algorithms.greedy_search(request.form['start'])
                        algorithm = "Greedy Search"
                    case "a*":
                        result = algorithms.a_star(request.form['start'])
                        algorithm = "A*"
            else:
                if 'end' in request.form and request.form['start'] == request.form['end']:
                    error = "You selected the same cities."
                elif request.form['start'] == 'Faro' and 'end' not in request.form:
                    error = "You can not select Faro as origin city for this algorithm."
                else:
                    error = "Something went wrong. Try again later."
            if 'debug' in request.form and request.form['debug'] == 'on' and result is not None: debug = True              
                
            #print(result)
        return redirect(url_for('index'))

# if you run with gunicorn uncomment the following line
initialize()

if __name__ == "__main__":
    # if you run with buit-in start server in flask uncomment the following line
    #initialize()
    app.run(host="0.0.0.0", port=5006)